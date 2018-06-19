import time
import hashlib
from .utils import verify_block, calculate_difficulty
from severus import db

class Block(object):
    def __init__(
            self, 
            index, 
            block_data, 
            previous_hash, 
            proof_of_work, 
            difficulty=None, 
            timestamp=None,
            block_hash=None
            ):
        self.index = index
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.block_data = block_data
        if difficulty != None:
            self.difficulty = difficulty
        else:
            self.difficulty = calculate_difficulty.calculate_difficulty()
        self.proof_of_work = proof_of_work
        if block_hash:
            self.block_hash = block_hash
        else:
            self.block_hash = self.hash_block()
        
    def hash_block(self):
        data = "{}{}{}{}{}{}".format(
                self.index, 
                self.timestamp, 
                self.previous_hash, 
                self.block_data, 
                self.difficulty, 
                self.proof_of_work)
        
        return hashlib.sha256(data.encode()).hexdigest()

    def __str__(self):
        return """
Index: {}
Time: {}
Previous: {}
Data: {}
Hash: {}
Difficulty: {}
Proof of Work: {}
        """.format(
                self.index, 
                self.timestamp, 
                self.previous_hash, 
                [bd.to_dict() for bd in self.block_data], 
                self.block_hash, 
                self.difficulty, 
                self.proof_of_work)

    def verify(self):
        all_checks = [
            verify_block.verify_pow(self),
            verify_block.verify_block_order(self),
            verify_block.verify_transactions(self)
        ]

        print(all_checks)
        return all(all_checks)

    def save(self):
        if not self.verify():
            raise Exception("Invalid Block")
    
        db.insert_block(self)
