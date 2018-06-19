from .. import db
import rsa
import base64
from .utils.crypto import load_priv_key, load_pub_key, save_key
from .utils.calculate_funds import calculate_funds

class Wallet(object):
    def __init__(self, private_key=None, public_key=None):
        self.private_key = load_priv_key(private_key) if private_key else None
        self.public_key = load_pub_key(public_key) if public_key else None

    def create(self):
        public_key, private_key = rsa.newkeys(512)
        return Wallet(
            public_key=base64.b64encode(public_key._save_pkcs1_der()),
            private_key=base64.b64encode(private_key._save_pkcs1_der())
        )

    def save(self):
        if not self.private_key or not self.public_key:
            raise Exception(
                "Both private key and public key must be set"
            )

        public_key = save_key(self.public_key)
        private_key = save_key(self.private_key)
        for address in self.all_addresses():
            if address['private_key'] == private_key or address['public_key'] == public_key:
                raise Exception(
                    "Address is already exists."
                )
                
        db.wallet.insert({
            "public_key":public_key,
            "private_key":private_key
        })

    def all_addresses(self):
        return db.wallet.all()

    def load(self):
        addresses = self.all_addresses()
        if not addresses:
            raise Exception("No addresses exist.")
        self.private_key = load_priv_key(addresses[-1]['private_key'].encode())
        self.public_key = load_pub_key(addresses[-1]['public_key'].encode())

    def get_funds(self):
        if not self.public_key:
            raise Exception("No address loaded")
        return calculate_funds(self.public_key)        
