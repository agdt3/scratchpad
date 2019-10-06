#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"


Semaphore *ren1;
Semaphore *ren2;


void *func1(void *arg) {
  printf("A1 critical section\n");
  // If thread1 arrives first
  // it unlocks ren 1
  // and waits on thread2 to unlock ren2
  sem_signal(ren1);
  sem_wait(ren2);
  printf("A2 critical section\n");
  pthread_exit(NULL);
}


void *func2(void *arg) {
  printf("B1 critical section\n");
  // If thread2 arrives first
  // it unlocks ren2
  // and waits on thread1 to unlock ren1
  sem_signal(ren2);
  sem_wait(ren1);
  printf("B2 critical section\n");
  pthread_exit(NULL);
}


int main() {
  ren1 = make_semaphore("ren1", 0);
  ren2 = make_semaphore("ren2", 0);

  Shared *shared = make_shared();
  pthread_t thread1 = make_thread(func1, shared);
  pthread_t thread2 = make_thread(func2, shared);
  join_thread(thread1);
  join_thread(thread2);
  printf("Goodbye, World!\n");
  return 0;
}
