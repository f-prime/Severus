import time
from severus import db

def calculate_difficulty(block=None):
    previous_block = db.get_last_block()
    if not block:
        if not previous_block:
            return 0
        prev_difficulty = previous_block.difficulty
        if prev_difficulty == 0:
            prev_difficulty += 1
        previous_timestamp = previous_block.timestamp
        time_to_complete = (time.time() - previous_timestamp) / 60.0 

    else:
        if block.index == 0:
            return 0
        
        previous_timestamp = previous_block.timestamp
        prev_difficulty = previous_block.difficulty

        if prev_difficulty == 0:
            prev_difficulty += 1

        time_to_complete = (block.timestamp - previous_timestamp) / 60.0
    
    if time_to_complete < 10: # 10 minutes per block
        difficulty = prev_difficulty + 1
    else:
        difficulty = prev_difficulty - 1
    if difficulty <= 0:
        difficulty = 1
    return difficulty

       
