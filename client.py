#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Client application for chat messaging

import socket

# The socket constructor accepts a few arguments; the defaults are fine for this class.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() #get local machine name
port = 8080

client_socket.connect((host, port))
#client_socket.send("Hello World \n")

from_server = client_socket.recv(4096)

client_socket.close()
print(from_server)



