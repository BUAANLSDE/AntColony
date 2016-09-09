__author__ = 'PC-LiNing'

from socket import *

address = ('',9000)
sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(address)

while True:
    data,addr = sock.recvfrom(8192)
    print(data)
    # send data
    sock.sendto(('Received %s bytes' % len(data)).encode(),addr)

sock.close()