#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Server application for chat messaging

import socket
import select

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


HEADER_LENGTH = 10
ip = socket.gethostname() #get local machine name
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((ip, port))
server_socket.listen(5)

sockets_list = [server_socket]
clients = {}

while True:
    read_sockets, _, exception_socket = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print(f"Closed Connection from {clients[notified_socket]['data'].decode('utf-8')}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                user = clients[notified_socket]
                print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_socket:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]



# while True:
#     conn, addr = server_socket.accept()
#     from_client = ""
#
#     while True:
#         data = conn.recv(4096)
#         if not data: break
#         from_client += data
#         print(from_client)
#
#         conn.send("I am SERVER \n")
#     conn.close()
#     print("client disconnected")


