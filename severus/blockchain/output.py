import severus
import uuid

class Output(object):
    def __init__(
            self, 
            amount, 
            to_addr, 
            from_addr,
            output_id=None
            ):
        
        self.amount = amount
        self.to_addr = severus.crypto.load_pub_key(to_addr)
        self.from_addr = severus.crypto.load_pub_key(from_addr)
        self.output_id = output_id
        if not self.output_id:
            self.output_id = uuid.uuid4().hex

    def to_dict(self):
        return {
            "amount":self.amount,
            "to":severus.crypto.save_key(self.to_addr),
            "from":severus.crypto.save_key(self.from_addr),
            "id":self.output_id
        }


