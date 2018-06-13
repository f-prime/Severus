class Output(object):
    def __init__(self, amount, to_addr, from_addr, signature):
        self.amount = amount
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.signature = signature
        
    def to_dict(self):
        return {
            "amount":self.amount,
            "to":self.to_addr,
            "from":self.from_addr,
            "signature":self.signature
        }


