from helpers import generate_timestamp
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import modbus_eaton
import modbus_sel
from can import Bus as can_client
from time import sleep

#kinds of devices so far: MODBUS-Eaton, MODBUS-SEL, pcan

'''
a "kind" is basically a label for a real physical device, 
target kinds will include TCP-Modbus devices, J1939 CAN devices, and NI-Visa connected instruments.
two devices of a same kind will have the same connection method, but may differ in data structures and request handling.
    (A great example is MODBUS-Eaton and MODBUS-Sel. They connect to their clients identically, however there will be some differences
    in how requests are formed and how requests are processed.)
two devices of a different kind will always have different connection method and definitely differ in data structures.
However, all kinds will share some commonalities.
'''
class DeviceManager:
    def __init__(self, kind, addr, port, logpath, nickname, resourcepath):
        # ~~~constant identifiers~~~ #
        self.modbus_kinds = ["modbus-eaton", "modbus-sel"]
        self.can_kinds = ["pcan"] #https://python-can.readthedocs.io/en/master/interfaces.html, https://python-can.readthedocs.io/en/master/interfaces/pcan.html, https://pypi.org/project/python-can/
        # ~~~initializizers~~~ #
        self.kind = kind
        self.addr = addr #ip address or None
        self.port = port #TCPIP port or COM port
        self.logpath = logpath #where we will write this device's log
        self.nickname = nickname
        self.resourcepath = resourcepath

        # ~~~runtime derived~~~ #
        self.log = open(f'{logpath}.txt','a')
        self.client = None
        self.fault_flag = 0
        self.resource = None
        self.current_data = None

    def jot(self, newl, *args):
        entry = ''
        for i in args:
            entry += str(i)
            entry += ','
        if newl == True:
            #terminates comma seperated log entry
            entry = entry[:-1]
            entry += '\n'
        self.log.write(entry)

    def start_connection(self, attempts=1000, sleeptimer = 120):
        #the default timer is 2 minutes to give breathing room for crontab
        #when we need to hurry and start it quickly, we can make it arbitarily short
        for i in range(0, attempts):
            try:
                if self.kind in self.modbus_kinds:
                    modbus_connection()
                if self.kind in self.can_kinds:
                    can_connection()
                self.jot(True, generate_timestamp(), f'[{self.nickname}] {self.kind} Connection successful on attempt {i}')
                self.fault_flag = 0
                return True
            except Exception as e:
                self.jot(True, generate_timestamp(), f'[{self.nickname}] {self.kind} Connection unsuccessful due to {e}')
                sleep(sleeptimer)
        self.fault_flag = 1
        return False

    def modbus_connection(self):
        self.client = ModbusClient(self.addr, port = self.port)
        self.client.connect()
            
    def can_connection(self):
        self.client = can_client(interface = self.kind, channel = self.port, receive_own_messages = True)

    def init_resource(self):
        if self.kind == 'modbus-eaton':
            self.resource = modbus_eaton.init_eaton_resource(self.resourcepath)
        if self.kind == 'modbus-sel':
            self.resource = modbus_sel.rules
        if self.kind == 'pcan':
            pass

    def fetch_data(self):
        try:
            if self.kind == 'modbus-eaton':
                self.current_data = modbus_eaton.fetch_eaton_dictionary(self.resource, self.client)
            if self.kind == 'modbus-sel':
                self.current_data = modbus_sel.fetch_sel_dictionary(self.resource, self.client)
            if self.kind == 'pcan':
                self.jot(True, timestamp(), f'[{self.nickname}] {self.kind} PCAN is meant to be used actively in the interpreter right now')
                #to-do: make config file for autonomous CAN activity
        except Exception as e:
            self.jot(True, generate_timestamp(), f'[{self.nickname}] {self.kind} [WARNING] Connection issue due to {e}, restoring...')
            self.client = None
            start_connection(self, attempts=1000, sleeptimer = .1)  
