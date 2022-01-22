import socket

SERVER_ADDRESS = ('localhost', 8000)

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(SERVER_ADDRESS)
serv_sock.listen(10)
print('server is running, please, press ctrl+c to stop')

while True:
    client_sock, client_addr = serv_sock.accept()

    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(data)
        

    client_sock.close()