import uuid
from severus.blockchain import Output, Transaction, Block
from severus.blockchain.utils.crypto import get_keys, save_key, sign

pub, priv = get_keys()
txid = uuid.uuid4().hex
signature = sign(txid, priv)
pub, priv = save_key(pub), save_key(priv)

output = Output(
    amount=25, 
    to_addr=pub,
    from_addr="severus", 
)

transaction = Transaction(
    txid=txid,
    to_addr=pub,
    from_addr="severus",
    inputs=[],
    amount=25,
    outputs=[output],
    signature=signature
)


block = Block(
    index=0,
    block_data=[transaction],
    previous_hash="aac0f041108e7c9af04aa633a56d73e7c63d7a062a349f505bcfe29c28581078",
    proof_of_work="61"
)
block.save()

print(block)
