import rsa
import base64

def sign(message, privkey):
    return base64.b64encode(rsa.sign(message.encode(), privkey, "SHA-1")).decode()

def check_sig(message, pubkey, signature):
    signature = base64.b64decode(signature)
    try:
        return rsa.verify(message.encode(), signature, pubkey).decode()
    except:
        return False

def get_keys():
    return rsa.newkeys(512)

def load_pub_key(key):
    if key == "severus":
        return key
    elif type(key) != bytes:
        return key
    key = base64.b64decode(key)
    return rsa.PublicKey._load_pkcs1_der(key)

def load_priv_key(key):
    if type(key) != bytes:
        return key.decode()
    key = base64.b64decode(key)
    return rsa.PrivateKey._load_pkcs1_der(key)

def save_key(key):
    if key == "severus":
        return key
    if type(key) == bytes:
        return key.decode()
    if type(key) == str:
        return key
    return base64.b64encode(key._save_pkcs1_der()).decode()
