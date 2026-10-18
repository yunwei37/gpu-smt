
#include <lean/lean.h>
extern char *getenv(const char *);
extern int open(const char *, int, ...);
extern long write(int, const void *, unsigned long);
extern int flock(int, int);
extern int close(int);
extern void abort(void);
extern void perror(const char *);
#define O_WRONLY 1
#define O_CREAT 64
#define O_APPEND 1024
#define LOCK_EX 2
#define LOCK_UN 8
LEAN_EXPORT lean_obj_res gpu_smt_cost_emit(b_lean_obj_arg s, lean_obj_arg world) {
  const char *path=getenv("FARKAS_CORPUS_FILE");
  if (path) {
    int fd=open(path,O_WRONLY|O_CREAT|O_APPEND,0644);
    if(fd<0 || flock(fd,LOCK_EX)<0) {perror("cost telemetry open/lock");abort();}
    const char *text=lean_string_cstr(s);size_t left=lean_string_size(s)-1;
    while(left) {long n=write(fd,text,left);
      if(n<=0){perror("cost telemetry write");abort();}text+=n;left-=n;}
    if(write(fd,"\n",1)!=1){perror("cost telemetry newline");abort();}
    flock(fd,LOCK_UN);close(fd);
  }
  return lean_io_result_mk_ok(lean_box(0));
}
