from severus import db

def check_spent(data, blocks):
    for block in blocks:
        for data in block.block_data:
            if data.type == "TRANSACTION":
                for input_ in data.inputs:
                    if input_.txid == data.txid:
                        return True
    return False

def calculate_funds(public_key):
    total = 0
    blocks = db.get_blocks()
    for block in blocks:
        for data in block.block_data:
            if data.type == "TRANSACTION":
                is_spent_check = False
                for output in data.outputs:
                    if output.to_addr == public_key:
                        if not is_spent_check:
                            if check_spent(data, db.get_blocks()):
                                break
                            is_spent_check = True
                        total += output.amount
    return total
                            

