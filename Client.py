import struct
from socket import * 

print("client")
c_s = socket(AF_INET, SOCK_DGRAM,IPPROTO_UDP)
c_s.bind(('',13117))
#c_s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  
c_s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  
data,addr = c_s.recvfrom(1024)
print("server says:")
print(addr)
print(struct.unpack('Ibh', data))
c_s.clos