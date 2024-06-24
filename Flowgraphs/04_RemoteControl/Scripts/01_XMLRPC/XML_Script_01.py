#!/usr/bin/env python3
#Coded by Christopher Onwuchekwa
#Umass Boston, MA,USA

import xmlrpc.client
from xmlrpc.client import ServerProxy
import time

# Setup Client Object
xmlrpc_control = ServerProxy('http://'+'localhost'+':8080')

# Modify Signal Frequency
xmlrpc_control.set_sig_freq(50000)
print("Set Signal Frequency to 50KHz...")
time.sleep(2)
xmlrpc_control.set_sig_freq(150000)
print("Set Signal Frequency to 150KHz...")
time.sleep(2)

# Modify Path Selection
xmlrpc_control.set_path_select(1)
print("Set to Complex sinusoid...")
time.sleep(2)
xmlrpc_control.set_filter_select(1)
print("Bypass Filter...")
time.sleep(2)

# Reset FG Parameters
xmlrpc_control.set_sig_freq(100000)
xmlrpc_control.set_path_select(0)
xmlrpc_control.set_filter_select(0)
print("Reset Parameters...")
