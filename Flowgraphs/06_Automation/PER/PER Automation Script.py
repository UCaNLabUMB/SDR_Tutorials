#!/usr/bin/env python3
#Coded by Christopher Onwuchekwa
#Umass Boston, MA,USA



#Patch Notes: Small Edits update with latest Features,

import argparse
import contextlib
import xmlrpc.client
from xmlrpc.client import ServerProxy
import sys
import time

server_list = ['http://' + 'localhost' + ':8080','http://' + '10.1.1.2' + ':8080',  'http://' + '10.1.1.3' + ':8080',  'http://' + '10.1.1.4' + ':8080']

def set_fn(file_name, server):
    """Sets the file name on the XML-RPC server"""
    server.set_fn(file_name)
    time.sleep(2)

def set_demofunction(demo_function, server):
    "This is a demo function set function naming to match the variable naming. Make sure to change naming in command functions"
    server.set_demofunction(demo_function)
    time.sleep(2)
                
 
def set_config_param(command, params, servers=None):
    """Sets the given parameter on the XML-RPC servers"""

    # Send command to all servers if no server is specified
    if servers is None:
        servers = server_list

    # Send command to the specified servers
    for server_url in servers:
        try:
            # Create an XML-RPC server object from the URL
            server = xmlrpc.client.ServerProxy(server_url)

            # Call the appropriate command function on the server
            if command in command_functions:
                result = command_functions[command](*params, server)
                print(f"Command '{command}' sent successfully to {server_url}")
                print(f"Server responded: {result}")
            else:
                raise ValueError(f"Invalid command: {command}")
        except ConnectionError as e:
            print(f"Error connecting to the server: {e}")
        except Exception as e:
            print(f"Error: {e}")



command_functions = {
    'set_fn': set_fn, # Set File Name
    'Set_demofunction': set_demofunction # Sets Demo function on the server.
    
}

param_types = {
    'set_fn': str,
}
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute commands on XML-RPC servers.')
    parser.add_argument('command', help='Name of the command to run.')
    parser.add_argument('params', nargs='*', help='Parameters for the command (separated by spaces). For Carriers use num in range of 0-n.')
    parser.add_argument('--server', default=None, help="Server index or 'all' to send the command to all servers (default: all)")

    args = parser.parse_args()

    if args.command.lower() in ['exit', 'quit', 'stop']:
        sys.exit(0)

    try:
        # Convert parameters according to the specified types for the given command
        if args.command in param_types:
            param_type = param_types[args.command]
        else:
            param_type = int
        params = [param_type(param) for param in args.params]

        if args.server is None or args.server.lower() == 'all':
            servers = server_list
        else:
            server_indices = [int(index.strip()) for index in args.server.split(',')]
            servers = [server_list[index] for index in server_indices]

        set_config_param(args.command, params, servers)

    except ValueError as e:
        print(f"Error: {e}")
















