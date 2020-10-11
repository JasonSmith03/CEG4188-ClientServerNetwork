import socket
import threading
import sys

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server and listen for connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

# Lists For Clients and Their Nicknames
names = '' #
connections = {} #dictionary wehre the key is the socket - value is [address, name, channel]
channels = {"lobby" : []} #dictionary where key is the channel name - value is list of channels

def listenForUser():
    '''
    This method listens for clients to connect and then awaits
    to reveiver either a control message or a normal message. 
    This method should first check to see if there is a message
    from a particular user, if message is blank then remove from channel.
    '''
    while True: 
        #address is a tupple with an IP and PORT number, connection is a long stream of connection information
        connection, address = server.accept() # accepts a connection
        print("Connected with {}".format(str(address)))
        print("Accepted connection {}".format(str(connection)))

        # Request And Store Nickname in connections dictionary
        connection.send('NICK'.encode('utf-8'))
        name = connection.recv(1024).decode('utf-8')


def broadcast(message):
    '''
    This method broadcasts a message to clients that are found 
    on the same channel. Use dictionary to find which user is part
    of which channel and broadcast to them. 
    '''


def main():
    listenForUser()


if __name__ == "__main__":
    main()