from azure.iot.device import IoTHubDeviceClient
DEVICE_CONNECTION_STRING = "HostName=bs-pi-poc.azure-devices.net;DeviceId=pi-clifton;SharedAccessKey=1Dbch6EdLTGfKX4kngXy9cgysrBxw9tKX1XnghrYiDs="

SLEEP_TIMER = 1
RETRY_TIMER = 1

def spawn_device_client():
    device_client = IoTHubDeviceClient.create_from_connection_string(
        DEVICE_CONNECTION_STRING
    )

    return device_client

#device_client.connect()


def send_message_to_azure(message, messageId):
    """Checks if the message is a json object and sends it to Azure IoT Hub

    Args:
        message (any): The data to be sent to Azure IoT Hub

    Returns:
        print statement saying Message successfully sent to Azure IoT Hub
    """

    # Check if valid json if not, make it valid
    
    device_client.send_message(json.dumps(message))
    # if messageId:
    #     print(f"messageId: {messageId} successfully sent")
    # else:
    #     print("Message successfully sent")







# d = get_dictionary(address_strings)
# new_d = camelCase_keys(d)
# new_d['cpuTempC'] = fetch_temperature()
# labels = ",".join(map(str, list(new_d.keys())))
# try:
#     with open("/home/pi/PyModBus/preprod/superlog.csv", 'a') as file:
#         file.write(labels)
#         file.write('\n')
#         while True:
#             if device_client.connected is True:
#                 try:
#                     d = get_dictionary(address_strings)
#                     new_d = camelCase_keys(d)
#                     new_d['cpuTempC'] = fetch_temperature()
#                     values = ",".join(map(str, list(new_d.values())))
#                     file.write(values)
#                     file.write('\n')
#                     send_message_to_azure(new_d, 'piClifton')
#                     #sleep(1)
#                 except ConnectionError:
#                     while device_client.connected is False:
#                         print("Error connecting to Azure IoT Hub")
#                         time.sleep(RETRY_TIMER)
#                         device_client.connect()
#                         if device_client.connected is True:
#                             print("Successfully connected to Azure IoT Hub")
# except Exception as e:
#     error_file = open(f'/home/pi/PyModBus/preprod/ERRORS.txt','a')
#     error_file.write(f"{sys.argv[0]}: [{generate_timestamp()}] ERROR: {str(e)} \n")
#     error_file.close()