class Input(object):
    def __init__(self, txid, amount, from_addr, to_addr, prev_txid, signature):
        self.txid = txid
        self.amount = amount
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.signature = signature
        self.prev_txid = prev_txid

    def to_dict(self):
        return {
            "txid":self.txid,
            "amount":self.amount,
            "from":self.from_addr,
            "to":self.to_addr,
            "signature":self.signature,
            "prev_txid":self.prev_txid
        }

    def __str__(self):
        return self.to_dict()
