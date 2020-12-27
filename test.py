from struct import *
data = pack('Ibh', 0xfeedbeef,0x2,13117)
print(data)
print(unpack('Ibh',data))
print(calcsize('Ibh'))
