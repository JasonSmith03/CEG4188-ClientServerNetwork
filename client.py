#Authors: Jason Smith, Bradley Rose
#October 13, 2020
#Client application for chat messaging

import socket
import threading
import sys

#Global variables
BUFF_SIZE = 2048
#argv[0] - script name
USERNAME = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def firstAction():
    #client selects action and tells server
    action = raw_input(">")
    CLIENTSOCKET.send(action)

    #client receives confirmation from server
    serverResponse = CLIENTSOCKET.recv(BUFF_SIZE)
    print(serverResponse)
    # serverResponse = CLIENTSOCKET.recv(BUFF_SIZE)
    # print(serverResponse)

#Method to recieve messages
def receive(client_socket):
    while True:
        message = client_socket.recv(BUFF_SIZE)
        print(message)

#Method to send messages
def write(client_socket, clientName):
    while True:
        message = raw_input(">")
        message = ("[" + clientName + "]: " + message)
        client_socket.send(message)

def main():
    #connect user to server and send username
    CLIENTSOCKET.connect((HOST, PORT))
    CLIENTSOCKET.send(USERNAME)

    #Receive welcome statement from server
    serverResponse = CLIENTSOCKET.recv(BUFF_SIZE)
    print(serverResponse)

    #User chooses first action
    firstAction()
    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive, args=(CLIENTSOCKET,))
    write_thread = threading.Thread(target=write, args=(CLIENTSOCKET, USERNAME))
    receive_thread.start()
    write_thread.start()

    #TODO CLIENTSOCKET.close()

if __name__ == "__main__":
    main()