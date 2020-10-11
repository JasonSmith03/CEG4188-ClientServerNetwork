#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Client application for chat messaging

import socket
import threading
import sys

BUFF_SIZE = 2048

#argv[0] - script name
clientName = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print ("\nConnected to server at \nHost: {} \nPort: {}\n".format(host, port))
client_socket.send(clientName)
serverResponse = client_socket.recv(BUFF_SIZE)
print(serverResponse)
client_socket.close()