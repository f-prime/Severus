from severus.db import blocks
import time
import math

def calculate_difficulty(block=None):
    all_blocks = blocks.all()
    if not block:
        num_blocks = len(all_blocks)
        if num_blocks == 0:
            return 0
        previous_block = all_blocks[-1]
        prev_difficulty = previous_block['difficulty']
        if prev_difficulty == 0:
            prev_difficulty += 1
        previous_timestamp = previous_block['timestamp']
        time_to_complete = (time.time() - previous_timestamp) / 60.0 

    else:
        if block.index == 0:
            return 0
        
        previous_block = all_blocks[block.index - 1]
        previous_timestamp = previous_block['timestamp']
        prev_difficulty = previous_block['difficulty']

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

       
