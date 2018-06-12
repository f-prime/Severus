from db import blocks

def calculate_difficulty():
    # Just a termporary difficulty calculation algorithm
    num_blocks = len(blocks.all())
    return num_blocks
