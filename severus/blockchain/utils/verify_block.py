import hashlib
from severus.blockchain.utils.calculate_difficulty import calculate_difficulty

def verify_pow(block):
    # Also need to verify that PoW is unique
    proof_of_work = block.proof_of_work
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
                transaction.get("id"),
                transaction.get("message"),
                transaction.get("from"),
                transaction.get("fee"),
            ]):
                return False
        elif transaction.get('type') == "TRANSACTION":
            if not all([
                transaction.get("from"),
                transaction.get("to"),
                transaction.get("amount")
            ]):
                return False
        else:
            return False

    return True

def verify_transactions(block):
    """
    Make sure there is no double spending and that sender has enough money to spend
    """
    return True

def verify_block_order(block):
    """
    Verify block comes after (both in time and index) to previous block
    """
    pass

def verify_block(block):
    pow_verify = verify_pow(block)
    data_verify = verify_data(block) 
    tx_verify = verify_transactions(block)

    return all([
        pow_verify,
        data_verify,
        tx_verify
    ])
