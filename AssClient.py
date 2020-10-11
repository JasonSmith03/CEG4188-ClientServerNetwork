import socket
import threading
import sys

# Listening to Server and Sending Nickname
def receive(client, clientName):
    while True:
        try:
            # Receive Message From Server
            serverResponse = client.recv(2048)
            client.send(clientName.encode('utf-8'))
            print(serverResponse)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write(client, clientName):
    while True:
        message = '{}: {}'.format(clientName, input(''))
        client.send(message.encode('utf-8'))


def main():
    #argv[0] - script name
    clientName = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print ("\nConnected to server at \nHost: {} \nPort: {}\n".format(host, port))
    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive(client, clientName))
    receive_thread.start()

    write_thread = threading.Thread(target=write(client, clientName))
    write_thread.start()


if __name__ == "__main__":
    main()