#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
import serial
import socket

import logging
import sys
from datetime import datetime

RAM_NAME = 'Generic Memory'
CPU_NAME = 'ABC 123'
GPU_NAME = 'DFC 456'

HOST = 'localhost'  # (localhost)
CORE_TEMP_PORT = 5200  # Core temp port 
OHW_PORT = 8085 # Open Hardware Monitor Port 
ARDUINO_PORT = 'COM3' # Arduino port


def get_cpu_json_contents(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)  # 5-second timeout
    try:
        s.connect((HOST, CORE_TEMP_PORT))
        data = s.recv(1024)
        try:
            data = json.loads(data.decode('utf-8'))
            if (data['CpuInfo']):
                return data['CpuInfo']
        except ValueError:
            print('Invalid JSON contents')
        
    except socket.timeout:
        print("Connection attempt timed out.")
    except ConnectionRefusedError:
        print("Connection refused.")



def space_pad(number, length):
    """
    Return a number as a string, padded with spaces to make it the given length
    :param number: the number to pad with spaces (can be int or float)
    :param length: the specified length
    :returns: the number padded with spaces as a string
    """

    number_length = len(str(number))
    spaces_to_add = length - number_length
    return (' ' * spaces_to_add) + str(number)

def get_json_contents(json_url):
    """
    Return the contents of a (remote) JSON file
    :param json_url: the url (as a string) of the remote JSON file
    :returns: the data of the JSON file
    """

    data = None

    req = Request(json_url)
    try:
        response = urlopen(req).read()
    except HTTPError as e:
        print('HTTPError ' + str(e.code))
    except URLError as e:
        print('URLError ' + str(e.reason))
    else:
        try:
            data = json.loads(response.decode('utf-8'))
        except ValueError:
            print('Invalid JSON contents')

    return data


def find_in_data(ohw_data, name):
    """
    Search in the OpenHardwareMonitor data for a specific node, recursively
    :param ohw_data:    OpenHardwareMonitor data object
    :param name:        Name of node to search for
    :returns:           The found node, or -1 if no node was found
    """
    if ohw_data == -1:
        raise Exception('Couldn\'t find value ' + name + '!')
    if ohw_data['Text'] == name:
        # The node we are looking for is this one
        return ohw_data
    elif len(ohw_data['Children']) > 0:
        # Look at the node's children
        for child in ohw_data['Children']:
            if child['Text'] == name:
                # This child is the one we're looking for
                return child
            else:
                # Look at this children's children
                result = find_in_data(child, name)
                if result != -1:
                    # Node with specified name was found
                    return result
    # When this point is reached, nothing was found in any children
    return -1


cpu_temp_value = 0
cpu_load_value = 0
ram_load_value = 0
gpu_load_value = 0

def get_hardware_info():
    """
    Get hardware info from OpenHardwareMonitor's web server and format it
    """
    global cpu_temp_value
    global cpu_load_value
    global ram_load_value
    global gpu_load_value

    # Init arrays
    my_info = {}

    # Get actual OHW data (Modify to your Open Hardware Monitor's IP Address)
    ohw_json_url = f'http://localhost:{OHW_PORT}/data.json'
    data_json = get_json_contents(ohw_json_url)

    # Get Core Temp data 
    cpu_data_json = get_cpu_json_contents()
    if (cpu_data_json): 
        cpu_temps = cpu_data_json['fTemp']
        cpu_average_temp = sum(cpu_temps) / len(cpu_temps)
        cpu_temp_value = (f"{cpu_average_temp:.0f}")

    # cpu load
    if (data_json): 
        cpu_data = find_in_data(data_json, CPU_NAME)
        if (cpu_data): 
            cpu_load = find_in_data(cpu_data, 'CPU Total')
            cpu_load_value = cpu_load['Value'][:-4]


    # ram load 
    if (data_json): 
        ram_data = find_in_data(data_json, RAM_NAME)
        if (ram_data): 
            ram_load = find_in_data(ram_data, 'Memory')
            ram_load_value = ram_load['Value'][:-4]

    #gpu load 
    if (data_json): 
        gpu_data = find_in_data(data_json, GPU_NAME)
        if (gpu_data): 
            gpu_load = find_in_data(gpu_data, 'Load')
            if (gpu_load):
                gpu_load_amount = find_in_data(gpu_load, 'GPU Core')
                gpu_load_value = gpu_load_amount['Value'][:-4]


    my_info['cpu_temp'] = cpu_temp_value
    my_info['cpu_load'] = cpu_load_value
    my_info['ram_load'] = ram_load_value
    my_info['gpu_load'] = gpu_load_value

    return my_info



def main():
    serial_port = ARDUINO_PORT
    ser = serial.Serial(serial_port)

    while True:
        current_datetime = datetime.now().strftime("%Y-%m-%d%H-%M-%S")
        logging.basicConfig(filename=f'crash_log_{current_datetime}.txt', 
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

        try: 
            my_info = get_hardware_info()

            if my_info['gpu_load'].isdigit() and \
                my_info['cpu_temp'].isdigit() and \
                my_info['cpu_load'].isdigit() and \
                my_info['ram_load'].isdigit():

                data = '<' + space_pad(int(my_info['cpu_temp']), 3) + \
                        ',' + space_pad(int(my_info['cpu_load']), 3) + \
                        ',' + space_pad(int(my_info['ram_load']), 3) + \
                        ',' + space_pad(int(my_info['gpu_load']), 3) + '>'
                ser.write(data.encode())
                print(data)

        except Exception as e:
            # Log the exception details, including the traceback
            logging.exception("Application crashed with an unhandled exception.")
            print(f"An error occurred. Check 'crash_log_{current_datetime}.txt' for details.")
            sys.exit(1) # Exit with a non-zero status code to indicate an error

        time.sleep(2.5)



if __name__ == '__main__':
    main()
