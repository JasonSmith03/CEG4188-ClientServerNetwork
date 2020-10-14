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
        if ("/create" in action):
            channelName = action[8:]
            #check if list already exists
            if channelName not in CONNECTIONLIST:
                #create the channel and add that user to the channel
                CONNECTIONLIST[channelName] = []
                CONNECTIONLIST[channelName].append((clientHost, userName))
                print("{} has created a new channel: {}\n".format(userName, channelName))
                #clientHost.send("You have created and have been added to the channel: {}".format(channelName))
                broadcast(channelName, "{} has joined the chat".format(userName))
                break
            #channel already exists, user needs to select a new action
        elif ("/join" in action):
            channelName = action[6:]
            #check to see if channel exists
            if channelName in CONNECTIONLIST:
                CONNECTIONLIST[channelName].append((clientHost, userName))
                print("{} has been added to the channel: {}\n".format(userName, channelName))
                #clientHost.send("You have joined channel: {}".format(channelName))
                broadcast(channelName, "{} has joined the chat".format(userName))
                break
            #channel does not exist, user needs to select new action
        elif ("/list" in action):
            #Display a list of all available channels
            clientHost.send("Available channels: {}".format(displayChannelList()))
            break
        #user did not enter correct action, repeat loop
    return userName

                
def start_conversation(clientHost, userName):
    '''
    This function handles message transaction between all users
    '''
    while True:
        message = clientHost.recv(BUFF_SIZE)
       
        #if the user decides to quit
        if ("/quit" in message):
            #This will exit the while loop
            #this should remove user from the channel and end the connection with the server
            #all users in the existing chat should be informed that the user has left

            #remove user from the old channel and inform everyone in the channel                 
            for key, value in CONNECTIONLIST.items():
                for user in value:
                    if(clientHost in user):
                        CONNECTIONLIST[key].remove(user)
                        broadcast(key, "{} has been removed from this channel".format(userName))
                        exit()

        #if the user decides to create and join a new channel
        elif ("/create" in message):
            #create the new channel and move the user to that new channel
            endOfCreate = message.find("/create", 0, len(message)-1) + 8
            newChannel = message[endOfCreate:]
            print("NEW CHANNEL: {}".format(newChannel))

            if newChannel not in CONNECTIONLIST:
                #remove user from the old channel and inform everyone in the channel                 
                for key, value in CONNECTIONLIST.items():
                    for user in value:
                        if(clientHost in user):
                            CONNECTIONLIST[key].remove(user)
                            broadcast(key, "{} has been removed from this channel".format(userName))

                #Create the new channel
                CONNECTIONLIST[newChannel] = []
                #Add userName to the new channel
                CONNECTIONLIST[newChannel].append((clientHost, userName))
                print("{} has been added to the channel: {}\n".format(userName, newChannel))
                broadcast(newChannel, "{} has joined the chat".format(userName))
            else:
                clientHost.send("Room {} already exists, so cannot be created".format(newChannel))
        #if the user decides to join a new channel
        elif ("/join" in message):
            #create the new channel and move the user to that new channel
            endOfJoin = message.find("/join", 0, len(message)-1) + 6
            newChannel = message[endOfJoin:]
            print("NEW CHANNEL: {}".format(newChannel))
            #check to see if channel exists
            if newChannel in CONNECTIONLIST:
                #remove user from the old channel and inform everyone in the channel                 
                for key, value in CONNECTIONLIST.items():
                    for user in value:
                        if(clientHost in user):
                            CONNECTIONLIST[key].remove(user)
                            broadcast(key, "{} has been removed from this channel".format(userName))

                #Add userName to the new channel
                CONNECTIONLIST[newChannel].append((clientHost, userName))
                print("{} has been added to the channel: {}\n".format(userName, newChannel))
                broadcast(newChannel, "{} has joined the chat".format(userName))

            #That channel does not exist, inform user
            else:
                clientHost.send("No channel named {} exists. Try '/create {}'?".format(newChannel, newChannel))
            
        #if the user decides to view the list of available channels
        elif ("/list" in message):
            clientHost.send("Available channels: {}".format(displayChannelList()))
        #The user has typed a normal message to the channel
        elif ("/" in message):
            clientHost.send("{} is not a valid control message. Valid messages are /create, /list, and /join.".format(message))
        else:
            for key, value in CONNECTIONLIST.items():
                for user in value:
                    if(clientHost in user):
                        channelName = key
                        #break
            broadcast(channelName, message)

    #user has quit the program

def broadcast(channelName, message):
    '''
    This message declares a new user in the chat to all existing users in that chat
    '''
    #Padding message to be 200 characters
    # counter = len(message)
    # if (counter < 200):
    #     diff = 200 - counter
    #     paddingString = len(message) + diff
    #     message = message.ljust(paddingString)
    
    #send message to each member in channel
    for key, value in CONNECTIONLIST.items():
        if (key == channelName):
            for user in value:
                user[0].send(message)

def displayChannelList():
    '''
        This method returns all the currently active channel lists
    '''
    channelList = ""
    for channelName in CONNECTIONLIST:
        channelList += (channelName + " ")
    return channelList


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

        userName = new_connection(clientHost)

        thread = threading.Thread(target=start_conversation, args=(clientHost, userName,))
        thread.start()

    #TODO   SERVERSOCKET.close()

if __name__ == "__main__":
    main()