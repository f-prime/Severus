import hashlib
from . import calculate_difficulty
from tinydb import Query
from severus import db

def verify_pow(block):
    # Also need to verify that PoW is unique
    query = Query()
    proof_of_work = block.proof_of_work
    if db.blocks.search(query.pow == proof_of_work):
        return False
    difficulty = calculate_difficulty.calculate_difficulty(block=block)
    hash_check = hashlib.sha512(proof_of_work.encode()).hexdigest()
    if hash_check.startswith("0" * difficulty):
        return True
    return False

def verify_transactions(block):
    for transaction in block.block_data:
        if transaction.type == "TRANSACTION":
            if not transaction.verify():
                return False
    return True

def verify_block_order(block):
    """
    Verify block comes after (both in time and index) to previous block
    """
    all_blocks = db.get_blocks()

    if not all_blocks:
        return True
    prev_block = all_blocks[-1]
    if prev_block.block_hash != block.previous_hash:
        return False
    
    if prev_block.index + 1 != block.index:
        return False

    if prev_block.timestamp >= block.timestamp:
        return False

    return True

