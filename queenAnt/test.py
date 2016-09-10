
import json
dic ={"id":"aabbcc","name":"test"}
str = dic['id']

print(bytearray(str,encoding='utf-8'))

print(bytes(str,'utf-8'))

print(json.dumps(dic).encode('utf-8'))

bs = b'aabbcc'
print(bs.decode('utf-8'))

data_home = '~/leveldb_home'
bigchain_path = data_home+'/bigchain'

print(bigchain_path)