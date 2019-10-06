#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "./helpers.h"


Semaphore *sem;


void *func(void *arg) {
  printf("Thread start\n");
  // Thread that arrives first grabs mutex and peforms action
  sem_wait(sem);
  printf("Thread inside critical area \n");
  sleep(1);
  sem_signal(sem);
  // Thread releases mutex
  printf("Thread end\n");
  pthread_exit(NULL);
}


int main() {
  int access  = 3; // three threads can access critical area at a time
  int total = 5;
  Thread threads[total];

  sem = make_semaphore("mutex", access);
  Shared *shared = make_shared();

  for (int i = 0; i < total; i++) {
    threads[i] = make_thread(func, shared);
  }

  for (int i = 0; i < total; i++) {
    join_thread(threads[i]);
  }

  printf("Goodbye, World!\n");
  return 0;
}
