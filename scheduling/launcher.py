#!/usr/bin/env python3
import sys, os, subprocess, signal
from time import sleep
from datetime import datetime

def generate_timestamp():
    now = datetime.utcnow()
    unix_now = datetime.timestamp(now)*1000
    return unix_now
try: #zebra
    p = subprocess.Popen(["python3", "test_read_MERGE-TEST.py"], cwd='/home/pi/PyModBus/preprod/')
    if os.path.isfile("/home/pi/PyModBus/preprod/IMPORTANT_PID"):
        os.system('rm /home/pi/PyModBus/preprod/IMPORTANT_PID')
    f = open("/home/pi/PyModBus/preprod/IMPORTANT_PID", 'w')
    f.write(str(p.pid))
    f.close()
    print(p.pid)
    p2 = subprocess.Popen(["python3", "PID_watcher.py"], cwd='/home/pi/PyModBus/preprod/')
except Exception as e:
    error_file = open(f'/home/pi/PyModBus/preprod/ERRORS.txt','a')
    error_file.write(f"[{generate_timestamp()}] Warning: Resetting script due to {str(e)}\n")
    error_file.close()