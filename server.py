#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Server application for chat messaging

import socket
import threading
import sys

PORT = 55555
HOST = 'localhost'
BUFF_SIZE = 2048



def client_thread(connection):
    '''
    Receives client information such as name, IP, and port number.
    Then sends a welcome message to the client to verify they are connected
    '''
    while True:
        data = connection.recv(BUFF_SIZE)
        if not data:
            break
        print("new user: {}".format(data))
        connection.send("Welcome {}".format(data))
    connection.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#show the socket and the port bind
try: 
    s.bind((HOST, PORT)) 
    print ("socket binded to port: {}".format(PORT))
except socket.error as e:
    print(e)
s.listen(5) 
print ("socket is listening\n")

def listenForMessage():
    '''
    This method listens for clients to connect and then awaits
    to reveiver either a control message or a normal message. 
    This method should first check to see if there is a message
    from a particular user, if message is blank then remove from channel.
    '''
    THREAD_COUNT = 0

    while True:
        client, address = s.accept()
        thread = threading.Thread()
        thread.start()
        THREAD_COUNT+=1
        print ("Thread count: {}".format(THREAD_COUNT))
        client_thread(client)
        #thread = threading.Thread(target=write(client, clientName))
        #thread.start()

def main():
    listenForMessage()
    s.close()


if __name__ == "__main__":
    main()