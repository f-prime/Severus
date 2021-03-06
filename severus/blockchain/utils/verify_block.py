import hashlib
import severus
from tinydb import Query

def verify_pow(block):
    # Also need to verify that PoW is unique
    previous_block = severus.db.get_last_block()
    if not previous_block:
        previous_hash = ""
    else:
        previous_hash = previous_block.block_hash
    query = Query()
    proof_of_work = "{}{}".format(previous_hash, block.proof_of_work)
    difficulty = severus.calculate_difficulty(block=block)
    hash_check = hashlib.sha512(proof_of_work.encode()).hexdigest()
    if hash_check.startswith("0" * difficulty):
        return True
    return False

def verify_transactions(block):
    severus_count = 0
    for transaction in block.block_data:
        if transaction.type == "TRANSACTION":
            if transaction.from_addr == "severus":
                severus_count += 1
                if severus_count > 1:
                    return False
            if not transaction.verify():
                return False   
    return True

def verify_block_order(block):
    """
    Verify block comes after (in time, index, previous hash) to previous block
    """
    prev_block = severus.db.get_last_block()

    if not prev_block:
        return True

    if prev_block.block_hash != block.previous_hash:
        return False
    
    if prev_block.index + 1 != block.index:
        return False

    if prev_block.timestamp >= block.timestamp:
        return False

    return True

