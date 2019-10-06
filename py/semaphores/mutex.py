from threading import Thread, Semaphore

s = Semaphore(3)
count = 0


def func(*args):
    s.acquire()
    global count
    count = count + 1
    print(f"Incremented count to {count} from thread {args[0]}")
    s.release()


if __name__ == "__main__":
    n = 5
    threads = []
    for i in range(n):
        t = Thread(target=func, args=[i])
        threads.append(t)

    for t in threads:
        t.start()
