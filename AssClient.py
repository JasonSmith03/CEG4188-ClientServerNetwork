import socket
import threading
import sys

# Listening to Server and Sending Nickname
def receive(client, nickname):
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


# Sending Messages To Server
def write(client, nickname):
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))


def main():
    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((sys.argv[2], int(sys.argv[3])))

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive(client, sys.argv[1]))
    receive_thread.start()

    write_thread = threading.Thread(target=write(client, sys.argv[1]))
    write_thread.start()


if __name__ == "__main__":
    main()