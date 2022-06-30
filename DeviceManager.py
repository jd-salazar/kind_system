import sys
sys.path.append('modbus') #temporary
from helpers import generate_timestamp, convert_key_toCamelCase
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import modbus_eaton
from modbus_eaton import fetch_eaton_dictionary

#kinds of devices so far: MODBUS-Eaton, MODBUS-SEL

'''
a "kind" is just an abstraction of my invention.
a "kind" is basically a label for a real physical device, 
target kinds will include TCP-Modbus devices, J1939 CAN devices, and NI-Visa connected instruments.
two devices of a same kind will have the same connection method, but may differ in data structures and request handling.
    (A great example is MODBUS-Eaton and MODBUS-Sel. They connect to their clients identically, however there will be some differences
    in how requests are formed and how requests are processed.)
two devices of a different kind will always have different connection method and definitely differ in data structures.
However, all kinds will share some commonalities.
    (An example of this is my penchant for using Xlsxwriter to insert images into a spreadsheet. This is great for an Oscilloscope
    because you can pair Oscilloscope measurements with the On-Screen image associated with said measurements. The fundmental subroutines
    for doing this is virtually the same as if you were "copy-pasting" a Matplotlib plot image instead. So, that would be an example of )
'''
class DeviceManager:
    modbus_kinds = ["modbus-eaton", "modbus-sel"]
    def __init__(self, kind, addr, port, logpath, resource):
        # ~~~initializizers~~~ #
        self.kind = kind
        self.addr = addr #ip address or None
        self.port = port #TCPIP port or COM port
        self.logpath = logpath #where we will write this device's log
        self.resource = resource #ex. modbus-eaton-address-strings.pkl if using Eaton Power meter, further explanation later
        '''
        note: preliminarily, a design goal is to ensure a resource will not only always be a dictionary
        but also essentially be an "empty cloud dictionary" where cloud dictionary means the data structure
        the Cloud Team(TM) is asking for.
        partial blocker: right now the resource for modbus-sel is actually a dictionary of dataframes. eventually,
        it will be a "plain" dictionary, but there is still complexity to be wrangled.
        '''
        # ~~~runtime derived~~~ #
        self.log = open(f'{logpath}','w')
        self.client = None
        self.fault_flag = 0

    def jot(self, newl, *args):
        entry = ''
        for i in args:
            entry += str(i)
            entry += ','
        if newl == True:
            #terminates comma seperated log entry
            entry = entry[:-1]
            entry += '\n'
        log.write(entry)

    def start_connection(self, attempts=10):
        if self.kind in modbus_kinds:
            jot(True, generate_timestamp(), f'TCPIP {kind} selected, running connection test')
            for i in range(1, attempts+1):
                try:
                    self.client = ModbusClient(self.addr, port = self.port)
                    self.client.connect()
                    jot(True, generate_timestamp(), f'Attempt {i} connected successfully')
                    return True
                except Exception as e:
                    jot(True, generate_timestamp(), f"[ERROR] Connection Start Attempt {i}: Exception {e} occurred, reattempting")
            self.fault_flag = 2
        else:
            jot(True, "Only TCP Modbus kinds implemented")
            fault_flag = 1
            return False


    def test_connection(self, test_values, attempts=10):
        '''
        test_values would be like say a register address + register length for modbus, (i.e. [0,4] means "fetch the four registers starting at address 0")
        or for J1939 CAN, a PGN request
        for a more obscure example, an NI-VISA connected instrument (oscilloscope or power analyzer) would be like inst.query("*IDN?")
        '''
        if self.kind in modbus_kinds:
            for i in range(1, attempts+1):
                try:
                    client.read_holding_registers(test_values[0], test_values[1]).registers
                    jot(True, generate_timestamp(), f'Connection test successful')
                    return True
                except Exception as e:
                    jot(True, generate_timestamp(), f"[ERROR] Connection Test Attempt {i}: Exception {e} occurred, reattempting")
                self.fault_flag = 2
        else:
            jot(True, "Only TCP Modbus kinds implemented")
            fault_flag = 1
            return False

    def fetch_dictionary(self):
        if self.kind in modbus_kinds:
            if self.kind == 'modbus-eaton':
                # "go the eaton path"
                return fetch_eaton_dictionary(client = self.client)
            if self.kind == 'modbus-sel':
                # "go the SEL path"
                pass
        else:
            jot(True, "Only TCP Modbus kinds implemented")
            device.fault_flag = 1