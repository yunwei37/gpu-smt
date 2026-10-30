/* Native timing for stock lean_profileit; no Lean-object allocation in callbacks.
   Experimental, serial frontend only. Delegates the original function unchanged. */
#define _GNU_SOURCE
#include <lean/lean.h>
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>
typedef lean_object *(*ProfileFn)(lean_object*,lean_object*,lean_object*,lean_object*);
static FILE *events; static int recording; static uint64_t serial;
static _Thread_local uint64_t stack[4096];static _Thread_local unsigned depth;
static uint64_t ns(clockid_t clock){struct timespec t;clock_gettime(clock,&t);return(uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec;}
static void quoted(const char *s){
 fputc('"',events);
 for(const unsigned char *p=(const unsigned char*)s;*p;p++){
  if(*p=='"'||*p=='\\')fputc('\\',events);
  if(*p<32)fprintf(events,"\\u%04x",*p);else fputc(*p,events);
 }fputc('"',events);
}
static void close_events(void){if(events){fclose(events);events=NULL;}}
__attribute__((constructor)) static void diagnostic_begin(void){
 const char *file=getenv("M_TACTIC_TRACE_FILE");
 if(!file)return;
 events=fopen(file,"wx");if(!events)_exit(132);
 atexit(close_events);recording=1;
}
LEAN_EXPORT lean_obj_res l_mTraceMode(lean_obj_arg value,lean_obj_arg world){
 (void)world;
 if(!events){
  const char *file=getenv("M_TACTIC_TRACE_FILE");
  if(!file)_exit(131);
  events=fopen(file,"wx");if(!events)_exit(132);
  atexit(close_events);
 }
 fprintf(events,"{\"event\":\"source\",\"name\":");quoted(lean_string_cstr(value));
 fprintf(events,",\"open_frames\":%u}\n",depth);fflush(events);
 recording=strstr(lean_string_cstr(value),"|observe")!=NULL;
 lean_dec(value);return lean_io_result_mk_ok(lean_box(0));
}
static size_t name_text(lean_object *n,char *buf,size_t cap){
 if(!cap)return 0;buf[0]=0;if(lean_is_scalar(n))return 0;
 size_t used=name_text(lean_ctor_get(n,0),buf,cap);
 const char *piece=lean_obj_tag(n)==1?lean_string_cstr(lean_ctor_get(n,1)):"#";
 int len=snprintf(buf+used,cap-used,"%s%s",used?".":"",piece);
 return len<0?used:used+(size_t)len>=cap?cap-1:used+(size_t)len;
}
#ifdef M_PROFILE_STATIC_WRAP
extern lean_object *__real_lean_profileit(lean_object*,lean_object*,lean_object*,lean_object*);
#define M_PROFILE_NAME __wrap_lean_profileit
#else
#define M_PROFILE_NAME lean_profileit
#endif
LEAN_EXPORT lean_object *M_PROFILE_NAME(lean_object *cat,lean_object *opts,lean_object *fn,lean_object *decl){
#ifdef M_PROFILE_STATIC_WRAP
 ProfileFn original=__real_lean_profileit;
#else
 static ProfileFn original;
 if(!original){original=(ProfileFn)dlsym(RTLD_NEXT,"lean_profileit");if(!original)_exit(133);}
#endif
 if(!recording||(strcmp(lean_string_cstr(cat),"tactic execution") &&
 strcmp(lean_string_cstr(cat),"type checking") && strcmp(lean_string_cstr(cat),"elaboration")))
  return original(cat,opts,fn,decl);
 if(depth>=4096)_exit(134);
 static _Thread_local char name[2048];name_text(decl,name,sizeof(name));
 uint64_t id=++serial,parent=depth?stack[depth-1]:0;
 stack[depth++]=id;
 uint64_t wall=ns(CLOCK_MONOTONIC),cpu=ns(CLOCK_THREAD_CPUTIME_ID);
 fprintf(events,"{\"event\":\"enter\",\"id\":%llu,\"parent\":%llu,\"thread\":%ld,\"kind\":",
  (unsigned long long)id,(unsigned long long)parent,(long)syscall(SYS_gettid));quoted(name);fprintf(events,",\"category\":");quoted(lean_string_cstr(cat));
 fprintf(events,",\"wall_ns\":%llu,\"cpu_ns\":%llu}\n",(unsigned long long)wall,(unsigned long long)cpu);
 fflush(events);lean_object *result=original(cat,opts,fn,decl);
 wall=ns(CLOCK_MONOTONIC);cpu=ns(CLOCK_THREAD_CPUTIME_ID);
 fprintf(events,"{\"event\":\"exit\",\"id\":%llu,\"wall_ns\":%llu,\"cpu_ns\":%llu,\"return_tag\":%u}\n",
  (unsigned long long)id,(unsigned long long)wall,(unsigned long long)cpu,(unsigned)(lean_is_scalar(result)?UINT32_MAX:lean_obj_tag(result)));
 fflush(events);--depth;return result;
}
