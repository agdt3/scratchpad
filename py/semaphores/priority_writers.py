import time
from random import random
from threading import Thread, Semaphore
from lightswitch import Lightswitch

n = 5
no_readers = Semaphore(1)
reader_switch = Lightswitch()

no_writers = Semaphore(1)
writer_switch = Lighthouse()


def writer_func(*args):
    writer_switch.lock(no_writers)
    reader_switch.lock(no_readers)
    print(f"Writer {args[0]} writing...")
    reader_switch.unlock(no_readers)
    writer_switch.unlock(no_writers)


def reader_func(*args):
    reader_switch.lock(no_readers)
    print(f"Reader {args[0]} reading...")
    reader_switch.unlock(no_readers)


def main():
    threads = []

    for i in range(n):
        if i == 2 or i == 3:
            t = Thread(target=writer_func, args=[i])
        else:
            t = Thread(target=reader_func, args=[i])

        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
