import severus
import socket
import time
import _thread as thread
import json

def handle(obj, data):
    commands = {
        "getallpeers":severus.getallpeers,
        "getblock":severus.getblock,
        "greet":severus.greet
    }
    data = data.decode() 
    try:
        data = json.loads(data)
    except:
        print("Invalid JSON {}".format(data))
        obj.close()
        return

    if data.get("command") in commands:
        commands[data["command"]](obj, data)
    obj.close()

def listen():
    while True:
        host = severus.config.host
        port = severus.config.port
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
        except:
            print("Could not bind to {}:{} trying again.".format(host, port))
            s.close()
            time.sleep(1)
        s.listen(5)
        print("Severus started on port {}".format(port))
        while True:
            obj, ip = s.accept()
            data = obj.recv(1024)
            thread.start_new_thread(handle, (obj,data))
