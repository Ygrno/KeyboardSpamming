import struct
import time
from socket import *

Running = False
PLAYTIME = 10
UDPORT = 13117


def client_app():
    global Running, PLAYTIME
    Running = True
    print("Client - Side")
    client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    client_socket.bind(('', UDPORT))

    print("Looking for a Server:")
    # Client receive UDP message (cookie + offer type + TCP PORT)
    data, addr = client_socket.recvfrom(1024)

    print("server says:")
    print(addr)

    encode_data = struct.unpack('Ibh', data)
    print(encode_data)

    # Client Continues until he finds the right message
    while encode_data[0] != 0xFEEDBEEF:
        data, addr = client_socket.recvfrom(1024)
        encode_data = struct.unpack('Ibh', data)
        print(encode_data)

    client_socket.close()
    print("Received offer from - " + str(addr[0]) + " attempting to connect...")

    # now the client will try connection trough tcp with the TCP port he received from the server over UDP
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((addr[0], encode_data[2]))
    except:
        Running = False
        return

    # Client send his Team Name
    msg = "BitHackers2\n"
    client_socket.send(msg.encode('ascii'))

    # Client receive Welcome message:
    data = client_socket.recv(1024)
    print(data.decode('ascii'))

    t_end = time.time() + PLAYTIME + 5
    while time.time() < t_end:
        ans = input()
        client_socket.send(ans.encode('ascii'))

    # Client receive how many keys he typed
    data = client_socket.recv(40)
    print(data.decode('ascii'))
    # Client receive summary message
    data = client_socket.recv(1024)
    print(data.decode('ascii'))

    # client_socket.send(b'ok')
    client_socket.close()
    print("Server disconnected, listening for offer requests. . .\n")
    Running = False


while not Running:
    try:
        client_app()
    except:
        Running = False
    time.sleep(8)