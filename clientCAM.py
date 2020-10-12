#Cameron Dey(300043455), Mourad Elmofty(300005506)
import socket
import threading
import sys

#Server port and Name
serverName = '127.0.0.1'
serverPort = 55555

try:
	if(sys.argv[1]!=""):
		print("\n\nPLEASE DO NOT ENTER ARGUMENTS.YOU JUST NEED TO RUN THE FILE\n\n")
		exit(1)
except:
	pass

#Create client socket and prompts user for username
clientSocket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
awk = clientSocket.recv(1024).decode()
print(awk)
username = raw_input('UserName: ')
clientSocket.send(username.encode())


#Initial interaction to create, join, or list channels
message = clientSocket.recv(1024).decode()
print(message)
channel = raw_input(">")
clientSocket.send(channel.encode())
chanSelect = clientSocket.recv(1024).decode()

#Loop in case client enters an invlaid command
while chanSelect != "ok ":
	print(chanSelect)
	channel = raw_input(">")
	clientSocket.send(channel.encode())
	chanSelect = clientSocket.recv(1024).decode()
	



chanSelect = clientSocket.recv(1024).decode()
print(chanSelect)
	

#Method to recieve messages
def receive():
	counter = 0
	while True:
		
		message = clientSocket.recv(1024).decode()
		print(message)
		if message =="":
			counter = counter + 1
			if counter==10:
				print("Server at ("+str(serverName)+"):("+str(serverPort)+") has disconnected")
				sys.exit()

#Method to send messages
def send():
	while True:
		message = raw_input(">")
		message = (message + " " + "("+username+")")
		clientSocket.send(message.encode())


#threads to run different clients in parallel
receiveThread = threading.Thread(target=receive)
sendThread = threading.Thread(target=send)
receiveThread.start()
sendThread.start()




