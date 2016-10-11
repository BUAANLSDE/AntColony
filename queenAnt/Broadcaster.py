__author__ = 'PC-LiNing'

from socket import *
import time
import multiprocessing
import util
import affairProcess
import json
from multiprocessing import Manager
from multiprocessing.sharedctypes import Value
import leveldb
import configparser
import sys

# signal
Start_Recovery = 'recovery start'
End_Recovery = 'recovery end'
Next_Block = 'next block'

No_FollowUp = 'no_follow_up'

# constant
Waiting_time_each_round = 5  # Waiting time for each round of voting , 5 seconds
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
        # voted_block , voted_vote number
        self._voted_block_number = Value('i', 0)
        self._voted_vote_number = Value('i',0)

    def close_Server(self):
        self._socketserver.close()

    # send data to a group of address
    def send_to_nodes(self,data):
        for ip in self._address_list:
            address = (ip, Worken_port)
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
        voted_block,voted_vote = affairProcess.vote(verify_list,len(self._address_list),self._nodes_keyring)
        # next block
        if not voted_vote:
            self._current_block_id.value = 'STOP'.encode()
        else:
            self._current_block_id.value = voted_vote[0]['vote']['voting_for_block'].encode()
            print('voted_vote: '+voted_vote[0]['vote']['voting_for_block'])
        print('voted_block: '+json.loads(voted_block)['id'])
        print('current block id : '+self._current_block_id.value.decode('utf-8'))
        # store block and votes
        leveldb.store_block_votes(voted_block,voted_vote)
        self._voted_block_number.value += 1
        self._voted_vote_number.value += len(voted_vote)

    # main process
    # one round : send request -- receiver response ---vote
    # send data format :
    # 1 round : { type : Start_Recovery,current_block_id : block id}
    # middle round : {type : Next_Block,current_block_id : block id}
    # last round : {type : End_Recovery,current_block_id : 'STOP'}
    def start(self):
        # round count
        round =1
        # TODO: mkdir for leveldb
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
                # statistic block and vote number.
                print('Voting statistics: ')
                print('block: '+str(self._voted_block_number.value))
                print('vote: '+str(self._voted_vote_number.value))
                leveldb.write_header(self._voted_block_number.value,self._voted_vote_number.value)
                return
            print('####################### Round %d Start #############################' % (round))
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
            # one round over
            print('####################### Round %d Over ##############################' % (round))
            round += 1
            if self._current_block_id.value.decode('utf-8') == 'STOP':
                send_data = {'type':End_Recovery,'current_block_id':'STOP'}
                end = True
            else:
                # next round send_data
                send_data = {'type':Next_Block,'current_block_id':self._current_block_id.value.decode('utf-8')}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 Broadcaster.py Ant.config")
        sys.exit(1)
    cf = configparser.ConfigParser()
    cf.read(sys.argv[1])
    # init parameter
    Waiting_time_each_round = int(cf.get('QueenAnt','queenant_waiting_time_each_round'))
    queenant_port = int(cf.get('QueenAnt','queenant_port'))
    NODES_FILE = cf.get('QueenAnt','queenant_node_list')
    Worken_port = int(cf.get('WorkenAnt','workenant_port'))

    # get local ip
    local_ip = util.get_ip('eth0')
    print('start Broadcaster server on %s:%d' % (local_ip,queenant_port))
    QueenServer(host=local_ip,port=queenant_port).start()
