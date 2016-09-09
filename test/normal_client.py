__author__ = 'PC-LiNing'

import sys
from socket import *

address = ('localhost', 9000)
message = ' '.join(sys.argv[1:])

sock=socket(AF_INET,SOCK_DGRAM)

sock.connect(address)
print('Sending %s bytes to %s:%s' % ((len(message), ) + address))
sock.sendto(message.encode(),address)

data, address = sock.recvfrom(8192)
print('%s:%s: got %r' % (address + (data, )))