import tinydb
import time
import hashlib
from severus.db import insert_block
from severus.blockchain.utils.calculate_difficulty import calculate_difficulty
from severus.blockchain.utils.verify_block import *

class Block(object):
    def __init__(
            self, 
            index, 
            block_data, 
            previous_hash, 
            proof_of_work, 
            difficulty=calculate_difficulty(), 
            timestamp = time.time(),
            block_hash=None
            ):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.block_data = block_data
        self.difficulty = difficulty
        self.proof_of_work = proof_of_work
        self.block_data = block_data
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
        return all([
            verify_pow(self),
            verify_block_order(self)
        ])

    def save(self):
        if not self.verify():
            raise Exception("Invalid Block")
    
        insert_block(self)
