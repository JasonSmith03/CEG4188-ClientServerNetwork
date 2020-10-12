#Authors: Jason Smith, Bradley Rose
#October 13, 2020
#Client application for chat messaging

import socket
import threading
import sys

BUFF_SIZE = 2048
#argv[0] - script name
clientName = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

#Method to recieve messages
def receive(client_socket):
	counter = 0
	while True:
		
		message = client_socket.recv(1024).decode()
		print(message)

#Method to send messages
def write(client_socket, clientName):
	while True:
		message = raw_input(">")
		message = ("[" + clientName + "]: " + message)
		client_socket.send(message.encode())

#Method to allow user to send an first message
def initInteraction(client_socket):
    message = client_socket.recv(BUFF_SIZE)
    print message
    channel = raw_input(">")
    client_socket.send(channel)
    select_channel = client_socket.recv(BUFF_SIZE)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print ("\nConnected to server at \nHost: {} \nPort: {}\n".format(host, port))
    client_socket.send(clientName)
    serverResponse = client_socket.recv(BUFF_SIZE)
    print(serverResponse) #welcome <user>
    
    initInteraction(client_socket)

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive, args=(client_socket,))
    write_thread = threading.Thread(target=write, args=(client_socket, clientName))
    receive_thread.start()
    write_thread.start()


    client_socket.close()


if __name__ == "__main__":
    main()