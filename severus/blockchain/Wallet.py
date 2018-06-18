from .. import db
import rsa
import base64

class Wallet(object):
    def __init__(self, private_key=None, public_key=None):
        self.private_key = private_key
        self.public_key = public_key

    def create(self):
        public_key, private_key = rsa.newkeys(256)
        return User(
            public_key=base64.b64encode(public_key._save_pkcs1_der()),
            private_key=base64.b64encode(private_key._save_pkcs1_der())
        )

    def save(self):
        if not self.private_key or not self.public_key:
            raise Exception(
                "Both private key and public key must be set"
            )
        db.wallet.insert({
            "public_key":self.public_key.decode(),
            "private_key":self.private_key.decode()
        })

    def all_addresses(self):
        return db.wallet.all()

    def load(self):
        addresses = self.all_addresses()
        if not addresses:
            raise Exception("No addresses exist.")
        self.private_key = addresses[-1]['private_key']
        self.public_key = addresses[-1]['public_key']
