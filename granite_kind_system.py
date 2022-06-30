from DeviceManager import DeviceManager
import cloud
import time
import sys

device = DeviceManager(kind = sys.argv[1], addr = sys.argv[2], port = sys.argv[3], logpath = sys.argv[4])
cloud_client = cloud.spawn_device_client()
cloud_client.connect()

fault_flag_dict = {0: "Nominal/No fault", 1: "Unimplemented logic reached", 2: "Excessive reconnection attempts"}

def main():
    while device.test_connection([0,1]) is True:
        d = device.fetch_dictionary()
        try:
            cloud_client.send_message_to_azure(d, 'piClifton')
        except Exception as e:
            device.jot(True, generate_timestamp(), f'Cloud fail due to {e}, retrying')
            while cloud_client.connected is False:
                time.sleep(cloud.RETRY_TIMER)


while device.fault_flag == 0:
    device.start_connection()
    main()

device.jot(True, generate_timestamp(), f'Hard fault, reason: {fault_flag_dict[device.fault_flag]}',
    "PID_watcher.py retrying script")