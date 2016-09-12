__author__ = 'PC-LiNing'

from  cryptoconditions import crypto


def generate_key_pair():
    sk, pk = crypto.ed25519_generate_key_pair()
    return sk.decode(), pk.decode()


# return signature
def sign_data(text,priv_key):
    return crypto.Ed25519SigningKey(key=priv_key).sign(data=text)


# verify . True or False
def verify_data(pub_key,text,signature):
    return crypto.Ed25519VerifyingKey(key=pub_key).verify(data=text,signature=signature)


