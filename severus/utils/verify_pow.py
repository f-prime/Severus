import hashlib

def verify_pow(difficulty, proof_of_work):
    hash_check = hashlib.sha512(proof_of_work.encode()).hexdigest()
    if hash_check.startswith("0" * difficulty):
        return True
    return False
