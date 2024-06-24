#!/usr/bin/python3
# -*- coding: utf-8 -*-

# zmq_SUB_proc.py
# Author: UCan Lab

import zmq
import numpy as np
import time
import xmlrpc.client
import argparse
import sys

# Set up XML-RPC servers
server_list = ['http://' + 'localhost' + ':8080','http://' + '10.1.1.2' + ':8080',  'http://' + '10.1.1.3' + ':8080',  'http://' + '10.1.1.4' + ':8080']

# Set up ZMQ
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:55555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

def control_loop():
    start_time = time.perf_counter()
    prev_time = start_time
    
    while True:
        current_time = time.perf_counter()
        # Only process data every 1 second
        if current_time - prev_time >= 1:
            prev_time = current_time
            
            latest_msg = None
            while socket.poll(0):
                latest_msg = socket.recv(flags=zmq.NOBLOCK)  # grab the latest message
                
            if latest_msg is not None:
                data = np.frombuffer(latest_msg, dtype=np.float32, count=-1)
                avg_power = np.average(data)
                print(f"Average Power: {avg_power}")

        else:
            time.sleep(0.1)

control_loop()
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# zmq_SUB_proc.py
# Author: UCan Lab

import zmq
import numpy as np
import time
import xmlrpc.client
import argparse
import sys

# Set up XML-RPC servers
server_list = ['http://' + 'localhost' + ':8080','http://' + '10.1.1.2' + ':8080',  'http://' + '10.1.1.3' + ':8080',  'http://' + '10.1.1.4' + ':8080']

# Set up ZMQ
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:55555")
socket.setsockopt(zmq.SUBSCRIBE, b'')

def control_loop():
    start_time = time.perf_counter()
    prev_time = start_time
    
    while True:
        current_time = time.perf_counter()
        # Only process data every 1 second
        if current_time - prev_time >= 1:
            prev_time = current_time
            
            latest_msg = None
            while socket.poll(0):
                latest_msg = socket.recv(flags=zmq.NOBLOCK)  # grab the latest message
                
            if latest_msg is not None:
                data = np.frombuffer(latest_msg, dtype=np.float32, count=-1)
                avg_power = np.average(data)
                print(f"Average Power: {avg_power}")

        else:
            time.sleep(0.1)

control_loop()
