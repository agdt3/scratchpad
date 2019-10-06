#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"


Semaphore *mutex;


void *func(void *arg) {
  printf("Thread start\n");
  // Thread that arrives first grabs mutex and peforms action
  sem_wait(mutex);
  printf("Thread counter %d\n", ((Shared *)arg)->counter);
  ((Shared *)arg)->counter += 1;
  printf("Thread counter %d\n", ((Shared *)arg)->counter);
  sem_signal(mutex);
  // Thread releases mutex
  printf("Thread end\n");
  pthread_exit(NULL);
}


int main() {
  mutex = make_semaphore("mutex", 1);
  Shared *shared = make_shared();

  pthread_t thread2 = make_thread(func, shared);
  pthread_t thread1 = make_thread(func, shared);

  join_thread(thread1);
  join_thread(thread2);

  printf("Goodbye, World!\n");
  return 0;
}
