import severus
import _thread as thread

thread.start_new_thread(severus.listen, ())
severus.sync()

while True:
    pass
