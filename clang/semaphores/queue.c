#include <stdio.h>
#include <stdlib.h>
#include "./helpers.h"

int leaders = followers = 0;
Semaphore *mutex;
Semaphore *leader_queue;
Semaphore *follower_queue;
Semaphore *rendezvous;


void *func1(void *arg) {
  int num = *(int *)arg;

  printf("Leader %d arrives\n", num);

  sem_wait(mutex);
  leaders++;
  sem_signal(mutex);

  sem_signal(follower_queue);
  sem_wait(leader_queue);

  printf("Leader %d dances\n", num);

  sem_wait(mutex);
  leaders--;
  sem_signal(mutex);

  //printf("Thread end\n");
  pthread_exit(NULL);
}

void *func2(void *arg) {
  int num = *(int *)arg;

  printf("Follower %d arrives\n", num);

  sem_wait(mutex);
  followers++;
  sem_signal(mutex);

  sem_signal(leader_queue);
  sem_wait(follower_queue);

  printf("Follower %d dances\n", num);

  sem_wait(mutex);
  followers--;
  sem_signal(mutex);

  //printf("Thread end\n");
  pthread_exit(NULL);
}

int main() {
  int total = 10;
  Thread threads[total * 2];
  int thread_number[total];

  mutex = make_semaphore("mutex", 1);
  leader_queue = make_semaphore("leader", 0);
  follower_queue = make_semaphore("follower", 0);
  rendezvous = make_semaphore("rendezvous", 0);

  for (int i = 0; i < total/2; i++) {
    // leaders
    thread_number[i] = i+1;
    threads[i] = make_thread_int(func1, &thread_number[i]);
  }

  for (int i = total/2; i < total; i++) {
    // followers
    thread_number[i] = i+1;
    threads[i] = make_thread_int(func2, &thread_number[i]);
  }

  for (int i = 0; i < total; i++) {
    join_thread(threads[i]);
  }

  close_semaphore(leader_queue);
  close_semaphore(follower_queue);

  printf("Goodbye, World!\n");
  return 0;
}
