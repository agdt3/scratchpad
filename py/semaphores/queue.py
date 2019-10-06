from threading import Thread, Semaphore

n = 5
leaders = 0
followers = 0
mutex = Semaphore(1)
leader_queue = Semaphore(0)
follower_queue = Semaphore(0)
rendezvous = Semaphore(0)


'''
leader1 arrives, leader_queue = 1, blocks on follower_queue
leader2 arrives, leader_queue = 2, blocks on follower_queue
leader3 arrives, leader_queue = 3, blocks on follower_queue
follower 1 arrives, follower_queue = 1, releases follower_queue
'''


def atomic_func(func):
    mutex.acquire()
    func()
    mutex.release()


def leader_func(*args):
    global leaders
    global followers
    print(f"{args[0]} arrived")

    mutex.acquire()
    if followers > 0:
        print(f"Follower count {followers}, going to signal follower")
        followers -= 1
        follower_queue.release()
    else:
        print(f"Follower count {followers}, going to wait")
        leaders += 1
        mutex.release()
        leader_queue.acquire()

    print(f"Critical code from {args[0]}")
    rendezvous.acquire()
    mutex.release()


def follower_func(*args):
    global leaders
    global followers
    print(f"{args[0]} arrived")

    mutex.acquire()
    if leaders > 0:
        print(f"Leader count {followers}, going to signal leader")
        leaders -= 1
        leader_queue.release()
    else:
        print(f"Leader count {followers}, going to wait")
        followers += 1
        mutex.release()
        follower_queue.acquire()

    print(f"Critical code from {args[0]}")
    rendezvous.release()


def main():
    threads = []

    for i in range(n):
        t = Thread(target=leader_func, args=[f"leader {i}"])
        threads.append(t)

    for i in range(n):
        t = Thread(target=follower_func, args=[f"follower {i}"])
        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
