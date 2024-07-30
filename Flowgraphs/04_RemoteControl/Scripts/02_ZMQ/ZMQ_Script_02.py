#!/usr/bin/env python3
#Author: UCaN Lab UMB
#Umass Boston, MA,USA

import numpy as np
import xmlrpc.client
from xmlrpc.client import ServerProxy
import time
import zmq

#################################################################
# Functions
#################################################################
def zmq_measure(my_socket,print_measurements):
	latest_msg = None  # Initialize latest_msg to None
	try:
		while my_socket.poll(0):  # As long as there are messages in the buffer
			latest_msg = my_socket.recv(flags=zmq.NOBLOCK)  # Overwrite latest_msg with the new message
	except zmq.Again:
		pass  # Buffer is now drained, and latest_msg contains the last message
	
	if latest_msg is not None:  # If we got at least one message
		measurement = np.frombuffer(latest_msg, dtype=np.float32, count=-1)		
		if print_measurements == 1: 
			print(f"  Measurements: {measurement}")
		measurement = np.average(measurement)
	else:
		measurement = 0
		print("No message received")


	return measurement

#################################################################
# Script Configuration
#################################################################
PRINT_MEASUREMENTS = 0

rpc_address = 'localhost'
rpc_port = '8080'
zmq_address = '127.0.0.1'
zmq_port = '55555'


# Simulation Parameters
t_setup =1        # Delay time (sec) between setting and measurement
t_pause = 2       # Delay time (sec) between iterations
init_pause = 1    # Delay time (sec) to allow for ZMQ setup

# Configuration settings from flowgraph
REAL_SINE = 0
COMPLEX_SINE = 1

FILTER_ENABLE = 0
FILTER_BYPASS = 1



#################################################################
# Setup
#################################################################
# Setup XMLRPC
xmlrpc_control = ServerProxy('http://' + rpc_address + ':' + rpc_port)

# Setup ZMQ
context = zmq.Context()
socket1 = context.socket(zmq.SUB)

socket1.connect('tcp://' + zmq_address + ':' + zmq_port)
socket1.setsockopt(zmq.SUBSCRIBE, b'')



#################################################################
# Execution (MAIN)
#################################################################
# Initial pause to make sure ZMQ is setup
time.sleep(init_pause)

# Configuration 1
print("Real Sine, Filter Enabled: ")
xmlrpc_control.set_path_select(REAL_SINE)       # Set signal config
xmlrpc_control.set_filter_select(FILTER_ENABLE) # Set filter config
time.sleep(t_pause)
P_avg = zmq_measure(socket1,PRINT_MEASUREMENTS)
print(f"  Average Power: {P_avg:.4}")
time.sleep(t_pause)


# Configuration 2
print("Complex Sine, Filter Enabled: ")
xmlrpc_control.set_path_select(COMPLEX_SINE)       # Set signal config
xmlrpc_control.set_filter_select(FILTER_ENABLE) # Set filter config
time.sleep(t_pause)
P_avg = zmq_measure(socket1,PRINT_MEASUREMENTS)
print(f"  Average Power: {P_avg:.4}")
time.sleep(t_pause)


# Configuration 3
print("Real Sine, Filter Bypass: ")
xmlrpc_control.set_path_select(REAL_SINE)       # Set signal config
xmlrpc_control.set_filter_select(FILTER_BYPASS) # Set filter config
time.sleep(t_pause)
P_avg = zmq_measure(socket1,PRINT_MEASUREMENTS)
print(f"  Average Power: {P_avg:.4}")
time.sleep(t_pause)


# Configuration 4
print("Complex Sine, Filter Bypass: ")
xmlrpc_control.set_path_select(COMPLEX_SINE)       # Set signal config
xmlrpc_control.set_filter_select(FILTER_BYPASS) # Set filter config
time.sleep(t_pause)
P_avg = zmq_measure(socket1,PRINT_MEASUREMENTS)
print(f"  Average Power: {P_avg:.4}")
time.sleep(t_pause)

