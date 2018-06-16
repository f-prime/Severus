from severus.blockchain.utils.crypto import save_key, load_pub_key

class Input(object):
    def __init__(
            self,
            txid, 
            amount, 
            from_addr, 
            to_addr, 
            prev_txid, 
            signature):
        
        self.txid = txid
        self.amount = amount
        self.from_addr = load_pub_key(from_addr)
        self.to_addr = load_pub_key(to_addr)
        self.signature = signature
        self.prev_txid = prev_txid

    def to_dict(self):
        return {
            "txid":self.txid,
            "amount":self.amount,
            "from":save_key(self.from_addr),
            "to":save_key(self.to_addr),
            "signature":self.signature,
            "prev_txid":self.prev_txid
        }

