#!/usr/bin/env python3
#Coded by Christopher Onwuchekwa
#Umass Boston, MA,USA

import xmlrpc.client
from xmlrpc.client import ServerProxy
import time

xmlrpc_control = ServerProxy('http://'+'localhost'+':8080')

xmlrpc_control.set_sig_freq(50000)
time.sleep(2)

xmlrpc_control.set_sig_freq(150000)
time.sleep(2)

xmlrpc_control.set_path_select(1)
time.sleep(2)

xmlrpc_control.set_filter_select(1)
time.sleep(2)

xmlrpc_control.set_sig_freq(100000)
xmlrpc_control.set_path_select(0)
xmlrpc_control.set_filter_select(0)

