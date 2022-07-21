from azure.iot.device import IoTHubDeviceClient
import json

class CloudConnection:
    modbus_kinds = ["modbus-eaton", "modbus-sel"]
    can_kinds = ["pcan"] #https://python-can.readthedocs.io/en/master/interfaces.html, https://python-can.readthedocs.io/en/master/interfaces/pcan.html, https://pypi.org/project/python-can/
    def __init__(self, device_connection_string, sleep_timer, retry_timer, device_client):
        #self.device_connection_string = "HostName=bs-pi-poc.azure-devices.net;DeviceId=pi-clifton;SharedAccessKey=1Dbch6EdLTGfKX4kngXy9cgysrBxw9tKX1XnghrYiDs="

        # ~~~initializizers~~~ #
        self.device_connection_string = device_connection_string
        self.sleep_timer = sleep_timer
        self.retry_timer = retry_timer
        self.messageId = messageId

        # ~~~runtime derived~~~ #
        self.device_client = None
        


    def init_device_client(self):
        device_client = IoTHubDeviceClient.create_from_connection_string(
            self.device_connection_string
        )

        self.messageId = None

        self.device_client = device_client
        self.device_client.connect()


    def send_message_to_azure(self, message, messageId):
        """Checks if the message is a json object and sends it to Azure IoT Hub

        Args:
            message (any): The data to be sent to Azure IoT Hub

        Returns:
            print statement saying Message successfully sent to Azure IoT Hub
        """

        # Check if valid json if not, make it valid

        self.device_client.send_message(json.dumps(message), self.messageId)

        # if messageId:
        #     print(f"messageId: {messageId} successfully sent")
        # else:
        #     print("Message successfully sent")
