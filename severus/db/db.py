import tinydb
import severus

blocks = tinydb.TinyDB("blocks.db").table("blocks")
wallet = tinydb.TinyDB("wallet.db").table("wallet")
peers  = tinydb.TinyDB("peers.db").table("peers")

def insert_peer(peer):
    peers.insert(peer.to_dict())

def insert_block(block):
    blocks.insert(block.to_dict())    

def get_peers():
    peers = []
    all_peers = peers.all()
    for peer in all_peers:
        peers.append(severus.Peer(peer['host'], peer['port']))
    return peers

def remove_peer(peer):
    query = tinydb.Query()
    peers.remove(query.host == peer.host and query.port == peer.port)

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

def get_block(index):
    query = tinydb.Query()
    return blocks.get(query.index == index)

def get_num_blocks():
    return len(blocks.all())

def get_last_block():
    last_block = blocks.all()
    if not last_block:
        return None
    return build_block(last_block[-1])

