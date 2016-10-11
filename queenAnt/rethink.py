__author__ = 'PC-LiNing'

import json
import rethinkdb as r
import leveldb


# write block and vote to rethinkdb
# rethinkdb should be empty before flush
def  flush_to_rethinkdb(host,port):
    # rethinkdb
    conn=r.connect(host=host,port=port)
    # bigchain
    b_db = leveldb.leveldb.bigchain_db
    for key,value in b_db:
        block = json.loads(value.decode('utf-8'))
        r.db('bigchain').table('bigchain').insert(block).run(conn)
    # votes
    v_db = leveldb.leveldb.votes_db
    for key,value in v_db:
        vote = json.loads(value.decode('utf-8'))
        r.db('bigchain').table('votes').insert(vote).run(conn)

    conn.close()


host = '10.2.1.4'
port = 28015
flush_to_rethinkdb(host,port)
