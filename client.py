#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Client application for chat messaging

import socket
import select
import errno
from pip._vendor.distlib.compat import raw_input
import sys

# serverName = "servername"
# serverPort = 12000
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket.connect(("127.0.0.1",serverPort))
# sentence = raw_input("Input lowercase sentence:")
# clientSocket.send(sentence.encode())
# modifiedSentence = clientSocket.recv(1024)
# print ("From Server:", modifiedSentence.decode())
# clientSocket.close()

HEADER_LENGTH = 10
ip = socket.gethostname()
port = 8080

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):< {HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            # receive messages
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error", str(e))
        sys.exit()




