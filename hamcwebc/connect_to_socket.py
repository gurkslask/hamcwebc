'''Here it is.'''
import pickle
import socket
import sys
import os
import json

__author__ = 'alexander'

file_name = 'data_points.json'
app_dir = os.path.abspath(os.path.dirname(__file__))

def call_server(message):
    '''
    This function takes a dict and returns a dict. Example:
    {'r': ['self.VS1_GT1.temp',
                     'self.VS1_GT2.temp',
                     'self.VS1_GT3.temp',
                     'self.SUN_GT2.temp',
                     'self.Setpoint_VS1',
                     'self.VS1_SV1_SP_Down',
                     'self.Komp.DictVarden',
                     'self.ThreeDayTemp'
    ]}
    or if you want to write:
    {'w': [['self.Setpoint_Vs1', 20.0]]
    }
    and returns a dict where the variable names is the keys
    paired with the values
    '''
    message = pickle.dumps(message)
    HOST = '192.168.1.8'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print("fel")
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)
    # print 'Received', repr(data)

def read_file():
    """Extract the JSON file."""
    with open(os.path.join(app_dir, file_name), 'r') as f:
        jsonData = json.load(f)
        return jsonData

def readJSON(jsonData):
    '''Read names of sensors from JSON file.'''
    readlist = [jsonData[sensor]['name'] for sensor in jsonData]
    print(readlist)


if __name__ == '__main__':
    command_str = sys.argv[1].replace('\n', '').split(':')
    print(command_str)
    command = {command_str[0]: [command_str[1]]}
    print(call_server(command))
