import struct
import time
from socket import *

Running = False


def client_app():
    global Running
    Running = True
    print("Client - Side")
    client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    client_socket.bind(('', 13117))

    print("Looking for a Server:")
    data, addr = client_socket.recvfrom(1024)

    print("server says:")
    print(addr)

    encode_data = struct.unpack('Ibh', data)
    print(encode_data)

    while encode_data[0] != 0xFEEDBEEF:
        data, addr = client_socket.recvfrom(1024)
        encode_data = struct.unpack('Ibh', data)
        print(encode_data)

    client_socket.close()
    print("Received offer from - " + str(addr[0]) + " attempting to connect...")

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((addr[0], encode_data[2]))

    msg = "BitHackers4\n"
    client_socket.send(msg.encode('ascii'))
    data = client_socket.recv(1024)
    print(data.decode('ascii'))
    client_socket.send(b'ok')
    data = client_socket.recv(4)
    print(data)

    while True:
        if data == b'n':
            break
        ans = input()
        client_socket.send(ans.encode('ascii'))
        data = client_socket.recv(1)
        print(data)

    client_socket.send(b'ok')
    data = client_socket.recv(40)
    print(data.decode('ascii'))
    data = client_socket.recv(1024)
    print(data.decode('ascii'))
    client_socket.send(b'ok')
    client_socket.close()
    print("Server disconnected, listening for offer requests. . .")
    Running = False


while not Running:
    client_app()
    time.sleep(5)





