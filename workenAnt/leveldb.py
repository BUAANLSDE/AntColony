__author__ = 'PC-LiNing'

import plyvel
import json
import os

# this file define interface to read data from local leveldb.

# node leveldb path
user_home =  os.path.expanduser('~')
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


# get value from header
def get_Header_value(key):
    h_db = leveldb.header_db
    return h_db.get(key.encode('utf-8')).decode('utf-8')


# update value from header
def update_Header_value(key,value):
    h_db = leveldb.header_db
    h_db.put(key.encode('utf-8'),value.encode('utf-8'))


# get block by id
def get_block_by_id(block_id):
    b_db = leveldb.bigchain_db
    return b_db.get(block_id.encode('utf-8')).decode('utf-8')


# get vote by id,the vote id is the previous_block value in the vote.
def get_vote_by_id(vote_id):
    v_db = leveldb.votes_db
    return v_db.get(vote_id.encode('utf-8')).decode('utf-8')


# get next block id
def get_block_next_id(current_block_id):
    vote = json.loads(get_vote_by_id(current_block_id))
    return vote['vote']['voting_for_block']


print(get_Header_value('gensis_block_id'))

print(get_block_next_id('77b87a97366d7dff22ad1662dafcd09bffaa5f60ae1610d401cae58882f1efa0'))
