import random
import hashlib
import time
import uuid
import severus
import sys

wallet = severus.Wallet()
wallet.load()

def get_nonce():
    return random.randint(0, 10*10**10)

def get_prev_block_hash():
    previous_block = severus.db.get_last_block()
    if not previous_block:
        return ""
    return previous_block.block_hash

def mine():
    start_nonce = get_nonce()
    difficulty = severus.calculate_difficulty()
    print("Mining at difficulty", difficulty)
    last_check = time.time()
    hashes = 0
    previous_hash = get_prev_block_hash()         
    while True:
        if time.time() - last_check >= 1:
            new_diff = severus.calculate_difficulty()
            previous_hash = get_prev_block_hash()
            if difficulty != new_diff:
                print("New Diff", new_diff)
                difficulty = new_diff
                start_nonce = get_nonce()
            last_check = time.time()
            print(hashes, "hashes per second")
            hashes = 0
        hashes += 1
        check = hashlib.sha512((previous_hash + str(start_nonce)).encode()).hexdigest()
        if check.startswith(difficulty * "0"):
            #print("Found match... verifying")
            previous = severus.db.get_last_block()
            if previous:
                previous_hash = previous.block_hash
                index = previous.index + 1
            else:
                index = 0
                previous_hash = ""
            
            txid = uuid.uuid4().hex

            output = severus.Output(
                amount=25,
                to_addr=wallet.public_key,
                from_addr="severus",
                txid=txid
            )

            transaction = severus.Transaction(
                txid=txid,
                from_addr="severus",
                to_addr=wallet.public_key,
                amount=25,
                inputs=[],
                outputs=[output],
                signature=severus.crypto.sign(txid, wallet.private_key)
            )
           
            block = severus.Block(
                index=index,
                block_data=[transaction],
                previous_hash=previous_hash,
                proof_of_work=str(start_nonce),
                miner=severus.crypto.save_key(wallet.public_key)
            )

            try:
                block.save()
                print("Found block", block) 
            except Exception as e:
                start_nonce = get_nonce()
            previous_hash = get_prev_block_hash()
        start_nonce += 1

if __name__ == "__main__":
    mine()
