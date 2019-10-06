import time
from random import random
from threading import Thread, Semaphore

n = 5
# protecc readers from writer
readers = 0
readers_mutex = Semaphore(1)

room_empty = Semaphore(1)


def writer_func(*args):
    room_empty.acquire()
    print(f"Writer {args[0]} writing...")
    room_empty.release()


def reader_func(*args):
    global readers

    readers_mutex.acquire()
    if readers == 0:
        room_empty.acquire()
    readers += 1
    readers_mutex.release()

    print(f"Reader {args[0]} reading...")

    readers_mutex.acquire()
    readers -= 1
    if readers == 0:
        room_empty.release()
    readers_mutex.release()


def main():
    threads = []

    for i in range(n):
        if i % 2 == 0:
            t = Thread(target=reader_func, args=[i])
        else:
            t = Thread(target=writer_func, args=[i])

        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
