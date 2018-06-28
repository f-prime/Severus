import json

class Message(object):
    def __init__(self, command, **kwargs):
        self.command = command
        self.args = {"command":self.command}
        for arg in kwargs:
            self.args[arg] = kwargs[arg]

    def to_dict(self):
        return self.args

    def to_json(self):
        return json.dumps(self.args).encode()
