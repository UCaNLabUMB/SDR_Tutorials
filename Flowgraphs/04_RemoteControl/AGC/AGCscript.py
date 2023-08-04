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

# Function to set the amplitude
def set_amplitude(amplitude, server):
    server.set_amplitude(amplitude)
    time.sleep(2)

# ... (other code above)

def control_loop():
    # Create an XML-RPC server object from the URL
    server = xmlrpc.client.ServerProxy(server_list[0]) # Select the appropriate server. 0 for the first in the list
    
    # Get the initial amplitude
    current_amplitude = server.get_amplitude()
    print(f"Initial Amplitude: {current_amplitude}")

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
                
                # Define power range and target
                lower_bound = 0.25
                upper_bound = 0.5
                target_power = (upper_bound + lower_bound) / 2
                
                # Calculate error as percentage of range
                error = (avg_power - target_power) / (upper_bound - lower_bound)
                print(f"Error: {error}")
                
                # Limit error to range -1 to 1
                error = max(min(error, 1), -1)
                
                # Calculate adjustment as percentage of current amplitude
                adjustment = error * current_amplitude * 0.3  # max 30% adjustment
                print(f"Adjustment: {adjustment}")
                
                # Set the new amplitude
                new_amplitude = current_amplitude + adjustment
                print(f"New Amplitude: {new_amplitude}")
                set_amplitude(new_amplitude, server)
                
                # Update the current amplitude
                current_amplitude = new_amplitude
                    
        else:
            time.sleep(0.1)

control_loop()

