__author__ = 'PC-LiNing'

import plyvel
import json
import os
import crypto

# this file define interface to read data from local leveldb.

# node leveldb path
user_home =  os.path.expanduser('~')
data_home = '/leveldb_home'
bigchain_path = user_home+data_home+'/bigchain'
votes_path = user_home+data_home+'/votes'
header_path = user_home+data_home+'/header'

No_FollowUp = 'no_follow_up'

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
    vote = v_db.get(vote_id.encode('utf-8'))
    if vote is not None:
        return vote.decode('utf-8')
    else:
        return None


# get next block id
def get_block_next_id(current_block_id):
    temp_vote = get_vote_by_id(current_block_id)
    if temp_vote is not None:
        vote = json.loads(temp_vote)
        return vote['vote']['voting_for_block']
    else:
        return None



# response data
# {pub_key: public key,signature:signature,next_block:block ,related_vote:vote}
def get_response_data(current_block_id):
    public_key = get_Header_value('public_key')
    private_key = get_Header_value('private_key')
    signature = crypto.sign_data(text=current_block_id,priv_key=private_key)
    next_block = get_block_by_id(current_block_id)
    next_vote = get_vote_by_id(current_block_id)
    if next_vote is None:
        next_vote = No_FollowUp
    response_data={
                    "pub_key": public_key,
                    "signature":signature,
                    "next_block":next_block,
                    "related_vote":next_vote
                  }
    return json.dumps(response_data)


# response start
# signature is encrypt string 'genesis'
# {pub_key: public key,signature:signature,genesis_block:block ,related_vote:vote , host:host}
def get_start_data():
    public_key = get_Header_value('public_key')
    private_key = get_Header_value('private_key')
    host = get_Header_value('host')
    signature = crypto.sign_data(text='genesis',priv_key=private_key)
    genesis_block =get_block_by_id(get_Header_value('gensis_block_id'))
    next_vote = get_vote_by_id(get_Header_value('gensis_block_id'))
    response_data={
                    "pub_key": public_key,
                    "signature":signature,
                    "genesis_block":genesis_block,
                    "related_vote":next_vote,
                    "host":host
                  }
    return json.dumps(response_data)

# print(get_Header_value('gensis_block_id'))
# print(get_block_next_id('77b87a97366d7dff22ad1662dafcd09bffaa5f60ae1610d401cae58882f1efa0'))
