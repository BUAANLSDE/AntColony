__author__ = 'PC-LiNing'

from gevent.server import DatagramServer

# signal
Start_Recovery = 'recovery start'
End_Recovery = 'recovery end'

class WorkenServer(DatagramServer):

    def __init__(self, *args, **kwargs):
        DatagramServer.__init__(self, *args, **kwargs)
        self._queen = None
        self._startflag = False

    def initial_bind_queen(self,addr):
        self._queen=(addr[0],9000)
        self._startflag=True

    # send data
    def send_to_queen(self,data):
        print(self._queen)
        self.socket.sendto(data.encode(),self._queen)

    def handle(self, data, address):
        content = data.decode("utf-8")
        print('%s:%s: got %r' % (address + (data, )))
        if content == Start_Recovery and self._startflag==False:
            # bind queen , return genesis block id
            # when first communicate, node send it's public key , gensis block id to center node.
            self.initial_bind_queen(address)
            self.send_to_queen('gensisi block id')
            print('start recovery.')
        elif content == End_Recovery:
            # end
            print('end recovery.')
            self.socket.close()
        else:
            print('send next block.')


if __name__ == '__main__':
    print('Receiving datagrams on localhost:9000')
    # bind localhost
    WorkenServer(':9000').serve_forever()