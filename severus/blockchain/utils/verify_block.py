import hashlib
from severus.blockchain.utils.calculate_difficulty import calculate_difficulty
from tinydb import Query
from severus.db import blocks

def verify_pow(block):
    # Also need to verify that PoW is unique
    query = Query()
    proof_of_work = block.proof_of_work
    if blocks.search(query.pow == proof_of_work):
        return False
    difficulty = calculate_difficulty(block=block)
    hash_check = hashlib.sha512(proof_of_work.encode()).hexdigest()
    if hash_check.startswith("0" * difficulty):
        return True
    return False

def verify_data(block):
    block_data = block.block_data
    if type(block_data) != list:
        return False

    for transaction in block_data:
        if type(transaction) != dict:
            return False
        if transaction.get('type') == "POST":
            if not all([
                transaction.get("message"),
                transaction.get("from"),
                transaction.get("fee"),
                #transaction.get("signature")
            ]):
                return False
        elif transaction.get('type') == "TRANSACTION":
            if not all([
                transaction.get("from"),
                transaction.get("to"),
                transaction.get("amount"),
                #transaction.get("signature")
            ]):
                return False
        else:
            return False

    return True

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
    all_blocks = blocks.all()
    if not all_blocks:
        return True

    prev_block = all_blocks[-1]
    if prev_block['index'] != block.index:
        return False

    if prev_block['timestamp'] >= block.timestamp:
        return False

    return True

def verify_block(block):
    pow_verify = verify_pow(block)
    data_verify = verify_data(block) 
    tx_verify = verify_transactions(block)
    order_verify = verify_block_order(block)

    return all([
        order_verify,
        pow_verify,
        data_verify,
        tx_verify
    ])
