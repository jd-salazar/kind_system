import pandas as pd
import pickle
import pytz
from datetime import datetime
import bitstring
from bitstring import BitArray
import struct
import sys
from helpers import generate_timestamp, convert_key_toCamelCase

def init_eaton_resource(resourcepath):
    xlsx = pd.ExcelFile(resourcepath)
    df = xlsx.parse('pxm2k-modbus-uid-0')
    address_strings = {}
    #example key: (1352, 'UINT', 'VA Rating')
    #i.e. (x,z,name)
    for x,y,z,name in zip(df['Base Address (1-based)'].values, df['Size (bytes)'].values, df['Type'].values, df['Display Name'].values):
        if z != 'STRING':
            address_strings[(x,z,name)] = int(y) // 2
        else:
            address_strings[(x,z,name)] = 12
    return address_strings

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

def fetch_eaton_dictionary(address_strings, client):
    d = {}
    d['startReadTime'] = generate_timestamp()
    for k in address_strings:
        regs = client.read_holding_registers(k[0]-1,address_strings[k]).registers
        val = process_registers(regs, k[1])
        d[k[2]] = val
    d['endReadTime'] = generate_timestamp()
    return d
