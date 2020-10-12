#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Server application for chat messaging

import socket
import threading
import sys

PORT = 55555
HOST = 'localhost'
BUFF_SIZE = 2048
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

channelList = [] #list of channels nothing to do with client
channelDict = {} #key is the channel name, value is the list of client connections


def client_thread(connection):
    '''
    Receives client information such as name, IP, and port number.
    Then sends a welcome message to the client to verify they are connected
    '''
    while True:
        clientName = connection.recv(BUFF_SIZE)
        if not clientName:
            break
        print("new user: {}".format(clientName))
        connection.send("Welcome {} select /join <channel>, /create <channel>, or /list".format(clientName))
        message = connection.recv(BUFF_SIZE)
        if not message:
            break
        if(message[:5] == "/join"):
            #join a channel with user input
            if(message[6:] in channelList):
                channelDict[message[6:]].append(clientName) #append the client name to that channel
                break
            connection.send("Channel name does not exist")
        elif(message[:7] == "/create"):
            #create a channel with user input
            if(message[8:] not in channelList):
                channelList.append(message[8:])
                server_socket.send("Connected to: {}".format(message[8:]))
                channelDict[message[8:]] = [] #create new key - channel, the value - empty list
                channelDict[message[8:]].append(clientName) #append the client name to that channel
                break
            connection.send("Channel already exists. Type /list to see all channel or /join <channel>")
        elif(message[:5] == "/list"):
            #list all the channels
            print '[%s]' % ', '.join(map(str, channelList)) #TODO make this a send
    print(channelList)
    #connection.close()


def main():
    #show the socket and the port bind
    try: 
        server_socket.bind((HOST, PORT)) 
        print ("socket binded to port: {}".format(PORT))
    except socket.error as e:
        print(e)
    server_socket.listen(5) 
    print ("socket is listening\n")
    
    THREAD_COUNT = 0

    while True:
        client, address = server_socket.accept() # returns (host, port)
        print(client, address)
        THREAD_COUNT+=1
        print ("Thread count: {}".format(THREAD_COUNT))
        thread = threading.Thread(target=client_thread(client))
        thread.start()
        print("we back bitches")
        #thread.join()
        print("lets get er goin baud")
    server_socket.close()


if __name__ == "__main__":
    main()