#from sync import Thread, Semaphore, time
from threading import Thread, Semaphore

aArrived = Semaphore(0)
bArrived = Semaphore(0)


def rendezvous_funcA(*args):
    print(f"Statement 1 from thread {args[0]}")
    aArrived.release()
    bArrived.acquire() # wait
    print(f"Statement 2 from thread {args[0]}")


def rendezvous_funcB(*args):
    print(f"Statement 1 from thread {args[0]}")
    bArrived.release()
    aArrived.acquire() # wait
    print(f"Statement 2 from thread {args[0]}")


def rendezvous():
    t1 = Thread(target=rendezvous_funcA, args=['A'])
    t2 = Thread(target=rendezvous_funcB, args=['B'])
    t1.start()
    t2.start()


if __name__ == "__main__":
    rendezvous()
