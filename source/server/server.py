import os
import socket
import subprocess
import sys
import time
import shlex
import netifaces


def get_hamachi_ip():
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)

        if addresses:
            for addr_info in addresses:
                ip = addr_info['addr']

                if ip.startswith('25.'):
                    return ip

    return None


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def change_debug_when_running_as_exe():
    if getattr(sys, 'frozen', False):  # Running as a standalone executable
        return False
    else:  # Running as a script
        return True


DEBUG = change_debug_when_running_as_exe()
DEBUG_prefix = "[debug-build] "

# Set host and port
import server_config as cfg

HOST = open('_config.ini', 'r').read()  # localhost or 127.0.0.1 for local server
PORT = cfg.port

# Check, if ".auto@hamachi_ip"
if HOST == ".auto@hamachi_ip":
    HOST = get_hamachi_ip()
    if HOST is None:
        print("An error occurred: [_config.ini] Couldn't find hamachi ip. Is hamachi active/installed?")
        sys.exit()
    if DEBUG:
        print(DEBUG_prefix + 'Using Hamachi-IP:', HOST)

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket on host and port
server_socket.bind((HOST, PORT))

# Get server run path
server_runpath = os.getcwd()
if DEBUG:
    print(DEBUG_prefix + 'Server Execute-Path:', server_runpath)


first_start = True


# Receive data and send
def start_server(first_start_attr=True):
    # set socket listening
    server_socket.listen(1)

    if DEBUG:
        if first_start_attr:
            print(DEBUG_prefix + 'Server started! Waiting for connection...')
        else:
            print(DEBUG_prefix + 'Server restarted, waiting for connection...')

    # Accept connection
    client_socket, addr = server_socket.accept()
    if DEBUG:
        print(DEBUG_prefix + 'Client connected:', addr)

    first_start_attr = False

    while True:
        try:
            data = client_socket.recv(1024).decode()  # Receive data
        except ConnectionResetError as e:
            if DEBUG:
                print(DEBUG_prefix + 'Connection Reset:', e)
            break

        if not data:
            break

        if DEBUG:
            print(DEBUG_prefix + 'Message from client:', data)

        if data.lower().startswith('cd'):
            splitted_data = shlex.split(data)
            try:
                os.chdir(splitted_data[1])
                cmd_data = 'Changed directory to: ' + str(os.getcwd())
            except:
                cmd_data = 'An error occurred while using "cd"'
        else:
            cmd_data = run_command(data)

        response = " $ " + str(cmd_data)  # Create answer
        client_socket.send(response.encode())  # Send answer


while True:
    start_server(first_start)
    if first_start:
        first_start = False
    time.sleep(3)
    os.chdir(server_runpath)

# Close connections
client_socket.close()
server_socket.close()
