/* Observe stock Lean profileitM calls without adding a C++ exception runtime. */
#define _POSIX_C_SOURCE 200809L
#include <lean/lean.h>
#include <zlib.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <errno.h>
#define NKEY 1024
#define NFRAME 4096
#define KEYLEN 1024
typedef struct { char key[KEYLEN]; uint64_t calls,wall,cpu,exclusive; } Bucket;
typedef struct { unsigned key; uint64_t wall,cpu,children; } Frame;
typedef struct State {
 pthread_mutex_t mu;pthread_t thread;clockid_t clock;unsigned id;
 char source[128],phase[32];Bucket buckets[NKEY];Frame stack[NFRAME];
 unsigned depth,overflow_depth;uint64_t dropped_keys,truncated_keys,frame_overflows,clock_errors;
 struct State* next;
} State;
extern lean_object* __real_lean_profileit(lean_object*,lean_object*,lean_object*,lean_object*);
static pthread_mutex_t global_mu=PTHREAD_MUTEX_INITIALIZER;
static pthread_once_t once=PTHREAD_ONCE_INIT;
static State* states;
static unsigned next_id;
static gzFile output;
static int sampler_error;
static _Atomic int running=1;
static _Thread_local State* local_state;
static uint64_t ns(clockid_t clock){struct timespec t;if(clock_gettime(clock,&t))return 0;return(uint64_t)t.tv_sec*1000000000+t.tv_nsec;}
static void copystr(char* out,size_t size,const char* in){if(size){snprintf(out,size,"%s",in);}}
static void jsonstr(const char* s){
 gzputc(output,'"');for(const unsigned char* p=(const unsigned char*)s;*p;p++){
  if(*p=='"'||*p=='\\'){gzputc(output,'\\');gzputc(output,*p);}
  else if(*p<32)gzputc(output,'?');else gzputc(output,*p);
 }gzputc(output,'"');
}
static void snapshot(const char* event){
 pthread_mutex_lock(&global_mu);
 if(!output){pthread_mutex_unlock(&global_mu);return;}
 gzprintf(output,"{\"event\":\"%s\",\"pid\":%d,\"time_ns\":%llu,\"sampler_error\":%d,\"threads\":[",
  event,getpid(),(unsigned long long)ns(CLOCK_MONOTONIC),sampler_error);
 int first=1;
 for(State* s=states;s;s=s->next){
  pthread_mutex_lock(&s->mu);if(!first)gzputc(output,',');first=0;
  uint64_t cpu=ns(s->clock);if(!cpu)s->clock_errors++;
  gzprintf(output,"{\"tid\":%u,\"source_id\":",s->id);jsonstr(s->source);
  gzputs(output,",\"phase\":");jsonstr(s->phase);
  gzprintf(output,",\"thread_cpu_ns\":%llu,\"dropped_keys\":%llu,\"truncated_keys\":%llu,\"frame_overflows\":%llu,\"clock_errors\":%llu,\"totals\":{",
   (unsigned long long)cpu,(unsigned long long)s->dropped_keys,(unsigned long long)s->truncated_keys,
   (unsigned long long)s->frame_overflows,(unsigned long long)s->clock_errors);
  int f=1;
  for(unsigned i=0;i<NKEY;i++){
   Bucket* b=&s->buckets[i];if(!b->key[0]||!b->calls)continue;
   if(!f)gzputc(output,',');f=0;jsonstr(b->key);
   gzprintf(output,":[%llu,%llu,%llu,%llu]",(unsigned long long)b->calls,(unsigned long long)b->wall,
    (unsigned long long)b->cpu,(unsigned long long)b->exclusive);
  }
  gzputs(output,"},\"active\":[");f=1;
  for(unsigned i=0;i<s->depth;i++){
   Frame* b=&s->stack[i];if(!f)gzputc(output,',');f=0;
   gzputs(output,"{\"key\":");jsonstr(s->buckets[b->key].key);
   gzprintf(output,",\"start_ns\":%llu,\"start_cpu_ns\":%llu,\"completed_child_cpu_ns\":%llu}",
    (unsigned long long)b->wall,(unsigned long long)b->cpu,(unsigned long long)b->children);
  }
  gzputs(output,"]}");pthread_mutex_unlock(&s->mu);
 }
 gzputs(output,"]}\n");gzflush(output,Z_SYNC_FLUSH);pthread_mutex_unlock(&global_mu);
}
static void finish(void){
 atomic_store(&running,0);snapshot("exit");
 pthread_mutex_lock(&global_mu);if(output){gzclose(output);output=NULL;}pthread_mutex_unlock(&global_mu);
}
static void* sampler(void* unused){
 (void)unused;struct timespec t={1,0};
 while(atomic_load(&running)){nanosleep(&t,NULL);snapshot("sample");}return NULL;
}
static void initialize(void){
 const char* dir=getenv("GPU_SMT_NATIVE_PROFILE_DIRECTORY");if(!dir)return;
 char path[4096];snprintf(path,sizeof(path),"%s/%d.jsonl.gz",dir,getpid());
 output=gzopen(path,"wb1");if(!output)return;
 pthread_t thread;sampler_error=pthread_create(&thread,NULL,sampler,NULL);
 if(!sampler_error)pthread_detach(thread);atexit(finish);
}
static State* state(void){
 pthread_once(&once,initialize);if(!output)return NULL;
 if(local_state)return local_state;
 State* s=calloc(1,sizeof(*s));if(!s)return NULL;
 pthread_mutex_init(&s->mu,NULL);s->thread=pthread_self();pthread_getcpuclockid(s->thread,&s->clock);
 copystr(s->source,sizeof(s->source),"unknown");copystr(s->phase,sizeof(s->phase),"unknown");
 pthread_mutex_lock(&global_mu);s->id=++next_id;s->next=states;states=s;pthread_mutex_unlock(&global_mu);
 local_state=s;return s;
}
static void field(const char* text,const char* key,char* out,size_t size){
 char needle[80];snprintf(needle,sizeof(needle),"\"%s\"",key);
 const char* p=strstr(text,needle);copystr(out,size,"unknown");if(!p)return;
 p=strchr(p,':');if(!p)return;p++;while(*p==' '||*p=='\t')p++;if(*p!='"')return;
 const char* e=strchr(++p,'"');if(!e)return;size_t n=(size_t)(e-p);if(n>=size)n=size-1;memcpy(out,p,n);out[n]=0;
}
static void ownership(char* source,size_t n,char* phase,size_t m){
 const char* dir=getenv("GPU_SMT_MEMORY_DIRECTORY");
 copystr(source,n,"unknown");copystr(phase,m,"unknown");if(!dir)return;
 int pids[]={getpid(),getppid()};
 for(unsigned i=0;i<2;i++){
  char path[4096],text[4096];snprintf(path,sizeof(path),"%s/activity/%d.json",dir,pids[i]);
  FILE* f=fopen(path,"r");if(!f)continue;size_t bytes=fread(text,1,sizeof(text)-1,f);fclose(f);text[bytes]=0;
  field(text,"source_id",source,n);field(text,"phase",phase,m);return;
 }
}
static size_t name_string(lean_object* name,char* text,size_t size){
 if(!size)return 0;text[0]=0;if(lean_is_scalar(name))return 0;
 size_t used=name_string(lean_ctor_get(name,0),text,size);
 const char* part=lean_obj_tag(name)==1?lean_string_cstr(lean_ctor_get(name,1)):"#";
 int n=snprintf(text+used,size-used,"%s%s",used?".":"",part);
 return n<0?used:used+(size_t)n>=size?size-1:used+(size_t)n;
}
static unsigned bucket(State* s,const char* key){
 uint64_t h=1469598103934665603ULL;
 for(const unsigned char* p=(const unsigned char*)key;*p;p++)h=(h^*p)*1099511628211ULL;
 for(unsigned j=0;j<NKEY-1;j++){
  unsigned i=1+(unsigned)((h+j)%(NKEY-1));Bucket* b=&s->buckets[i];
  if(!b->key[0]){copystr(b->key,sizeof(b->key),key);return i;}
  if(!strcmp(b->key,key))return i;
 }
 s->dropped_keys++;copystr(s->buckets[0].key,KEYLEN,"unknown|diagnostic key overflow");return 0;
}
lean_object* __wrap_lean_profileit(lean_object* category,lean_object* opts,lean_object* fn,lean_object* decl){
 if(!getenv("GPU_SMT_NATIVE_PROFILE_DIRECTORY"))return __real_lean_profileit(category,opts,fn,decl);
 State* s=state();if(!s)return __real_lean_profileit(category,opts,fn,decl);
 char key[KEYLEN],name[KEYLEN];name_string(decl,name,sizeof(name));
 int length=snprintf(key,sizeof(key),"%s|%s",lean_string_cstr(category),name);
 pthread_mutex_lock(&s->mu);int outer=s->depth==0&&s->overflow_depth==0;pthread_mutex_unlock(&s->mu);
 if(outer){
  char source[128],phase[32];ownership(source,sizeof(source),phase,sizeof(phase));
  pthread_mutex_lock(&s->mu);int changed=strcmp(s->source,source)||strcmp(s->phase,phase);pthread_mutex_unlock(&s->mu);
  if(changed){snapshot("source_boundary");pthread_mutex_lock(&s->mu);
   copystr(s->source,sizeof(s->source),source);copystr(s->phase,sizeof(s->phase),phase);
   memset(s->buckets,0,sizeof(s->buckets));pthread_mutex_unlock(&s->mu);}
 }
 pthread_mutex_lock(&s->mu);
 if(length<0||length>=KEYLEN)s->truncated_keys++;
 int dropped=s->depth>=NFRAME||s->overflow_depth;
 if(dropped){s->frame_overflows++;s->overflow_depth++;}
 else{unsigned k=bucket(s,key);s->stack[s->depth++]=(Frame){k,ns(CLOCK_MONOTONIC),ns(CLOCK_THREAD_CPUTIME_ID),0};}
 pthread_mutex_unlock(&s->mu);
 lean_object* result=__real_lean_profileit(category,opts,fn,decl);
 uint64_t cpu=ns(CLOCK_THREAD_CPUTIME_ID),wall=ns(CLOCK_MONOTONIC);
 pthread_mutex_lock(&s->mu);
 if(dropped)s->overflow_depth--;
 else{
  Frame f=s->stack[--s->depth];uint64_t c=cpu-f.cpu;Bucket* b=&s->buckets[f.key];
  b->calls++;b->wall+=wall-f.wall;b->cpu+=c;b->exclusive+=c>=f.children?c-f.children:0;
  if(s->depth)s->stack[s->depth-1].children+=c;
 }
 pthread_mutex_unlock(&s->mu);if(outer)snapshot("outer_return");return result;
}
