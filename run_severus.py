import severus
import _thread as thread
import socket
import requests
import random
import threading
import time

def is_relay():
    def listen(port):
        s = socket.socket()
        s.bind(("0.0.0.0", port))
        s.listen(5)
        _, __ = s.accept()
        _.close()
    port = random.randint(5000, 9999)
    try:
        ip = requests.get("https://bot.whatismyipaddress.com").content.decode()
    except:
        ip = input("Could not get external IP address... what is it? ")
    while port == severus.config.port:
        port = random.randint(5000, 9999)
    t = threading.Thread(target=listen, args=(port,))
    t.start()
    time.sleep(3) # Give thread time to start socket
    s = socket.socket()
    try:
        s.settimeout(5)
        s.connect((ip, port))
    except:
        s.close()
        return False
    s.close()
    return True

if is_relay():
    severus.config.is_relay = True
    print("Relay Node")
    thread.start_new_thread(severus.listen, ())
    severus.sync()
    while True:
        pass
else:
    print("Leech node")
    severus.config.is_relay = False
    while True:
        severus.sync()
        time.sleep(30)

