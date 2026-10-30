/* Process-local software PC samples; installed only after Lean initialization. */
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/time.h>
#include <sys/syscall.h>
#include <ucontext.h>
#include <time.h>
#ifndef M_PC_TEST
#include <lean/lean.h>
#endif
typedef struct {uint64_t pc,phase,tid;} PCSample;
typedef struct {uint64_t count,capacity,interval_us,version;PCSample rows[];} PCData;
static PCData *pcdata;static volatile sig_atomic_t pcphase;
static void pc_handler(int number,siginfo_t *info,void *context){
 (void)number;(void)info;int saved_errno=errno;
 if(pcdata){
  uint64_t i=__atomic_fetch_add(&pcdata->count,1,__ATOMIC_RELAXED);
  if(i<pcdata->capacity){
   pcdata->rows[i].pc=(uint64_t)((ucontext_t*)context)->uc_mcontext.gregs[REG_RIP];
   pcdata->rows[i].phase=(uint64_t)pcphase;
   pcdata->rows[i].tid=(uint64_t)syscall(SYS_gettid);
  }
 }errno=saved_errno;
}
static int pc_begin(const char *path){
 if(pcdata)return 1;
 const size_t cap=262144,bytes=sizeof(PCData)+cap*sizeof(PCSample);
 int fd=open(path,O_CREAT|O_EXCL|O_RDWR,0600);
 if(fd<0)return 2;
 if(ftruncate(fd,(off_t)bytes)){close(fd);return 3;}
 pcdata=mmap(NULL,bytes,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);close(fd);
 if(pcdata==MAP_FAILED){pcdata=NULL;return 4;}
 memset(pcdata,0,bytes);pcdata->capacity=cap;pcdata->interval_us=2000;pcdata->version=1;
 char mapspath[4096];int n=snprintf(mapspath,sizeof(mapspath),"%s.maps",path);
 if(n<=0||(size_t)n>=sizeof(mapspath))return 5;
 FILE *source=fopen("/proc/self/maps","r"),*out=fopen(mapspath,"wx");
 if(!source||!out){if(source)fclose(source);if(out)fclose(out);return 6;}
 char line[8192];while(fgets(line,sizeof(line),source))fputs(line,out);fclose(source);fclose(out);
 struct sigaction action={0};action.sa_sigaction=pc_handler;action.sa_flags=SA_SIGINFO|SA_RESTART;
 sigemptyset(&action.sa_mask);if(sigaction(SIGPROF,&action,NULL))return 7;
 struct itimerval timer={{0,2000},{0,2000}};
 if(setitimer(ITIMER_PROF,&timer,NULL))return 8;
 return 0;
}
static void pc_end(void){
 struct itimerval timer={{0,0},{0,0}};setitimer(ITIMER_PROF,&timer,NULL);
 if(pcdata)msync(pcdata,sizeof(PCData)+pcdata->capacity*sizeof(PCSample),MS_SYNC);
}
#ifndef M_PC_TEST
LEAN_EXPORT lean_obj_res l_mPCStart(lean_obj_arg path,lean_obj_arg world){
 (void)world;int status=pc_begin(lean_string_cstr(path));lean_dec(path);
 if(status){fprintf(stderr,"M_PC_START_FAILURE=%d\n",status);_exit(140+status);}
 return lean_io_result_mk_ok(lean_box(0));
}
LEAN_EXPORT lean_obj_res l_mPCPhase___boxed(lean_obj_arg value,lean_obj_arg world){
 (void)world;pcphase=(sig_atomic_t)lean_unbox_uint64(value);lean_dec(value);
 return lean_io_result_mk_ok(lean_box(0));
}
LEAN_EXPORT lean_obj_res l_mPCStop(lean_obj_arg world){
 (void)world;pcphase=0;pc_end();return lean_io_result_mk_ok(lean_box(0));
}
#else
int main(int argc,char **argv){
 if(argc!=2)return 1;
 int status=pc_begin(argv[1]);if(status)return status;
 pcphase=1;struct timespec a,b;clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&a);
 volatile uint64_t value=1;
 do{
  for(int i=0;i<10000;i++)value=value*6364136223846793005ULL+1;
  clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&b);
 }while((b.tv_sec-a.tv_sec)*1000000000LL+b.tv_nsec-a.tv_nsec<200000000);
 pcphase=0;pc_end();printf("samples=%llu phase=1 value=%llu\n",
  (unsigned long long)pcdata->count,(unsigned long long)value);
 return pcdata->count?0:2;
}
#endif
