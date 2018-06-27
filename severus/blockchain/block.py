import time
import hashlib
import severus

class Block(object):
    def __init__(
            self, 
            index, 
            block_data, 
            previous_hash, 
            proof_of_work, 
            miner,
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
            self.difficulty = severus.calculate_difficulty()
        self.proof_of_work = proof_of_work
        self.miner = miner
        if block_hash:
            self.block_hash = block_hash
        else:
            self.block_hash = self.hash_block()
        
    def hash_block(self):
        data = "{}{}{}{}{}{}{}".format(
                self.index, 
                self.timestamp, 
                self.previous_hash, 
                self.block_data, 
                self.difficulty, 
                self.proof_of_work,
                self.miner)
        
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
Miner: {}
        """.format(
                self.index, 
                self.timestamp, 
                self.previous_hash, 
                [bd.to_dict() for bd in self.block_data], 
                self.block_hash, 
                self.difficulty, 
                self.proof_of_work,
                self.miner)

    def to_dict(self):
        block_data = []
        for item in self.block_data:
            block_data.append(item.to_dict())

        return {
            "index":self.index,
            "timestamp":self.timestamp,
            "previous":self.previous_hash,
            "data":block_data,
            "hash":self.block_hash,
            "difficulty":self.difficulty,
            "pow":self.proof_of_work,
            "miner":self.miner
        }

    def verify(self):
        all_checks = [
            severus.verify_block.verify_pow(self),
            severus.verify_block.verify_block_order(self),
            severus.verify_block.verify_transactions(self)
        ]
        
        return all(all_checks)

    def save(self):
        if not self.verify():
            raise Exception("Invalid Block")
    
        severus.db.insert_block(self)
