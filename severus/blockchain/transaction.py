import severus
import uuid

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
            "from":severus.crypto.save_key(self.from_addr),
            "to":severus.crypto.save_key(self.to_addr),
            "amount":self.amount,
            "inputs":inputs,
            "outputs":outputs,
            "signature":self.signature
        }

    def create(to_addr, amount):
        wallet = severus.Wallet()
        wallet.load()
        from_addr = wallet.public_key
        funds = severus.calculate_funds(from_addr)
        if funds < amount:
            raise Exception("You do not have enough funds in your wallet.")
        unspent_tx = severus.get_unspent_tx(from_addr)
        inputs = []
        total = 0
        txid = uuid.uuid4().hex
        for output in unspent_tx:
            if total >= amount:
                break
            inputs.append(
                severus.Input(
                    txid=txid,
                    amount=output.amount,
                    from_addr=from_addr,
                    to_addr=to_addr,
                    output_id=output.output_id
                )
            )
            total += output.amount
        
        outputs = []
        difference = total - amount
        if difference > 0:
            outputs.append(
                severus.Output(
                    txid=txid,
                    amount=difference,
                    to_addr=from_addr,
                    from_addr=from_addr
                )
            )
        outputs.append(
            severus.Output(
                txid=txid,
                amount=amount,
                to_addr=to_addr,
                from_addr=from_addr
            )
        )

        transaction = Transaction(
            txid=txid,
            from_addr=from_addr,
            to_addr=to_addr,
            amount=amount,
            inputs=inputs,
            outputs=outputs,
            signature=severus.crypto.sign(txid, wallet.private_key)
        )

        return transaction
        
    def verify(self):
        """
        1. Check all blocks and make sure this txid has not been used in a previous input
        2. Checks signature
        3. Verifies user has enough spendable coins available
        """

        if self.from_addr == "severus":
            if self.amount > 25:
                return False
            return True

        total_outputs = sum([x.amount for x in self.outputs])
        total_inputs = sum([x.amount for x in self.inputs])
        if total_inputs != total_outputs:
            return False

        unspent_tx = list(severus.get_unspent_tx(self.from_addr))
        for input_ in self.inputs:
            for output in unspent_tx:
                if output.output_id == input_.output_id:
                    break
            else:
                return False

        blocks = severus.db.get_blocks()

        total_funds = severus.calculate_funds(self.from_addr) 
        if total_funds < self.amount:
            return False

        signed = severus.crypto.check_sig(self.txid, self.from_addr, self.signature)
        return signed

            
