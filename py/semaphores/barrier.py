from threading import Thread, Semaphore

n = 6
count = 0
barrier = Semaphore(0)
turnstile2 = Semaphore(1)
mutex = Semaphore(1)


def barrier_func(*args):
    global count
    global n

    mutex.acquire()
    count += 1
    print(count)

    if count == n:
        barrier.release()
    mutex.release()

    print(f"Thread {args[0]} is waiting")

    # This pattern is known as a turnstile
    barrier.acquire() # waits here if negative
    barrier.release() # once it passes, it releases the next thread
    print(f"Critical section from thread {args[0]}")

    mutex.acquire()
    count -= 1
    if count == 0:
        print("Relock barrier")
        # Final thread locks first turnstile
        barrier.acquire()
        # Final thread unlocks second turnstile to allow other threads to flood through
        turnstile2.release()
    mutex.release()

    # All threads have to wait here until the final thread
    turnstile2.acquire()
    turnstile2.release()

def main():
    threads = []

    for i in range(n):
        t = Thread(target=barrier_func, args=[i])
        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
