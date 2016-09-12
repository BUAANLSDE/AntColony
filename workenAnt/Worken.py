__author__ = 'PC-LiNing'

from gevent.server import DatagramServer
import leveldb
import json

# signal
Start_Recovery = 'recovery start'
End_Recovery = 'recovery end'
Next_Block = 'next block'

No_FollowUp = 'no_follow_up'


# data format:
# 1 round :  {pub_key: public key,signature:signature,genesis_block:block ,host:node ip}
# 2 round :  {pub_key: public key,signature:signature,next_block:block[None],related_vote:vote[None]}
# ...
# last round : workenAnt close.

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

    # close server
    def closeServer(self):
        super().close()

    def handle(self, data, address):
        content = json.loads(data.decode("utf-8"))
        print('%s:%s: got %r' % (address + (data, )))
        if content['type'] == Start_Recovery and self._startflag==False:
            # bind queen , return genesis block id
            # when first communicate, node send it's public key , gensis block id to center node.
            print('start recovery.')
            self.initial_bind_queen(address)
            # self.send_to_queen('gensisi block id')
            self.send_to_queen(leveldb.get_start_data())
        elif content['type'] == End_Recovery:
            # end
            print('end recovery.')
            self.socket.close()
            self.closeServer()
            return
        elif content['type'] == Next_Block :
            block_id = content['current_block_id']
            self.send_to_queen(leveldb.get_response_data(current_block_id=block_id))
            print('send next block.')

if __name__ == '__main__':
    print('Receiving datagrams on localhost:9000')
    # bind localhost
    server = WorkenServer(':9000')
    server.serve_forever()