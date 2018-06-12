import Block
from utils.calculate_difficulty import calculate_difficulty
import random
import hashlib
from db import blocks

def mine():
    start_nonce = random.randint(0, 9999999)
    difficulty = calculate_difficulty()
    while True:
        new_diff = calculate_difficulty()
        if difficulty != new_diff:
            start_nonce = random.randint(0, 9999999)
        check = hashlib.sha512(str(start_nonce).encode()).hexdigest()
        if check.startswith(new_diff * "0"):
            all_blocks = blocks.all()
            if all_blocks:
                previous = all_blocks[-1]['hash']
            else:
                previous = ""

            block = Block.Block(
                [{
                    "to":"me",
                    "from":"severus",
                    "amount":25
                }],
                previous,
                str(start_nonce)
            )
            print("Found block", block)
            block.save()
        start_nonce += 1

if __name__ == "__main__":
    mine()
