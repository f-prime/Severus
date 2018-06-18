import hashlib
from . import calculate_difficulty
from tinydb import Query
import severus

def verify_pow(block):
    # Also need to verify that PoW is unique
    query = Query()
    proof_of_work = block.proof_of_work
    if severus.db.blocks.search(query.pow == proof_of_work):
        return False
    difficulty = calculate_difficulty.calculate_difficulty(block=block)
    hash_check = hashlib.sha512(proof_of_work.encode()).hexdigest()
    if hash_check.startswith("0" * difficulty):
        return True
    return False

def verify_transactions(block):
    """
    Make sure there is no double spending and that sender has enough money to spend

    - Verifies signature on transaction is valid for the sender
    - Verifies user has enough spendable coins available
    - Verifies transaction is not duplicated
    """
    return True

def verify_block_order(block):
    """
    Verify block comes after (both in time and index) to previous block
    """
    all_blocks = severus.db.get_blocks()

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

