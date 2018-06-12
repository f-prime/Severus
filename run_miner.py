from severus import Block
from severus.utils.calculate_difficulty import calculate_difficulty
import random
import hashlib
from severus.db import blocks
import time

def mine():
    start_nonce = random.randint(0, 9999999)
    difficulty = calculate_difficulty()
    print("Mining at difficulty", difficulty)
    while True:
        new_diff = calculate_difficulty()
        if difficulty != new_diff:
            print("New Diff", new_diff)
            difficulty = new_diff
            start_nonce = random.randint(0, 9999999)
        check = hashlib.sha512(str(start_nonce).encode()).hexdigest()
        if check.startswith(new_diff * "0"):
            all_blocks = blocks.all()
            if all_blocks:
                previous = all_blocks[-1]
                previous_hash = previous['hash']
                index = previous['index'] + 1
            else:
                index = 0
                previous_hash = ""

            block = Block.Block(
                index,  
                [{
                    "type":"TRANSACTION",
                    "to":"me",
                    "from":"severus",
                    "amount":25
                }],
                previous_hash,
                str(start_nonce),
                difficulty=difficulty,
                timestamp=time.time()
            )
            print("Found block", block)
            block.save()
        start_nonce += 1

if __name__ == "__main__":
    mine()
