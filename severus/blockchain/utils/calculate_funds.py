import severus

def check_spent(output, blocks):
    for block in blocks:
        for data in block.block_data:
            if data.type == "TRANSACTION":
                for input_ in data.inputs:
                    if input_.output_id == output.output_id:
                        return True
    return False

def get_unspent_tx(public_key):
    public_key = severus.crypto.load_pub_key(public_key)
    blocks = severus.db.get_blocks()
    for block in blocks:
        for data in block.block_data:
            if data.type == "TRANSACTION":
                is_spent_check = False
                for output in data.outputs:
                    if output.to_addr == public_key:
                        if not is_spent_check:
                            if check_spent(output, severus.db.get_blocks()):
                                break
                            is_spent_check = True
                        yield output
                
def calculate_funds(public_key):
    return sum([x.amount for x in get_unspent_tx(public_key)])

