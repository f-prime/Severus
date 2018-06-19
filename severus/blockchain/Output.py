from severus.blockchain.utils import crypto

class Output(object):
    def __init__(
            self, 
            amount, 
            to_addr, 
            from_addr):
        
        self.amount = amount
        self.to_addr = crypto.load_pub_key(to_addr)
        self.from_addr = crypto.load_pub_key(from_addr)
        
    def to_dict(self):
        return {
            "amount":self.amount,
            "to":crypto.save_key(self.to_addr),
            "from":crypto.save_key(self.from_addr),
        }


