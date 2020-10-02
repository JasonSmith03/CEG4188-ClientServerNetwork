#Authors: Jason Smith, Bradley Rose
#October 7, 2020
#Server application for chat messaging

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() #get local machine name
port = 8080
server_socket.bind((host, port))
server_socket.listen(5)

while True:
    conn, addr = server_socket.accept()
    from_client = ""

    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data
        print(from_client)

        conn.send("I am SERVER \n")
    conn.close()
    print("client disconnected")


