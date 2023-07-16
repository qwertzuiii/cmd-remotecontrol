import socket
import os
import sys

default_port = 1823

def read_config(filename="config.ini"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            cfgdata = f.read()
        return cfgdata
    else:
        print('An error occurred: [config.ini] Not existing')
        sys.exit()


def split_config(data):
    return data.split('^')


# Set host and port
def cmd_argscheck():
    # Check if using args
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
        if len(sys.argv) > 2:
            try:
                PORT = int(sys.argv[2])
            except ValueError:
                print('An error occurred: [ValueError] Port is not an integer')
                sys.exit()
        else:
            PORT = default_port
    else:
        config = read_config()
        config = split_config(config)

        HOST = config[0]  # Set IP
        PORT = int(config[1])  # Set Port

def init(host, port):
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to server
    client_socket.connect((host, port))
    #print('Connected to server:', host, port)

    # Set timeout
    client_socket.settimeout(5)

    # Check if autostart
    if os.path.exists('_autostart.ini'):
        autostart = True
        autostart_string = open("_autostart.ini", 'r').read()
    else:
        autostart = False


    # Send data
    while True:
        if not autostart:
            message = input('{}:{} @ '.format(str(host), str(port)))
        elif autostart:
            message = autostart_string
            autostart = False

        if message.lower() == 'exit' or message.lower() == 'q':
            break
        if ";socket.timeout" in message.lower():
            socket_timeout = float(input('SOCKET.TIMEOUT = '))
            client_socket.settimeout(socket_timeout)
            continue
        if message.lower() == 'cls' or message.lower() == 'clear':
            os.system('cls')
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
