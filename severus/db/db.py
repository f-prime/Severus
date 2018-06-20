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
        "pow":block.proof_of_work
    })

def get_blocks():
    all_blocks = blocks.all()
    block_objects = []
    for block in all_blocks:
        inputs = []
        outputs = []
        block_data = []
        for data in block['data']:
            if data['type'] == "TRANSACTION":
                for input_ in data['inputs']:
                    inputs.append(
                        Input(
                            txid=input_['txid'],
                            amount=input_['amount'],
                            from_addr=crypto.load_pub_key(input_['from']),
                            to_addr=crypto.load_pub_key(input_['to']),
                            signature=input_['signature'],
                            prev_txid=input_['prev_txid']
                        )
                    )
                for output in data['outputs']:
                    outputs.append(
                        severus.Output(
                            amount=output['amount'],
                            to_addr=severus.crypto.load_pub_key(output['to']),
                            from_addr=severus.crypto.load_pub_key(output['from'])
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
        block_objects.append(
            severus.Block(
                index=block['index'],
                block_data=block_data,
                previous_hash=block['previous'],
                timestamp=block['timestamp'],
                difficulty=block['difficulty'],
                proof_of_work=block['pow'],
                block_hash=block['hash']
            )
        )   
    return block_objects

