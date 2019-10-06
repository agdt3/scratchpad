import threading


class Semaphore(threading.Semaphore):
    wait = threading.Semaphore.acquire
    signal = threading.Semaphore.release


class Thread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()
