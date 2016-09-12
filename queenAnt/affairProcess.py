__author__ = 'PC-LiNing'

import  json
import crypto
import hashlib
from collections import Counter

# init the publickey_list .
# receive_list is the 1 round  received data.
def init_publickey_list(receive_list,address_list):
    print('address list: ')
    print(address_list)
    node_num = len(address_list)
    publickey_list = []
    for data in receive_list:
        content = json.loads(data.decode("utf-8"))
        current_host = content['host']
        if current_host in address_list:
            publickey_list.append(content['pub_key'])
    print(publickey_list)
    if len(list(set(publickey_list))) == node_num:
        print('init public key : ')
        print(list(set(publickey_list)))
        return list(set(publickey_list))
    else:
        return None


# verify node's identity.
# first current_block_id is 'gensis' .
def verifynodes(receive_list,current_block_id,publickey_list):
    verify_list = []
    print('verifynodes current block id : ')
    print(current_block_id)
    print('public keys :')
    print(publickey_list)
    print('receive_list:')
    print(receive_list)
    for data in receive_list:
        content = json.loads(data.decode("utf-8"))
        verify_2 = True if content['pub_key'] in publickey_list  else False
        verify_1 = crypto.verify_data(pub_key=content['pub_key'],text=current_block_id,signature=content['signature'])
        if verify_1 and verify_2:
            verify_list.append(content)

    # TODO: add public_key duplicate removal
    print('verify_list : ')
    print(verify_list)
    return verify_list


# hash dict
def  hash_dict(dict):
    return hashlib.sha1(json.dumps(dict, sort_keys=True).encode()).hexdigest()


# get block list and vote list from verify_list .
def get_block_vote(verify_list):
    block_list = []
    vote_list = []
    for one in verify_list:
        if 'genesis_block' in one.keys():
            block_list.append(one['genesis_block'])
            vote_list.append(one['related_vote'])
        if 'next_block' in one.keys():
            block_list.append(one['next_block'])
            vote_list.append(one['related_vote'])

    print('get_block_vote : ')
    print(block_list)
    print('#####')
    print(vote_list)
    return block_list,vote_list

# vote . select the correct one data from list . (block,vote)
def vote(verify_list,num_node):
    block_values = []
    vote_values = []
    block_list , vote_list = get_block_vote(verify_list)

    for block in block_list:
        block_values.append(hash_dict(block))
    for vote in vote_list:
        vote_values.append(hash_dict(vote))

    print('vote  values : ')
    print(block_values)
    print(vote_values)
    b_values_counts = Counter(block_values)
    v_values_counts = Counter(vote_values)
    b_top_1 = b_values_counts.most_common(1)
    v_top_1 = v_values_counts.most_common(1)
    print('top : ')
    print(b_top_1)
    print(v_top_1)

    block_votes = b_top_1[0][1]
    block_target = b_top_1[0][0]

    vote_votes = v_top_1[0][1]
    vote_target = v_top_1[0][0]

    if block_votes > num_node / 2 and vote_votes > num_node / 2:
        return block_list[block_values.index(block_target)] , vote_list[vote_values.index(vote_target)]
    else:
        return None,None



