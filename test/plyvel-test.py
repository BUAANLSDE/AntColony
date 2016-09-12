
import plyvel

db=plyvel.DB('./db3',create_if_missing=True)

db.put(b'example-aaa',b'aaa')
db.put(b'example-bbb',b'bbb')
db.put(b'example-ccc',b'ccc')



sub_db = db.prefixed_db(b'example-')

sub_db.put(b'ddd',b'ddd')

print('#########')
for key,value in sub_db:
	print(key)
	print(value)
