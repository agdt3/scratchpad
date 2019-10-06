#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"


Semaphore *mutex;
Semaphore *barrier;
int n;
int total;


void *func(void *arg) {
  printf("Thread start\n");

  sem_wait(mutex);
  n += 1;
  printf("%d\n", n);
  sem_signal(mutex);

  if (n == total) {
    // Sem value can never be below 0, so no matter how ofter
    // sem_wait(barrier) is called, the value of s never decrements past negative
    // the momement sem_signal(barrier) is called, barrier value becomes 1
    // and lets the next thread through (which can trigger the turnstile)
    sem_signal(barrier);
  }

  // turnstile
  sem_wait(barrier);
  sem_signal(barrier);

  printf("Critical section\n");
  printf("Thread end\n");
  pthread_exit(NULL);
}


int main() {
  n = 0;
  total = 5;
  Thread threads[total];

  barrier = make_semaphore("sem", 0);
  mutex = make_semaphore("mutex", 1);
  Shared *shared = make_shared();

  for (int i = 0; i < total; i++) {
    threads[i] = make_thread(func, shared);
  }

  for (int i = 0; i < total; i++) {
    join_thread(threads[i]);
  }

  close_semaphore(mutex);

  printf("Goodbye, World!\n");
  return 0;
}
