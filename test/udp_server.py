__author__ = 'PC-LiNing'

from gevent.server import DatagramServer
import time

class EchoServer(DatagramServer):

    def closeServer(self):
        super().close()

    def handle(self, data, address): # pylint:disable=method-hidden
        print('%s: got %r' % (address[0], data))
        self.socket.sendto(('Received %s bytes' % len(data)).encode('utf-8'), address)
        print("5s later close the server .")
        time.sleep(5)
        self.closeServer()

if __name__ == '__main__':
    print('Receiving datagrams on :9000')
    server = EchoServer(':9000')
    # server.serve_forever()
    server.start()