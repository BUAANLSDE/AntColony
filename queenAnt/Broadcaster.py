__author__ = 'PC-LiNing'

from socket import *
import time
import multiprocessing
import util
import affairProcess
import json
from multiprocessing import Manager

# signal
Start_Recovery = 'recovery start'
End_Recovery = 'recovery end'
Next_Block = 'next block'

No_FollowUp = 'no_follow_up'

# constant
Waiting_time_each_round = 10  # Waiting time for each round of voting , 10 seconds
Worken_port = 9000
NODES_FILE = 'nodes-list'

# data format:
# 1 round :  Start_Recovery
# 2 round :  {current_block_id: block_id}
# ...
# last round : End_Recovery

class QueenServer():

    # udp client to send data to all nodes.
    # udp server to receive data from all nodes.this make it easy.
    def __init__(self,host=None,port=9000):
        # init udp client , udp server
        self._host = host
        self._port = port
        sock_server = socket(AF_INET,SOCK_DGRAM)
        address = (self._host,self._port)
        sock_server.bind(address)
        self._socketserver = sock_server

        sock_client = socket(AF_INET,SOCK_DGRAM)
        self._socketclient =  sock_client
        #  next request block
        self._current_block_id = multiprocessing.Array('c',64,lock=multiprocessing.Lock())
        # node public key
        self._nodes_keyring = Manager().list()
        # nodes info
        self._address_list = util.read_nodes(NODES_FILE)
        self._publickey_list = []
        # receive data
        self._receive_data = multiprocessing.Queue()

    def close_Server(self):
        self._socketserver.close()

    # send data to a group of address
    def send_to_nodes(self,data):
        address = ('10.2.1.35', 9000)
        self._socketclient.connect(address)
        # data is dict
        self._socketclient.sendto(json.dumps(data).encode(),address)

    # receive process
    def receiver(self):
        print('receiver start .')
        while True:
            data,addr = self._socketserver.recvfrom(8192)
            print('%s: got %r' % (addr[0], data))
            # current_time = time.time()
            # self._receive_data.put((current_time,data,addr))
            self._receive_data.put(data)

    # vote process
    def voter(self):
        print('voter start .')
        print('received data number: '+str(self._receive_data.qsize()))
        received_list = util.convert_to_list(self._receive_data)
        # TODO: if some mistakes happen,nodes public key not init .
        if not self._nodes_keyring :
            temp_keys=affairProcess.init_publickey_list(receive_list=received_list,address_list=self._address_list)
            for one in temp_keys:
                self._nodes_keyring.append(one)

        verify_list = affairProcess.verifynodes(received_list,self._current_block_id.value.decode('utf-8'),self._nodes_keyring)
        voted_block,voted_vote = affairProcess.vote(verify_list,len(self._address_list))
        print('voted_vote : ')
        print(voted_vote)
        # next block
        if voted_vote == No_FollowUp :
            self._current_block_id.value = 'STOP'.encode()
            print('voted_vote: '+voted_vote)
        else:
            self._current_block_id.value = json.loads(voted_vote)['vote']['voting_for_block'].encode()
            print('voted_vote: '+json.loads(voted_vote)['vote']['voting_for_block'])
        print('voted_block: '+json.loads(voted_block)['id'])
        print('current block id : ')
        print(self._current_block_id.value.decode('utf-8'))


    # main process
    # one round : send request -- receiver response ---vote
    # send data format :
    # 1 round : { type : Start_Recovery,current_block_id : block id}
    # middle round : {type : Next_Block,current_block_id : block id}
    # last round : {type : End_Recovery,current_block_id : 'STOP'}
    def start(self):
        end = False
        self._current_block_id.value = 'genesis'.encode()
        send_data ={'type':Start_Recovery,'current_block_id':self._current_block_id.value.decode('utf-8')}
        # start recovery
        while True:
            # clear queue
            self._receive_data.empty()
            # send request
            self.send_to_nodes(send_data)
            if end:
                return
            receiver = multiprocessing.Process(name='receiver',target=self.receiver)
            receiver.start()
            receiver.join(Waiting_time_each_round)
            # kill
            if receiver.is_alive():
                print("receiver timeout.")
                receiver.terminate()
                receiver.join()

            voter = multiprocessing.Process(name='voter',target=self.voter)
            voter.start()
            voter.join()
            if self._current_block_id.value.decode('utf-8') == 'STOP':
                send_data = {'type':End_Recovery,'current_block_id':'STOP'}
                end = True
            else:
                # next round send_data
                print('send data : ')
                print(self._current_block_id.value.decode('utf-8'))
                send_data = {'type':Next_Block,'current_block_id':self._current_block_id.value.decode('utf-8')}


if __name__ == '__main__':
    # get local ip
    local_ip = util.get_ip('eth0')
    print('start Broadcaster server on %s:9000' % local_ip)
    QueenServer(host=local_ip,port=9000).start()
