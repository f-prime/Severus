import tinydb
import time
import hashlib
from severus.db import blocks
from severus.utils.calculate_difficulty import calculate_difficulty
from severus.utils.verify_pow import verify_pow

class Block(object):
    def __init__(self, block_data, previous_hash, proof_of_work):
        self.index = len(blocks.all())
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        if type(block_data) == dict:
            block_data = [block_data]
        elif type(block_data) != list:
            raise Exception("Block data must be an array of dictionaries")
        
        self.difficulty = calculate_difficulty()
        self.proof_of_work = proof_of_work
        
        if not verify_pow(self.difficulty, proof_of_work):
            raise Exception("Proof of Work invalid")

        self.block_data = block_data
        self.block_hash = self.hash_block()

    def hash_block(self):
        data = "{}{}{}{}{}{}".format(self.index, self.timestamp, self.previous_hash, self.block_data, self.difficulty, self.proof_of_work)
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
        """.format(self.index, self.timestamp, self.previous_hash, self.block_data, self.block_hash, self.difficulty, self.proof_of_work)

    def save(self):
        blocks.insert({
            "index":self.index,
            "timestamp":self.timestamp,
            "previous":self.previous_hash,
            "data":self.block_data,
            "hash":self.block_hash,
            "difficulty":self.difficulty,
            "pow":self.proof_of_work
        })
