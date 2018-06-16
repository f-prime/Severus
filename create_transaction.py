from severus.blockchain.Output import Output
from severus.blockchain.Transaction import Transaction
from severus.blockchain.Block import Block
from severus.blockchain.utils.crypto import get_keys, save_key, sign
import uuid

pub, priv = get_keys()
txid = uuid.uuid4().hex
signature = sign(txid, priv)

output = Output(
            amount=25, 
            to_addr=save_key(pub), 
            from_addr="severus", 
            )

transaction = Transaction(
    txid=txid,
    to_addr=save_key(pub),
    from_addr="severus",
    inputs=[],
    amount=25,
    outputs=[output],
    signature=signature
)

block = Block(
    index=0,
    block_data=[transaction],
    previous_hash="",
    proof_of_work="a"
)
block.save()

print(block)
