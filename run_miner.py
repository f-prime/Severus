from severus.blockchain import Block, Output, Input, Transaction, Wallet
from severus.blockchain.utils.calculate_difficulty import calculate_difficulty
from severus.blockchain.utils.crypto import sign
import random
import hashlib
from severus.db import get_blocks
import time
import uuid

wallet = Wallet()
wallet.load()

def get_nonce():
    return random.randint(0, 10*10**10)

def mine():
    start_nonce = get_nonce()
    difficulty = calculate_difficulty()
    print("Mining at difficulty", difficulty)
    while True:
        new_diff = calculate_difficulty()
        if difficulty != new_diff:
            print("New Diff", new_diff)
            difficulty = new_diff
            start_nonce = get_nonce()
        check = hashlib.sha512(str(start_nonce).encode()).hexdigest()
        if check.startswith(new_diff * "0"):
            all_blocks = get_blocks()
            if all_blocks:
                previous = all_blocks[-1]
                previous_hash = previous.block_hash
                index = previous.index + 1
            else:
                index = 0
                previous_hash = ""
            output = Output(
                amount=25,
                to_addr=wallet.public_key,
                from_addr="severus"
            )
            
            txid = uuid.uuid4().hex

            transaction = Transaction(
                txid=txid,
                from_addr="severus",
                to_addr=wallet.public_key,
                amount=25,
                inputs=[],
                outputs=[output],
                signature=sign(txid, wallet.private_key)
            )
            
            block = Block(
                index=index,
                block_data=[transaction],
                previous_hash=previous_hash,
                proof_of_work=str(start_nonce)
            )

            print("Found block", block)
            try:
                block.save()
            except Exception as e:
                print(e)
                start_nonce = get_nonce()
                break
        start_nonce += 1

if __name__ == "__main__":
    mine()
