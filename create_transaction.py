import uuid
import severus

pub, priv = severus.crypto.get_keys()
txid = uuid.uuid4().hex
signature = severus.crypto.sign(txid, priv)
pub, priv = severus.crypto.save_key(pub), severus.crypto.save_key(priv)

output = severus.Output(
    amount=25, 
    to_addr=pub,
    from_addr="severus", 
)

transaction = severus.Transaction(
    txid=txid,
    to_addr=pub,
    from_addr="severus",
    inputs=[],
    amount=25,
    outputs=[output],
    signature=signature
)


block = severus.Block(
    index=0,
    block_data=[transaction],
    previous_hash="aac0f041108e7c9af04aa633a56d73e7c63d7a062a349f505bcfe29c28581078",
    proof_of_work="61"
)
block.save()

print(block)
