__author__ = 'PC-LiNing'

import socket, struct, fcntl

# get current node ip
def get_ip(iface = 'eth0'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd = sock.fileno()
    SIOCGIFADDR = 0x8915
    ifreq = struct.pack('16sH14s', iface.encode('utf-8'), socket.AF_INET, b'\x00'*14)
    try:
        res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
        return None
    ip = struct.unpack('16sH2x4s8x', res)[2]
    return socket.inet_ntoa(ip)


# each line is a node's ip
def read_nodes(nodes_file):
    nodes_list = []
    nodes = open(nodes_file)
    for line in nodes.readlines():
        nodes_list.append(line.strip('\n'))
    return nodes_list

# print(read_nodes('nodes-list'))