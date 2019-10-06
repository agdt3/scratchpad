#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"


Semaphore *mutex;
Semaphore *turnstyle1;
Semaphore *turnstyle2;
int n;
int n2;
int total;

Semaphore *rendezvous1;
Semaphore *rendezvous2;


void *func(void *arg) {
  int *value = (int *)(arg);
  printf("Thread start %d\n", *value);

  // Rendezvous
  if (*value == 1) {
    printf("Rendezvous Thread %d\n", *value);
    sem_signal(rendezvous1);
    sem_wait(rendezvous2);
  }
  else if (*value == 2) {
    printf("Rendezvous Thread %d\n", *value);
    sem_signal(rendezvous2);
    sem_wait(rendezvous1);
  }

  // Barrier
  for (int i = 0; i < 5; i++) {
    printf("Thread %d iteration %d\n", *value, i);

    sem_wait(mutex);
    n += 1;
    //printf("%d\n", n);
    if (n == total) {
      // Sem value can never be below 0, so no matter how ofter
      // sem_wait(turnstyle1) is called, the value of s never decrements past negative
      // the momement sem_signal(turnstyle1) is called, barrier value becomes 1
      // and lets the next thread through (which can trigger the turnstile)
      sem_signal(turnstyle1);
    }
    sem_signal(mutex);

    // turnstile
    sem_wait(turnstyle1);
    sem_signal(turnstyle1);

    printf("Critical section %d %d \n", *value, i);

    sem_wait(mutex);
    n2 -= 1;
    //printf("%d\n", n2);
    if (n2 == 0) {
      // Locks the turnstyle1 on the way out
      sem_wait(turnstyle1);
      printf("Closed the turnstyle1\n");
    }
    sem_signal(mutex);
  }

  printf("Thread end %d\n", *value);
  pthread_exit(NULL);
}


int main() {
  n = 0;
  total = 2;
  n2 = total;
  Thread threads[total];
  int thread_values[total];

  turnstyle1 = make_semaphore("sem", 0); // starts closed
  turnstyle2 = make_semaphore("sem", 1); // starts open
  mutex = make_semaphore("mutex", 1);

  rendezvous1 = make_semaphore("ren1", 0);
  rendezvous2 = make_semaphore("ren2", 0);

  for (int i = 0; i < total; i++) {
    thread_values[i] = i+1;
  }

  for (int i = 0; i < total; i++) {
   threads[i] = make_thread_int(func, &thread_values[i]);
  }

  for (int i = 0; i < total; i++) {
    join_thread(threads[i]);
  }

  close_semaphore(mutex);

  printf("Goodbye, World!\n");
  return 0;
}
