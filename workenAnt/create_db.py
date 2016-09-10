__author__ = 'PC-LiNing'

import plyvel
import json
import rethinkdb as r

# rethinkdb
r.connect("10.2.1.57",28015).repl()

bigchain_cursor = r.db('bigchain').table('bigchain').run()

# leveldb
db = plyvel.DB('/home/bc6/leveldb_home/bigchain',create_if_missing = True)

# bigchain
for document in bigchain_cursor:
    print(document['id'])
    db.put(document['id'].encode('utf-8'),json.dumps(document).encode('utf-8'))

db.close()

# votes
votes_cursor = r.db('bigchain').table('votes').run()
# leveldb
vote_db = plyvel.DB('/home/bc6/leveldb_home/votes',create_if_missing = True)
for vote in votes_cursor:
    print(vote['vote']['previous_block'])
    vote_db.put(vote['vote']['previous_block'].encode('utf-8'),json.dumps(vote).encode('utf-8'))

vote_db.close()


# header
# leveldb
header_db = plyvel.DB('/home/bc6/leveldb_home/header',create_if_missing = True)
header_db.put(b'votes_num',b'2')
header_db.put(b'block_num',b'3')
header_db.put(b'gensis_block_id',b'77b87a97366d7dff22ad1662dafcd09bffaa5f60ae1610d401cae58882f1efa0')
header_db.put(b'previous_block_id',b'a77c8df1b9302c08f12a2a31308e14003b874621f4cb3786ddbaa99b98ae4310')
header_db.put(b'current_block_id',b'85f99abfc3e4d0945cbedff9bb522b48ec9c17e4cbdf4e225f98558ce5f8d3e3')
header_db.put(b'current_voting_for_block_id',b'85f99abfc3e4d0945cbedff9bb522b48ec9c17e4cbdf4e225f98558ce5f8d3e3')
header_db.put(b'previous_voting_for_block_id',b'a77c8df1b9302c08f12a2a31308e14003b874621f4cb3786ddbaa99b98ae4310')
header_db.put(b'host',b'10.2.1.35')
header_db.put(b'public_key',b'Bnhrz13GTVMoL1okmUT8igD3ywKQfS8J9EdW6oq9jzwo')
header_db.put(b'private_key',b'FMsBYHJepFn7KHWVvSqb3saZRrzcRe9bqUjUqd6VsTLS')

header_db.close()