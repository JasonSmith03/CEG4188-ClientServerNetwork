#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Server application for chat messaging

import socket
import threading
import sys

#Global Variables
PORT = 55555
HOST = 'localhost'
BUFF_SIZE = 2048
SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONNECTIONLIST = {} #key = channel names, value = usernames


def new_connection(clientHost):
    '''
        Welcomes the client and asks to choose among a list of actions
    '''
    #receive username from client
    userName = clientHost.recv(BUFF_SIZE)
    print("New user: {}\n".format(userName))

    #TODO   CHECK IF USERNAME HAS ALREADY BEEN TAKEN
    

    clientHost.send("Welcome {}, thank you for joining our chat service.\n".format(userName))
    #loop breaks when user selects one of the listed actions
    while True:
        #send welcome message and list of actions to client
        clientHost.send("\nPlease select one of the following options: \n/create <channel>, /join <channel>, or /list \n")
        #perform action based on user respronse
        action = clientHost.recv(BUFF_SIZE)
        if (action[:7] == "/create"):
            channelName = action[8:]
            #check if list already exists
            if channelName not in CONNECTIONLIST:
                #create the channel and add that user to the channel
                CONNECTIONLIST[channelName] = []
                CONNECTIONLIST[channelName].append((clientHost, userName))
                print("{} has created a new channel: {}".format(userName, channelName))
                #clientHost.send("You have created and have been added to the channel: {}".format(channelName))
                broadcast(channelName, "{} has joined the chat".format(userName))
                print("THIS IS CONNECTIONLIST: {}".format(CONNECTIONLIST))
                break
            #channel already exists, user needs to select a new action
        elif (action[:5] == "/join"):
            channelName = action[6:]
            #check to see if channel exists
            if channelName in CONNECTIONLIST:
                CONNECTIONLIST[channelName].append((clientHost, userName))
                print("{} has been added to the channel: {}".format(userName, channelName))
                #clientHost.send("You have joined channel: {}".format(channelName))
                broadcast(channelName, "{} has joined the chat".format(userName))
                print("THIS IS CONNECTIONLIST: {}".format(CONNECTIONLIST))
                break
            #channel does not exist, user needs to select new action
        elif (action[:5] == "/list"):
            #Display a list of all available channels
            channelList = ""
            for channelName in CONNECTIONLIST:
                channelList += (channelName + " ")
            clientHost.send(channelList)
            break
        #user did not enter correct action, repeat loop

def broadcast(channelName, message):
    '''
        This message declares a new user in the chat to all existing users in that chat
    '''
    #send message to each member in channel
    for key, value in CONNECTIONLIST.items():
        if (key == channelName):
            for user in value:
                user[0].send(message)
                #print(user[0])
                
def start_conversation(clientHost):
    '''
        This function handles message transaction between all users
    '''
    pass


def main():
    #initalize server
    try: 
        SERVERSOCKET.bind((HOST, PORT)) 
    except socket.error as e:
        print(e)
    SERVERSOCKET.listen(5) 
    print("server is ready and listenting on {} : {}\n".format(HOST, PORT))

    while True:
        #accept connection requests from client(s)
        clientHost, clientPort = SERVERSOCKET.accept() # returns (host, port)
        #thread = threading.Thread(target=new_connection(clientHost, clientPort))
        #thread.start()
        new_connection(clientHost)

        #print to server the list of channels and all users in those channels
        print(CONNECTIONLIST)

        # thread = threading.Thread(target=start_conversation, args=(clientHost))
        # thread.start()
        print("testing: end of thread")
        #thread.join()

if __name__ == "__main__":
    main()
