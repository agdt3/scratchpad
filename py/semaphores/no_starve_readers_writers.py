import time
from random import random
from threading import Thread, Semaphore
from lightswitch import Lightswitch

n = 5
room_empty = Semaphore(1)
switch = Lightswitch()
turnstile = Semaphore(1)


def writer_func(*args):
    turnstile.acquire()
    room_empty.acquire()
    print(f"Writer {args[0]} writing...")
    turnstile.release()

    room_empty.release()


def reader_func(*args):
    turnstile.acquire()
    turnstile.release()

    switch.lock(room_empty)
    print(f"Reader {args[0]} reading...")
    switch.unlock(room_empty)


def main():
    threads = []

    for i in range(n):
        if i != 3:
            t = Thread(target=reader_func, args=[i])
        else:
            t = Thread(target=writer_func, args=[i])

        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
