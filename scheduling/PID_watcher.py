#!/usr/bin/env python3
import os, sys, subprocess
from time import sleep
from datetime import datetime

def generate_timestamp():
    now = datetime.utcnow()
    unix_now = datetime.timestamp(now)*1000
    return unix_now

try:
    f = open("/home/pi/PyModBus/preprod/IMPORTANT_PID", 'r')
    PID = f.readline().replace('\n','')
    while os.path.isdir(f'/proc/{PID}'):
        0+0
except FileNotFoundError:
    error_file.write(f"{sys.argv[0]}: [{generate_timestamp()}] test_read_MERGE-TEST.py PID died")

error_file = open(f'/home/pi/PyModBus/preprod/ERRORS.txt','a')
error_file.write(f"{sys.argv[0]}: [{generate_timestamp()}] Warning: Resetting init_modbus_script.py\n")
error_file.close()
p = subprocess.Popen(["python3", "init_modbus_script.py"], cwd='/home/pi/PyModBus/preprod/')

#ssh pi@10.160.110.120
#pscp pi@10.160.110.120:/home/pi/PyModBus/preprod/superlog_log.txt C:\Users\JavierSalazar\