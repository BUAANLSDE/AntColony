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
    for data in receive_list:
        content = json.loads(data.decode("utf-8"))
        verify_2 = True if content['pub_key'] in publickey_list  else False
        verify_1 = crypto.verify_data(pub_key=content['pub_key'],text=current_block_id,signature=content['signature'])
        if verify_1 and verify_2:
            verify_list.append(content)

    # TODO: add public_key duplicate removal
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

    return block_list,vote_list


# get vote list by node_pubkey
def  parse_vote_list(votes_list,publickey_list):
     node_vote_list = []
     for key in publickey_list:
         current_node = []
         for votes in votes_list:
             # handle  No_FollowUp , votes is empty list .
             for vote in votes:
                 # convert string to json
                 temp = json.loads(vote)
                 if temp['node_pubkey'] == key:
                     current_node.append(temp)
                     break

         if current_node:
             node_vote_list.append(current_node)

     return node_vote_list


# vote . select the correct one data from list . (block,vote)
def vote(verify_list,num_node,publickey_list):
    # target votes
    target_votes = []
    # separate block and vote
    block_list , vote_list = get_block_vote(verify_list)
    # parse vote list
    node_votes_list = parse_vote_list(vote_list,publickey_list)

    # ballot for block
    block_values = []
    for block in block_list:
        block_values.append(hash_dict(json.loads(block)))
    b_values_counts = Counter(block_values)
    b_top_1 = b_values_counts.most_common(1)
    block_votes = b_top_1[0][1]
    block_target = b_top_1[0][0]
    target_block = block_list[block_values.index(block_target)]
    # failed flag
    votes_failed = False
    # ballot for votes
    for votes in node_votes_list:
        votes_values = []
        # ballot for node's vote
        for vote in votes:
            votes_values.append(hash_dict(vote))
        node_values_counts = Counter(votes_values)
        node_top_1 = node_values_counts.most_common(1)
        node_votes = node_top_1[0][1]
        node_target = node_top_1[0][0]
        if node_votes > num_node / 2:
            target_votes.append(votes[votes_values.index(node_target)])
        else:
            votes_failed = True
            break

    if block_votes > num_node / 2 and not votes_failed:
        # No_FollowUp,target_votes is empty list .
        print('vote success!')
        return target_block,target_votes
    else:
        print('pass failed!')
        return None,None



