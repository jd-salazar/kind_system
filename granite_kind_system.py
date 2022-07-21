from DeviceManager import DeviceManager
from helpers import generate_timestamp as timestamp
from CloudConnection import CloudConnection
import sys, os
import pretty_errors

fault_flag_dict = {0: "Nominal/No fault", 1: "Excessive reconnection attempts", 2: "Unimplemented logic reached", 3: "Resource init error"}

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
    retry_timer = params[8])

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

while device.fault_flag == 0:
    d = device.fetch_data()
    cloud.send_message_to_azure(d)

device.jot(True, timestamp(), f'[{device.nickname}] {device.kind} Fault: {fault_flag_dict[device.fault_flag]}')
device.log.close()