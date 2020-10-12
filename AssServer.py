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

clientList = [] #client connection nothing to do with channel
channelList = [] #list of channels nothing to do with client
channelDict = {"lobby" : clientList} #key is the channel name, value is the list of client connections


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
        connection.send("Welcome {} select /join <channel>, /create <channel>, or /list".format(data))

        message = connection.recv(BUFF_SIZE)
        if(message[:5] == "/join"):
            #join a channel with user input
            channelName = message[6:]
            if(channelName in channelList):
                channelDict['lobby'] = channelName #finds the specified channel name
                channelDict[clientList] = clientList.append(connection) #adds a user into that channel
                break
            connection.send("channel name does not exist")
        elif(message[:7] == "/create"):
            #create a channel with user input
            if(message[8:] not in channelList):
                channelList.append(message[8:])
                break
            connection.send("Channel already exists. Type /list to see all channel or /join <channel>")
        elif(message[:5] == "/list"):
            #list all the channels
            print '[%s]' % ', '.join(map(str, channelList))
    connection.close()

def listenForMessage():
    '''
    This method listens for clients to connect and then awaits
    to reveiver either a control message or a normal message. 
    This method should first check to see if there is a message
    from a particular user, if message is blank then remove from channel.
    '''
    pass

def initConn():
    '''
    User to decide if they want to create, join, or list channels on the server.
    '''
    pass


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
        client, address = server_socket.accept()
        THREAD_COUNT+=1
        print ("Thread count: {}".format(THREAD_COUNT))
        thread = threading.Thread(target=client_thread(client))
        thread.start()
        thread.join()
    server_socket.close()


if __name__ == "__main__":
    main()