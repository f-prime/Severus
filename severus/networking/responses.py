import severus
import json

def respond(obj, data):
    obj.send(json.dumps(data).encode())

def greet(obj, ip, data):
    """
    Allows two peers to exchange information.
    Receives host and port of peer and responds with own host and port
    """
    host = ip[0]
    port = data.get("port")
    is_relay = data.get("is_relay")
    if is_relay:
        peer = severus.Peer(host, port)
        if peer.is_alive() and host != severus.config.host and port != severus.config.port:
            peer.save()
    respond(obj, {
        "message":"Greetings"
    })

def getallpeers(obj, ip, data):
    """
    Returns list of all known peers
    """
    all_peers = severus.db.peers.all()
    respond(obj, {"peers":all_peers})

def getblock(obj, ip, data):
    """
    Returns a block with specific index
    """
    index = data.get("index")
    block = severus.db.get_block(index)
    respond(obj, {"block":block})
