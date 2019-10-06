#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"

void *func(void *arg) {
  Shared *shared = (Shared *) arg;
  printf("%d\n", shared->counter);
  shared->counter = shared->counter + 1;
  printf("%d\n", shared->counter);
  pthread_exit(NULL);
}


int main() {
  Semaphore *mutex = make_semaphore("sem1", 1);

  Shared *shared = make_shared();
  pthread_t thread1 = make_thread(func, shared);
  pthread_t thread2 = make_thread(func, shared);
  join_thread(thread1);
  join_thread(thread2);
  printf("Goodbye, World!\n");
  return 0;
}
