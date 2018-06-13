from severus.blockchain.Output import Output
from severus.blockchain.Transaction import Transaction
from severus.blockchain.Block import Block

output = Output(
            amount=25, 
            to_addr="me", 
            from_addr="severus", 
            signature="123"
        )

transaction = Transaction(
    txid="123",
    to_addr="me",
    from_addr="severus",
    inputs=[],
    amount=25,
    outputs=[output],
    signature="123"
)

block = Block(
    index=0,
    block_data=[transaction],
    previous_hash="",
    proof_of_work="a"
)

print(block)
