import struct, time
from socket import * 

server_socket = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  
server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  
server_socket.settimeout(0.2)
msg = struct.pack('Ibh', 0xfeedbeef,0x2,30546)
while True:
    print("server listening . . .")
    server_socket.sendto(msg,('<broadcast>',13117))
    time.sleep(1)

