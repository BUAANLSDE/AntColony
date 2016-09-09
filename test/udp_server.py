__author__ = 'PC-LiNing'

from gevent.server import DatagramServer

class EchoServer(DatagramServer):

    def handle(self, data, address): # pylint:disable=method-hidden
        print('%s: got %r' % (address[0], data))
        self.socket.sendto(('Received %s bytes' % len(data)).encode('utf-8'), address)

if __name__ == '__main__':
    print('Receiving datagrams on :9000')
    EchoServer(':9000').serve_forever()