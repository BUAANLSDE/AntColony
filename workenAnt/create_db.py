__author__ = 'PC-LiNing'

import plyvel
import json
import rethinkdb as r

# rethinkdb
r.connect("10.2.1.4",28015).repl()

bigchain_cursor = r.db('bigchain').table('bigchain').run()

# leveldb
db = plyvel.DB('/home/bc2/leveldb_home/bigchain',create_if_missing = True)

# bigchain
for document in bigchain_cursor:
    print(document['id'])
    db.put(document['id'].encode('utf-8'),json.dumps(document).encode('utf-8'))

db.close()

# votes
votes_cursor = r.db('bigchain').table('votes').run()
# leveldb
vote_db = plyvel.DB('/home/bc2/leveldb_home/votes',create_if_missing = True)
for vote in votes_cursor:
    print(vote['vote']['previous_block'])
    vote_id = vote['vote']['previous_block']+'-'+vote['node_pubkey']
    vote_db.put(vote_id.encode('utf-8'),json.dumps(vote).encode('utf-8'))

vote_db.close()


# header
# leveldb
header_db = plyvel.DB('/home/bc2/leveldb_home/header',create_if_missing = True)
header_db.put(b'votes_num',b'9')
header_db.put(b'block_num',b'4')
header_db.put(b'gensis_block_id',b'165590174b724e3242227e6bd82d602806845630c35579e9b642ed81e1713fa2')
header_db.put(b'previous_block_id',b'93a880af8b018bf98ee969d3fab2edcc78f13298dfd00649605528a443614cad')
header_db.put(b'current_block_id',b'38ae07973217534b67333b87553babcf3cc50fd2341e702a0c72f57cfb2ee822')
header_db.put(b'current_voting_for_block_id',b'38ae07973217534b67333b87553babcf3cc50fd2341e702a0c72f57cfb2ee822')
header_db.put(b'previous_voting_for_block_id',b'93a880af8b018bf98ee969d3fab2edcc78f13298dfd00649605528a443614cad')
header_db.put(b'host',b'10.2.1.4')
header_db.put(b'public_key',b'6yvVMDQqpbnCmVDaZcWX83CF9cdJh8otyusmKqKiPL8Q')
header_db.put(b'private_key',b'RDYLWjBsb43A34fSttjYqKcHRk6DwciSmhbrbuHpQ9R')

header_db.close()