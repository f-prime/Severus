from severus.blockchain.utils.crypto import save_key, load_pub_key

class Output(object):
    def __init__(
            self, 
            amount, 
            to_addr, 
            from_addr):
        
        self.amount = amount
        self.to_addr = load_pub_key(to_addr)
        self.from_addr = load_pub_key(from_addr)
        
    def to_dict(self):
        print(save_key(self.to_addr))
        return {
            "amount":self.amount,
            "to":save_key(self.to_addr),
            "from":save_key(self.from_addr),
        }


