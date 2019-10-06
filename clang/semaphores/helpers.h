#include <pthread.h>
#include <semaphore.h>

typedef struct {
  int counter;
} Shared;

typedef sem_t Semaphore;
typedef pthread_t Thread;

void *check_malloc(int size) {
  void *p = malloc (size);
  if (p == NULL) {
    perror (" malloc failed ");
    exit (-1);
  }
  return p;
}

//Thread make_thread(void *(*entry)(void *), Shared *shared) {
Thread make_thread(void *func(void *), Shared *shared) {
  int n;
  Thread thread;
  n = pthread_create(&thread, NULL, func, (void *)shared);
  if (n!=0){
      perror (" pthread_create failed ");
      exit ( -1);
  }
  return thread;
}

Thread make_thread_int(void *func(void *), int *value) {
  int n;
  Thread thread;
  n = pthread_create(&thread, NULL, func, (void *)value);
  if (n!=0){
      perror (" pthread_create failed ");
      exit ( -1);
  }
  return thread;
}

Thread make_thread_any(void *func(void *), void *param) {
  int n;
  Thread thread;
  n = pthread_create(&thread, NULL, func, param);
  if (n!=0){
      perror (" pthread_create failed ");
      exit ( -1);
  }
  return thread;
}

Shared *make_shared () {
  Shared *shared = check_malloc (sizeof (Shared));
  shared->counter = 0;
  return shared;
}

void join_thread (Thread thread) {
  int ret = pthread_join(thread, NULL);
  if (ret == -1) {
    perror (" pthread_join failed ");
    exit (-1);
  }
}

Semaphore *make_semaphore (const char* name, int n) {
  // Unlink named semaphore, if it exists
  int ret = sem_unlink(name);
  if (ret == -1) {
    perror(" unlinking failed ");
    //exit(-1);
  }

  // Can no longer use sem_init
  Semaphore *sem = sem_open(name, O_CREAT|O_EXCL, 0644, n);

  if (SEM_FAILED == sem) {
    perror (" sem_init failed ");
    exit ( -1);
  }
  return sem;
}

void close_semaphore(Semaphore* sem) {
  int ret = sem_close(sem);
  if (ret == -1) {
    perror (" sem_close failed ");
    exit ( -1);
  }
}

int sem_signal(Semaphore *sem) {
  return sem_post(sem);
}

int sem_signal_multi(Semaphore *sem, int n) {
  for (int i = 0; i < n; i++) {
    sem_post(sem);
  }

  return 1;
}
