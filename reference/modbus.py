import time
from time import sleep
import pretty_errors
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import pandas as pd
import bitstring
from bitstring import BitArray
import re
import json
import requests
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient
import subprocess, os, sys
import struct
import pytz

sleep(1) #here to let PID_watcher.py "catch up"

def generate_timestamp():
    now = datetime.utcnow()
    unix_now = datetime.timestamp(now)*1000
    return unix_now

try:
    # client = ModbusClient("192.168.1.1", port=502)
    client = ModbusClient("10.160.200.98", port=502)
    client.connect()
except Exception as e:
    error_file = open(f'/home/pi/PyModBus/preprod/ERRORS.txt','a')
    error_file.write(f"[{generate_timestamp()}] ERROR: {str(e)} \n")
    error_file.close()


xlsx = pd.ExcelFile('/home/pi/PyModBus/preprod/pxm2k-modbus-uid-0.xlsx')
df = xlsx.parse('pxm2k-modbus-uid-0')

#https://www.delftstack.com/howto/python/python-find-all-indexes-of-a-character-in-string/
def convert_key_toCamelCase(key):
    s = ''
    s += key[0].lower()
    rest_of_string = key[1:]
    if '(' in rest_of_string:
        start = rest_of_string.find('(')
        end = rest_of_string.find(')')
        parenthesis_encl_string = rest_of_string[start:end+1].replace('(','').replace(')','')
        l = parenthesis_encl_string.split(' ')
        s2 = ''
        for i in l:
            s2+=i.capitalize()
        s3 = rest_of_string[0:start] + s2 + rest_of_string[end:]
        s += s3
    else:
        s+=rest_of_string
    s = s.replace(' ','').replace(')','').replace('(','').replace('-','')
    return s

address_strings = {}
#example key: (1352, 'UINT', 'VA Rating')
#i.e. (x,z,name)
for x,y,z,name in zip(df['Base Address (1-based)'].values, df['Size (bytes)'].values, df['Type'].values, df['Display Name'].values):
    if z != 'STRING':
        address_strings[(x,z,name)] = int(y) // 2
    else:
        address_strings[(x,z,name)] = 12

def split_int_into_two_bytes(regval: int):
    padding = '0' * (16 - len(bin(regval)[2:]))
    b = padding + bin(regval)[2:]
    first_byte = int('0b'+ b[:-8] ,2)
    second_byte = int('0b'+ b[-8:] ,2)
    return [first_byte, second_byte]


