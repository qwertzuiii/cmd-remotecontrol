import socket
import os


def read_config(filename="config.ini"):
    with open(filename, 'r') as f:
        cfgdata = f.read()
    return cfgdata


def split_config(data):
    return data.split('^')


config = read_config()
config = split_config(config)


# Set host and port
HOST = config[0]  # Set IP
PORT = int(config[1])  # Set Port

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to server
client_socket.connect((HOST, PORT))
print('Connected to server:', HOST, PORT)

# Set timeout
client_socket.settimeout(5)

# Check if autostart
if os.path.exists('_autostart.ini'):
    autostart = True
    autostart_string = open("_autostart.ini", 'r').read()
else:
    AUTOSTART = False


# Send data
while True:
    if not autostart:
        message = input('{}:{} @ '.format(config[0], config[1]))
    elif autostart:
        message = autostart_string
        autostart = False

    if message.lower() == 'exit' or message.lower() == 'q':
        break
    if ";set socket.timeout" in message.lower():
        socket_timeout = float(input('SOCKET.TIMEOUT = '))
        client_socket.settimeout(socket_timeout)
        continue
    if message.lower() == "" or message.lower() == " ":
        continue

    replaced_msg = message.replace('$DESKTOP', '%USERPROFILE%\\Desktop')
    replaced_msg = replaced_msg.replace('$DOCUMENTS', '%USERPROFILE%\\Documents')

    client_socket.send(replaced_msg.encode())  # Send message to server

    try:
        response = client_socket.recv(1024).decode()  # Get answer from server
        print(response)
    except socket.timeout:
        print('{NO ANSWER FROM SERVER}')

# Close connection
client_socket.close()
