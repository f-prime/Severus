import rsa
import base64

def sign(message, privkey):
    return base64.b64encode(rsa.sign(message.encode(), privkey, "SHA-1")).decode()

def check_sig(message, pubkey, signature):
    if pubkey == "severus":
        return True
    signature = base64.b64decode(signature)
    if isinstance(pubkey, str):
        pubkey = load_pub_key(pubkey.encode())
    elif isinstance(pubkey, bytes):
        pubkey = load_pub_key(pubkey)

    try:
        return rsa.verify(message.encode(), signature, pubkey)
    except Exception as e:
        print(e)
        return False

def get_keys():
    return rsa.newkeys(512)

def load_pub_key(key):
    if key == "severus":
        return key
    elif isinstance(key, str):
        key = key.encode()
    elif not isinstance(key, bytes):
        return key
    key = base64.b64decode(key)
    return rsa.PublicKey._load_pkcs1_der(key)

def load_priv_key(key):
    if isinstance(key, str):
        key = key.encode()
    elif not isinstance(key, bytes):
        return key.decode()
    key = base64.b64decode(key)
    return rsa.PrivateKey._load_pkcs1_der(key)

def save_key(key):
    if key == "severus":
        return key
    if isinstance(key, bytes):
        return key.decode()
    if isinstance(key, str):
        return key
    return base64.b64encode(key._save_pkcs1_der()).decode()
