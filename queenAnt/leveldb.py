__author__ = 'PC-LiNing'

import os
import plyvel
import json

# block and votes store in leveldb.
# leveldb path
user_home = os.path.expanduser('~')
data_home = '/leveldb_home'
bigchain_path = user_home+data_home+'/bigchain'
votes_path = user_home+data_home+'/votes'
header_path = user_home+data_home+'/header'


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Leveldb(Singleton):
    bigchain_db = plyvel.DB(bigchain_path,create_if_missing = True)
    votes_db = plyvel.DB(votes_path,create_if_missing = True)
    header_db = plyvel.DB(header_path,create_if_missing = True)


leveldb = Leveldb()


# store  block
def  put_block(voted_block):
    b_db = leveldb.bigchain_db
    block = json.loads(voted_block)
    b_db.put(block['id'].encode('utf-8'),voted_block.encode('utf-8'))


# store vote
def put_vote(voted_vote):
    v_db = leveldb.votes_db
    vote_id = voted_vote['vote']['previous_block']+'-'+voted_vote['node_pubkey']
    v_db.put(vote_id.encode('utf-8'),json.dumps(voted_vote).encode('utf-8'))


# store header
def put_header_pair(key,value):
    h_db = leveldb.header_db
    h_db.put(key.encode('utf-8'),value.encode('utf-8'))


# write db header
def write_header(block_num,vote_num):
    put_header_pair("block_num",str(block_num))
    put_header_pair("vote_num",str(vote_num))


# get header value. return string
def get_header_value(key):
    h_db = leveldb.header_db
    return h_db.get(key.encode('utf-8')).decode('utf-8')


# store block , votes
def store_block_votes(voted_block,voted_votes):
    put_block(voted_block)
    for vote in voted_votes:
        put_vote(vote)

