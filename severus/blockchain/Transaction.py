from .. import db
from .utils import crypto
from .utils import calculate_funds

class Transaction(object):
    def __init__(
            self, 
            txid,
            from_addr, 
            to_addr, 
            amount, 
            inputs, 
            outputs, 
            signature
            ):
        
        self.txid = txid
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.inputs = inputs
        self.outputs = outputs
        self.signature = signature
        self.type = "TRANSACTION"

    def to_dict(self):
        inputs = []
        outputs = []
        for input_ in self.inputs:
            inputs.append(input_.to_dict())
        for output in self.outputs:
            outputs.append(output.to_dict())
        
        return {
            "type":self.type,
            "txid":self.txid,
            "from":crypto.save_key(self.from_addr),
            "to":crypto.save_key(self.to_addr),
            "amount":self.amount,
            "inputs":inputs,
            "outputs":outputs,
            "signature":self.signature
        }

     
    def verify(self):
        """
        1. Check all blocks and make sure this txid has not been used in a previous input
        2. Checks signature
        3. Verifies user has enough spendable coins available
       """
 

        blocks = db.get_blocks()
        for block in blocks:
            for data in block.block_data:
                if data.type == self.type:
                    for input_ in data.inputs:
                        if input_.txid == self.txid:
                            return False

        total_funds = calculate_funds.calculate_funds(self.from_addr)
        if total_funds < self.amount:
            return False

        signed = crypto.check_sig(self.txid, self.from_addr, self.signature)
        return signed

            
