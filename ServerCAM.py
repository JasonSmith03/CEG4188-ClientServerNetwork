#Cameron Dey(300043455), Mourad Elmofty(300005506)
import socket
import select
import sys
import threading


#Global Variables
serverName = '127.0.0.1' #Server set to local host 
serverPort = 55555 #Server port 
sockets = [] #List of the socket connections made by the clients
clients = [] #List of client names connected to server
channels = [] #List of active channels
users = {} #Dictionaty of client names and the channels they're connected to

#Initilize the server socket connection 
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((serverName,serverPort))
serverSocket.listen(10)

print("Server is active")

	
#Method for receiving messges from clients after they've chosen a Username & Channel
def receive(connection):
	while True:
		
		message = connection.recv(1024).decode()
		index = sockets.index(connection)
		client = clients[index]
		channel = users[client]
		try:
			#Checks to see if a server command is sent
			if message[0] == "/":
				newMessage = message.replace("/","")
				newMessage = newMessage.replace(" ","")
				clientInfo = ("("+client+")")
				newMessage = newMessage.replace(clientInfo,"")
				
				#Handles "Join" Command
				if "join" in newMessage:
					newMessage = newMessage.replace("join","")

					if newMessage == "":
						error = "/join command must be followed by the name of a channel to join."
						connection.send(error.encode())

					elif newMessage in channels:
						message = (client + "has left the channel")
						multicast(message,users[client],client)
						users[client] = newMessage
						joined = ("You are now in Channel "+newMessage)
						connection.send(joined.encode())
						message = (client + " has joined the channel")
						multicast(message,users[client],client)
					else:
						error = ("No channel named "+newMessage+ " exists.")
						connection.send(error.encode())

				#Handles Create Command
				elif "create" in newMessage:
					newMessage = newMessage.replace('create',"")

					if newMessage == "":
						error = "/create command must be followed by the name of a channel to create"
						connection.send(error.encode())

					elif newMessage in channels:
						error = ("Channel "+newMessage+ " already exists, so cannot be created.")
						connection.send(error.encode())

					else:
						message = (client + " has left the channel")
						multicast(message,users[client],client)
						channels.append(newMessage)
						users[client] = newMessage
						joined = ("You are now in Channel "+ newMessage)
						connection.send(joined.encode())

				#Handles List Command
				elif "list" in newMessage:
					channel_list = ""
					for i in range(len(channels)):
						channel_list = (channel_list + channels[i]+"\n")
					connection.send(channel_list.encode())
				else: 
					error = ("Invalid entry")
					connection.send(error.encode())

			#Broadcasts a messge to whoever is in the Channel
			else:
				multicast(message,channel,client)

		#Exception to check if the client thread has disconnected. 
		except:
			disconnect = (client + " has disconnected")
			multicast(disconnect,channel,client)
			sockets.remove(connection)
			clients.remove(client)
			del users[client]
			break

#Method to handle new Client connections to the server
def newConnection():
	while True:

		#Handles intial connection and interaction with the client
		connection, address =  serverSocket.accept()
		welcome = "Welcome to the ChatBot"
		connection.send(welcome.encode())
		client = connection.recv(1024).decode()
		clients.append(client)
		sockets.append(connection)


		chanSelect = ("Create, Join, or List a Channel (0-9): ")
		chanMessage = connection.send(chanSelect.encode())
		
		#While loop to check for valid commands to join, create, or list channels
		while True:
			chanResponse = connection.recv(1024).decode()
			chanResponse = chanResponse.lower()
			
			error = ("Not currently in any channel. Must join a channel before sending messages.")
			if chanResponse[0] != "/":
				connection.send(error.encode())

			#Handles the 'list' command
			elif chanResponse == "/list":
				if len(channels) == 0:
					noChannel = ("There are no Active Channels")
					connection.send(noChannel.encode())
				else:
					channel_list = ""
					for i in range(len(channels)):
						channel_list = (channel_list + channels[i]+"\n")
					connection.send(channel_list.encode())

			#Handles the 'join' command
			elif "/join" in chanResponse:
				chanResponse = chanResponse.replace("/join","")
				chanResponse = chanResponse.replace(" ","")

				if chanResponse == "":
					error = "/join command must be followed by the name of a channel to create"
					connection.send(error.encode())


				elif chanResponse in channels:
					users[client] = chanResponse
					valid = ("ok ")
					joined = ("You are now in Channel "+chanResponse)

					connection.send(valid.encode())
					connection.send(joined.encode())
					message = (client + " has joined the channel")
					multicast(message,users[client],client)
					break
				else:
					error = "No channel named "+chanResponse+ " exists."
					connection.send(error.encode())

			#Handles the 'create' command
			elif "/create" in chanResponse:
				chanResponse = chanResponse.replace("/create","")
				chanResponse = chanResponse.replace(" ","")

				if chanResponse == "":
					error = "/create command must be followed by the name of a channel to create"
					connection.send(error.encode())

				elif chanResponse in channels:
					invalid = ("Channel "+chanResponse+ " already exists, so cannot be created.")
					connection.send(invalid.encode())
				else:
					channels.append(chanResponse)
					users[client] = chanResponse
					valid = ("ok ")
					joined = ("You are now in Channel "+ chanResponse)
					connection.send(valid.encode())
					connection.send(joined.encode())
					break
			#Sends message if not valid
			else:
				error = chanResponse+ " is not a valid control message. Valid messages are /create, /list, and /join."
				connection.send(error.encode())

		thread = threading.Thread(target=receive, args=(connection,))
		thread.start()
	
#Method used to braodcast a message to every client connected to a specific channel
def multicast(message,channel,client):
	for i in users.keys():
		temp = users[i]
		if temp == channel:
			index = clients.index(i)
			connection = sockets[index]
			if i == client:
				continue
			else:
				connection.send(message.encode())




newConnection()





 

