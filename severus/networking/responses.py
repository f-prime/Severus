import severus
import json

def respond(obj, data):
    obj.send(json.dumps(data).encode())

def greet(obj, data):
    """
    Allows two peers to exchange information.
    Receives host and port of peer and responds with own host and port
    """
    host = data.get("host")
    port = data.get("port")
    peer = severus.Peer(host, port)
    if peer.is_alive() and host != severus.config.host and port != severus.config.port:
        peer.save()
    respond(obj, {
        "host":severus.config.host,
        "port":severus.config.port
    })

def getallpeers(obj, data):
    """
    Returns list of all known peers
    """
    all_peers = severus.db.peers.all()
    respond(obj, {"peers":all_peers})

def getblock(obj, data):
    """
    Returns a block with specific index
    """
    index = data.get("index")
    block = severus.db.get_block(index)
    respond(obj, {"block":block})
