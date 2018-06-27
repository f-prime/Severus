import tinydb
import severus

blocks = tinydb.TinyDB("blocks.db").table("blocks")
wallet = tinydb.TinyDB("wallet.db").table("wallet")

def insert_block(block):
    block_data = []
    for item in block.block_data:
        block_data.append(item.to_dict())
    
    blocks.insert({
        "index":block.index,
        "timestamp":block.timestamp,
        "previous":block.previous_hash,
        "data":block_data,
        "hash":block.block_hash,
        "difficulty":block.difficulty,
        "pow":block.proof_of_work,
        "miner":block.miner
    })

def build_block(block):
    inputs = []
    outputs = []
    block_data = []
    for data in block['data']:
        if data['type'] == "TRANSACTION":
            for input_ in data['inputs']:
                inputs.append(
                    severus.Input(
                        txid=input_['txid'],
                        amount=input_['amount'],
                        from_addr=severus.crypto.load_pub_key(input_['from']),
                        to_addr=severus.crypto.load_pub_key(input_['to']),
                        output_id=input_['output_id']
                    )
                )
            for output in data['outputs']:
                outputs.append(
                    severus.Output(
                        txid=output['txid'],
                        amount=output['amount'],
                        to_addr=severus.crypto.load_pub_key(output['to']),
                        from_addr=severus.crypto.load_pub_key(output['from']),
                        output_id=output['id']
                    )
                )
            block_data.append(
                severus.Transaction(
                    txid=data['txid'],
                    from_addr=severus.crypto.load_pub_key(data['from']),
                    to_addr=severus.crypto.load_pub_key(data['to']),
                    amount=data['amount'],
                    inputs=inputs,
                    outputs=outputs,
                    signature=data['signature']
                )
            )
    return severus.Block(
        index=block['index'],
        block_data=block_data,
        previous_hash=block['previous'],
        timestamp=block['timestamp'],
        difficulty=block['difficulty'],
        proof_of_work=block['pow'],
        block_hash=block['hash'],
        miner=block['miner']
    )


def get_blocks():
    all_blocks = blocks.all()
    for block in all_blocks:
        yield build_block(block)

def get_num_blocks():
    return len(blocks.all())

def get_last_block():
    last_block = blocks.all()
    if not last_block:
        return None
    return build_block(last_block[-1])