def process_modbus_DATE_type(regs):
    local = pytz.timezone('UTC')
    if len(regs) == 6:
        seconds = str(regs[5])[0:2]
        milliseconds = str(regs[5])[2:]
        try:
            t = datetime.strptime(f'{regs[2]}-{regs[0]}-{regs[1]} {regs[3]}:{regs[4]}:{seconds}.{milliseconds}', "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
             # return f"Buggy timestamp: {regs[2]}-{regs[0]}-{regs[1]} {regs[3]}:{regs[4]}:{seconds}.{milliseconds} register raws = {regs}"
             return "Placeholder"
        # utc_dt = local_dt.astimezone(pytz.utc)
    else:
        '''
        note :ymdHMS
        we're working with 3 registers which means 6 bytes
        B1 B2 B3 B4 B5 B6
        B1 & 0xFF: year
        B2 & 0x0C: month
        B3 & 0x1F: day
        B4 & 0x18: hour
        B5 & 0x3C: minute
        B6 & 0x3C: seconds
        '''
        year_and_month = split_int_into_two_bytes(regs[0])
        day_and_hour = split_int_into_two_bytes(regs[1])
        minute_and_seconds = split_int_into_two_bytes(regs[2])
        year = year_and_month[0] & 0xFF
        month = year_and_month[1] & 0x0C
        day = day_and_hour[0] & 0x1F
        hour = day_and_hour[1] & 0x18
        minute = minute_and_seconds[0] & 0x3C
        seconds = minute_and_seconds[1] & 0x3C
        try:
            t = datetime.strptime(f'20{year}-{month}-{day} {hour}:{minute}:{seconds}', "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # return f"Buggy timestamp: {year}-{month}-{day} {hour}:{minute}:{seconds} register raws = {regs}"
            return "Placeholder"
    
    local_dt = local.localize(t)
    return time.mktime(local_dt.timetuple())

def process_registers(regs, typ):
    hex_str = ''.join(format(i, '02x') for i in regs)
    if typ == 'INT':
        return int(hex_str, 16)
    if typ == 'UINT':
        #needs to be tested on mock prod
        return int(hex_str, 16)
    if typ == 'FLOAT':
        if hex_str == '0000':
            hex_str = '00000000'
        if len(hex_str) != 8:
            hex_str += '0'*(8-len(hex_str))
        return struct.unpack('!f', bytes.fromhex(hex_str))[0]
    if typ == 'DATE':
        return process_modbus_DATE_type(regs)
        # return "Dummy"
    if typ == 'STRING':
        return bytearray.fromhex(hex_str).decode().replace('\x00','')

def get_dictionary(address_strings):
    d = {}
    d['startReadTime'] = generate_timestamp()
    for k in address_strings:
        regs = client.read_holding_registers(k[0]-1,address_strings[k]).registers
        val = process_registers(regs, k[1])
        d[k[2]] = val
    d['endReadTime'] = generate_timestamp()
    return d

def camelCase_keys(d):
    new_d = {}
    for key in d.keys():
        new_d[convert_key_toCamelCase(key)] = d[key]
    return new_d

def test_CamelCaseConverter(keys):
    for key in keys:
        try:
            # print(key, '{', convert_key_toCamelCase(key), '}')
            print(convert_key_toCamelCase(key))
        except TypeError:
            print(key)

def fetch_temperature():
    if sys.platform == 'linux':
        if os.uname()[1] == 'raspberrypi':
            temperature = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            return float(temperature.replace('temp=','').replace("'C",''))
        else:
            temperature = subprocess.run(['sensors'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            return "Not implemented on generic Linux"
    else:
        new_d['cpuTempC'] = "Not implemented on Windows"

DEVICE_CONNECTION_STRING = "HostName=bs-pi-poc.azure-devices.net;DeviceId=pi-clifton;SharedAccessKey=1Dbch6EdLTGfKX4kngXy9cgysrBxw9tKX1XnghrYiDs="

SLEEP_TIMER = 1
RETRY_TIMER = 1

device_client = IoTHubDeviceClient.create_from_connection_string(
    DEVICE_CONNECTION_STRING
)

device_client.connect()


def send_message_to_azure(message, messageId):
    """Checks if the message is a json object and sends it to Azure IoT Hub

    Args:
        message (any): The data to be sent to Azure IoT Hub

    Returns:
        print statement saying Message successfully sent to Azure IoT Hub
    """

    # Check if valid json if not, make it valid
    device_client.send_message(json.dumps(message))
    if messageId:
        print(f"messageId: {messageId} successfully sent")
    else:
        print("Message successfully sent")


#########################################################################
############ Looped Message Sending #####################################
#########################################################################

"""
Whatever the name of the data dictionary you are adding the modbus registers to, assign it to the variable "data_dict and we should be good to go"
"""


d = get_dictionary(address_strings)
new_d = camelCase_keys(d)
new_d['cpuTempC'] = fetch_temperature()
labels = ",".join(map(str, list(new_d.keys())))
try:
    with open("/home/pi/PyModBus/preprod/superlog.csv", 'a') as file:
        file.write(labels)
        file.write('\n')
        while True:
            if device_client.connected is True:
                try:
                    d = get_dictionary(address_strings)
                    new_d = camelCase_keys(d)
                    new_d['cpuTempC'] = fetch_temperature()
                    values = ",".join(map(str, list(new_d.values())))
                    file.write(values)
                    file.write('\n')
                    send_message_to_azure(new_d, 'piClifton')
                    #sleep(1)
                except ConnectionError:
                    while device_client.connected is False:
                        print("Error connecting to Azure IoT Hub")
                        time.sleep(RETRY_TIMER)
                        device_client.connect()
                        if device_client.connected is True:
                            print("Successfully connected to Azure IoT Hub")
except Exception as e:
    error_file = open(f'/home/pi/PyModBus/preprod/ERRORS.txt','a')
    error_file.write(f"{sys.argv[0]}: [{generate_timestamp()}] ERROR: {str(e)} \n")
    error_file.close()