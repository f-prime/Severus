import tinydb
import time
import hashlib
from severus.db import blocks
from severus.utils.calculate_difficulty import calculate_difficulty
from severus.utils.verify_block import verify_block

class Block(object):
    def __init__(
            self, 
            index, 
            block_data, 
            previous_hash, 
            proof_of_work, 
            difficulty=calculate_difficulty(), 
            timestamp = time.time()
            ):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        block_data = block_data
        self.difficulty = difficulty
        self.proof_of_work = proof_of_work
        self.block_data = block_data
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
                self.block_data, 
                self.block_hash, 
                self.difficulty, 
                self.proof_of_work)

    def save(self):
        if not verify_block(self):
            raise Exception("Invalid Block")
        
        blocks.insert({
            "index":self.index,
            "timestamp":self.timestamp,
            "previous":self.previous_hash,
            "data":self.block_data,
            "hash":self.block_hash,
            "difficulty":self.difficulty,
            "pow":self.proof_of_work
        })
