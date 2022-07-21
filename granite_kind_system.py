from DeviceManager import DeviceManager
from helpers import generate_timestamp as timestamp
from CloudConnection import CloudConnection
import sys, os
from time import sleep
import pretty_errors

fault_flag_dict = {0: "Nominal/No fault", 1: "Excessive reconnection attempts", 2: "Unimplemented logic reached", 3: "Resource init error", 4: "Cloud init failed"}

f = open(sys.argv[1], 'r')
params = f.readline().split()
print(params)
f.close()

device = DeviceManager(
    kind = params[0], 
    addr = params[1], 
    port = params[2], 
    logpath = params[3], 
    nickname = params[4],
    resourcepath = params[5])

cloud = CloudConnection(
    device_connection_string = params[6],
    sleep_timer = params[7],
    retry_timer = params[8],
    messageId = params[9])

'''
Examples

(note: the example right below is how we are using it right now):
{crontab string} python granite_kind_system eaton_cfg.txt

{crontab string} python granite_kind_system modbus-eaton 10.160.200.98 502 LOGPATH WAL-ATS_Eaton_Power_Meter RESOURCEPATH DEVICE_CONNECTION_STRING 1 1
where ALL_CAPS_SNAKE_VARIABLES are constants
{crontab string} python granite_kind_system modbus-eaton 10.160.200.98 502 LOGPATH WAL-ATS_Eaton_Power_Meter RESOURCEPATH DEVICE_CONNECTION_STRING 1 1

device = DeviceManager(
    kind = sys.argv[1], 
    addr = sys.argv[2], 
    port = sys.argv[3], 
    logpath = sys.argv[4], 
    nickname = sys.argv[5],
    resourcepath = sys.argv[6])

cloud = CloudConnection(
    device_connection_string = sys.argv[7],
    sleep_timer = sys.argv[8],
    retry_timer = sys.argv[9])

cloud = CloudConnection(
    device_connection_string = "HostName=bs-pi-poc.azure-devices.net;DeviceId=pi-clifton;SharedAccessKey=1Dbch6EdLTGfKX4kngXy9cgysrBxw9tKX1XnghrYiDs=",
    sleep_timer = 1,
    retry_timer = 1)
device = DeviceManager(
    kind = 'modbus-eaton', 
    addr = 10.160.200.98, 
    port = 502, 
    logpath = os.getcwd()+'example', 
    nickname = "ATS Eaton Power Meter", 
    resourcepath = 'directory')

'''

device.jot(True, timestamp(), "~~~New Session~~~\n"f'[{device.nickname}] {device.kind} Device Manager script spawned')
if device.start_connection():
    try:
        device.init_resource()
    except Exception as e:
        device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} Device resource init failed due to exception {e}. Check directories.')
        device.fault_flag = 3

try:
    cloud.init_device_client()
except Exception as e:
    device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} Cloud Client init failed due to exception {e}. Check device_connection_string')
    device.fault_flag = 4

while device.fault_flag == 0:
    d = device.fetch_data()
    if cloud.device_client.connected is True:
        try:
            cloud.send_message_to_azure(d)
        except ConnectionError:
            counter = 0
            while cloud.device_client.connected = False:
                device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} [WARNING] Cloud service interruption due to ConnectionError. Restoring connection on attempt {counter}...')
                sleep(cloud.retry_timer)
                cloud.device_client.connect()
                counter += 1
                if cloud.device_client.connected is True:
                    device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} Cloud service restored.')

device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} Fault: {fault_flag_dict[device.fault_flag]}')
device.log.close()