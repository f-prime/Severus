import severus
import socket
import json

class Peer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def to_dict(self):
        return {
            "host":self.host,
            "port":self.port
        }

    def __str__(self):
        return "{}:{}".format(self.host, self.port)

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

    def send(self, message):
        s = socket.socket()
        try:
            s.settimeout(5)
            s.connect((self.host, self.port))
        except:
            s.close()
            raise Exception("Peer is not alive")
        s.send(message.to_json())
        response = ""
        while True:
            resp = s.recv(1024)
            if not resp:
                break
            response += resp.decode()
        s.close()
        return json.loads(response)

    def remove(self):
        severus.db.remove_peer(self)

    def save(self):
        self.remove()
        severus.db.insert_peer(self)

