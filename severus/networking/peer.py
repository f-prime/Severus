import severus
import socket

class Peer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def to_dict(self):
        return {
            "host":self.host,
            "port":self.port
        }

    def is_alive(self):
        s = socket.socket()
        try: 
            s.settimeout(5)
            s.connect((self.host, self.port))
        except Exception as e:
            print(e)
            s.close()
            return False
        s.close()
        return True

    def send(self, data):
        s = socket.socket()
        try:
            s.settimeout(5)
            s.connect((self.host, self.port))
        except:
            s.close()
            raise Exception("Peer is not alive")
        s.send(data)
        s.close()

    def remove(self):
        severus.db.remove_peer(self)

    def save(self):
        self.remove()
        severus.db.insert_peer(self)

