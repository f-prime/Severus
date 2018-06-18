from .. import db

def calculate_funds(public_key):
    blocks = db.get_blocks()
    for block in blocks:
        print(block)

