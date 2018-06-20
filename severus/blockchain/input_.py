import severus

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
        self.from_addr = severus.crypto.load_pub_key(from_addr)
        self.to_addr = severus.crypto.load_pub_key(to_addr)
        self.signature = signature
        self.prev_txid = prev_txid

    def to_dict(self):
        return {
            "txid":self.txid,
            "amount":self.amount,
            "from":severus.crypto.save_key(self.from_addr),
            "to":severus.crypto.save_key(self.to_addr),
            "signature":self.signature,
            "prev_txid":self.prev_txid
        }

