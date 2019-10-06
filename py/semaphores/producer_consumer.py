import time
from random import random
from threading import Thread, Semaphore


n = 5
events = []
mutex = Semaphore(1)
events_queue = Semaphore(0)

events_max_size = 3
#events_count = 0
#events_count_mutex = Semaphore(1)
#events_count_semaphore = Semaphore(0)
items = Semaphore(0)
spaces = Semaphore(events_max_size)


class Event(object):
    def __init__(self, value):
        self.value = value

    def process(self):
        print(f"I am event {self.value}")

    def __str__(self):
        return str(self.value)

'''
def atomic_events_count_mod(val):
    global events_count
    events_count_mutex.acquire()
    events_count += val
    events_count_mutex.release()
'''

def wait_for_event():
    time.sleep(2)
    event = Event(int(random() * 100))
    return event


def producer_func(*args):
    global events
    #global events_count
    #global events_max_size
    print(f"Producer {args[0]} arrived, waiting...")

    event = wait_for_event()

    '''
    events_count_mutex.acquire()
    if events_count == events_max_size:
        events_count_mutex.release()
        events_count_semaphore.acquire()
    else:
        events_count_mutex.release()
    '''

    spaces.acquire()
    mutex.acquire()
    print(f"Producer {args[0]} pushing event {event}")
    events.append(event)
    #atomic_events_count_mod(1)
    mutex.release()
    items.release()

    events_queue.release()


def consumer_func(*args):
    global events
    print(f"Consumer {args[0]} arrived, waiting...")
    events_queue.acquire()

    items.acquire()
    mutex.acquire()
    event = events.pop()
    #atomic_events_count_mod(-1)
    #events_count_semaphore.release()
    mutex.release()
    spaces.release()

    print(f"Consumer {args[0]} processing event {event}")
    event.process()


def main():
    threads = []

    for i in range(n):
        t = Thread(target=consumer_func, args=[i])
        threads.append(t)

    for i in range(n):
        t = Thread(target=producer_func, args=[i])
        threads.append(t)

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
