import severus

def sync():
    last_block = severus.db.get_last_block()
    index = 0
    if last_block:
        index = last_block.index + 1
    peers = severus.db.get_peers()
    usable_peer = None
    for peer in peers:
        if peer.is_alive():
            usable_peer = peer
            break
    else:
        usable_peer = severus.config.default_peer
        if not usable_peer.is_alive():
            raise Exception("No peers are alive.")
       
    greet = severus.Message(
        command="greet",
        host=severus.config.host,
        port=severus.config.port
    )
    usable_peer.send(greet)

    get_peers = severus.Message(
        command="getallpeers"
    )

    peers = usable_peer.send(get_peers)

    print(peers)

    while True:
        message = severus.Message(
            command="getblock",
            index=index
        )

        response = usable_peer.send(message)
        if not response['block']:
            print("All block downloaded.")
            break
        index += 1
        print(response)
