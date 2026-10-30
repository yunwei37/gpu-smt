#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <ucontext.h>
#include <dlfcn.h>
#include <time.h>
#ifndef NO_LEAN_FFI
#include <lean/lean.h>
#endif
typedef struct {uint64_t pc,phase;} Sample;
typedef struct {uint64_t count,capacity; Sample samples[];} Capture;
static Capture *capture; static volatile sig_atomic_t current_phase;
static void wall_exit(int number) {(void)number;_exit(124);}
static void sample_pc(int signal_number,siginfo_t *info,void *context) {
 (void)signal_number;(void)info;
 if(!capture)return;
 uint64_t index=__atomic_fetch_add(&capture->count,1,__ATOMIC_RELAXED);
 if(index<capture->capacity) {
  capture->samples[index].pc=(uint64_t)((ucontext_t*)context)->uc_mcontext.gregs[REG_RIP];
  capture->samples[index].phase=(uint64_t)current_phase;
 }
}
__attribute__((constructor)) static void start_capture(void) {
 const char *wall=getenv("M_WALL_MILLISECONDS");
 if(wall) {
  long ms=strtol(wall,NULL,10);if(ms<=0||ms>1500000)_exit(125);
  struct sigaction timeout={0};timeout.sa_handler=wall_exit;
  sigemptyset(&timeout.sa_mask);if(sigaction(SIGALRM,&timeout,NULL))_exit(126);
  struct itimerval timer={{0,0},{ms/1000,(ms%1000)*1000}};
  if(setitimer(ITIMER_REAL,&timer,NULL))_exit(127);
 }
 const char *file=getenv("M_SOFTWARE_CPU_FILE"); if(!file)return;
 size_t size=sizeof(Capture)+262144*sizeof(Sample);
 int fd=open(file,O_CREAT|O_EXCL|O_RDWR,0600);
 if(fd<0||ftruncate(fd,(off_t)size))_exit(120);
 capture=mmap(NULL,size,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);close(fd);
 if(capture==MAP_FAILED)_exit(121);
 memset(capture,0,size); capture->capacity=262144;
 struct sigaction action={0};action.sa_sigaction=sample_pc;action.sa_flags=SA_SIGINFO;
 sigemptyset(&action.sa_mask);if(sigaction(SIGPROF,&action,NULL))_exit(122);
 struct itimerval timer={{0,2000},{0,2000}};
 if(setitimer(ITIMER_PROF,&timer,NULL))_exit(123);
}
#ifndef NO_LEAN_FFI
LEAN_EXPORT lean_obj_res m_lookup_symbol(lean_obj_arg value,lean_obj_arg world) {
 (void)world;void *address=dlsym(RTLD_DEFAULT,lean_string_cstr(value));Dl_info info;
 const char *file=address&&dladdr(address,&info)?info.dli_fname:"NO_NATIVE_SYMBOL";
 lean_object *result=lean_mk_string(file);lean_dec(value);return lean_io_result_mk_ok(result);
}
LEAN_EXPORT lean_obj_res m_set_phase(uint64_t value,lean_obj_arg world) {
 (void)world;current_phase=(sig_atomic_t)value;return lean_io_result_mk_ok(lean_box(0));
}
LEAN_EXPORT lean_obj_res l_mCpuNS(lean_obj_arg world) {
 (void)world;struct timespec t;clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);
 uint64_t value=(uint64_t)t.tv_sec*1000000000ULL+(uint64_t)t.tv_nsec;
 return lean_io_result_mk_ok(lean_box_uint64(value));
}
LEAN_EXPORT lean_obj_res l_lookupSymbol(lean_obj_arg value,lean_obj_arg world) {
 return m_lookup_symbol(value,world);
}
LEAN_EXPORT lean_obj_res l_setPhase___boxed(lean_obj_arg value,lean_obj_arg world) {
 uint64_t number=lean_unbox_uint64(value);lean_dec(value);
 return m_set_phase(number,world);
}
#endif
#ifdef SAMPLER_TEST
int main(void) {
 struct timespec start,now;clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&start);
 volatile uint64_t state=1;
 do {for(int i=0;i<10000;i++)state=state*6364136223846793005ULL+1;
 clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&now);
 } while((now.tv_sec-start.tv_sec)*1000000000LL+now.tv_nsec-start.tv_nsec<200000000);
 printf("software_samples=%lu state=%lu\n",capture?capture->count:0,(uint64_t)state);
 return capture&&capture->count?0:1;
}
#endif
