import time
from random import random
from threading import Thread, Semaphore


n = 5
s = Semaphore(0)


def func1(*args):
    s.acquire()
    print(f"T {args[0]} working...")
    s.release()


def func2(*args):
    s.acquire()
    print(f"T {args[0]} working...")
    #s.release()


def main():
    threads = []

    for i in range(n):
        if i == n-1:
            t = Thread(target=func2, args=[i])
        else:
            t = Thread(target=func1, args=[i])

        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
