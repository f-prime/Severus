class Transaction(object):
    def __init__(self, txid, from_addr, to_addr, amount, inputs, outputs, signature):
        self.txid = txid
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.inputs = inputs
        self.outputs = outputs
        self.signature = signature

    def to_dict(self):
        inputs = []
        outputs = []
        for input_ in self.inputs:
            inputs.append(input_.to_dict())
        for output in self.outputs:
            outputs.append(output.to_dict())
        
        return {
            "txid":self.txid,
            "from":self.from_addr,
            "to":self.to_addr,
            "amount":self.amount,
            "inputs":inputs,
            "outputs":outputs,
            "signature":self.signature
        }

     
    def verify(self):
        pass
            
