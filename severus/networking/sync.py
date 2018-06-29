import severus

def sync():
    last_block = severus.db.get_last_block()
    index = 0
    if last_block:
        index = last_block.index + 1
    peers = severus.db.get_peers()
    usable_peer = None
    for peer in peers:
        if peer.host != severus.config.host and peer.port != severus.config.port and peer.is_alive():
            usable_peer = peer
            break
        else:
            peer.remove()
    else:
        usable_peer = severus.config.default_peer
        if not usable_peer.is_alive():
            raise Exception("No peers are alive.")
       
    greet = severus.Message(
        command="greet",
        port=severus.config.port,
        is_relay=severus.config.is_relay
    )

    usable_peer.send(greet)

    get_peers = severus.Message(
        command="getallpeers"
    )

    peers = usable_peer.send(get_peers)

    for peer in peers['peers']:
        peer = severus.Peer(host=peer['host'], port=peer['port'])
        peer.save()

    while True:
        message = severus.Message(
            command="getblock",
            index=index
        )

        response = usable_peer.send(message)
        if not response['block']:
            print("All block downloaded.")
            break
             
        block = severus.db.build_block(response['block'])
        if block.verify():
            print(block)
            block.save()
        else:
            raise Exception("Block invalid")
        index += 1
