// SPDX-License-Identifier: Apache-2.0
// Native parallel frontend embedding. One immutable prepared seed, independent
// per-worker native incremental states. No process fork or result cache.
#include <lean/lean.h>
#include "runtime/thread.h"
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <memory>
#include <mutex>
#include <sstream>
#include <string>
#include <vector>
#include <unistd.h>
extern "C" {
void lean_initialize(void);
lean_object *initialize_bench_Lean49SharedFrontends(uint8_t,lean_object*);
lean_object *gpu_smt_lean49_start(lean_object*,lean_object*);
lean_object *gpu_smt_lean49_prepare(lean_object*,lean_object*,lean_object*);
lean_object *gpu_smt_lean49_shared_evaluate(lean_object*,lean_object*,lean_object*);
LEAN_EXPORT lean_obj_res gpu_smt_native_persist_root(lean_obj_arg root,lean_obj_arg world){
 lean_mark_persistent(root);lean_dec(world);return lean_io_result_mk_ok(lean_box(0));
}
LEAN_EXPORT lean_obj_res gpu_smt_native_checkpoint(uint64_t,lean_obj_arg stage,lean_obj_arg world){
 lean_dec(stage);lean_dec(world);return lean_io_result_mk_ok(lean_box(0));
}
}
using Clock=std::chrono::steady_clock;
static uint64_t ns(){return std::chrono::duration_cast<std::chrono::nanoseconds>(Clock::now().time_since_epoch()).count();}
static lean_object *take(lean_object *r){
 if(!lean_io_result_is_ok(r)){lean_io_result_show_error(r);lean_dec(r);return nullptr;}
 auto *v=lean_io_result_get_value(r);lean_inc(v);lean_dec(r);return v;
}
static std::mutex output_mutex;
static void emit(const std::string &s){std::lock_guard<std::mutex> guard(output_mutex);fwrite(s.data(),1,s.size(),stdout);fputc('\n',stdout);fflush(stdout);}
struct WorkerState{bool active=false;size_t ordinal=0;uint64_t start=0,deadline=0;};
int main(int argc,char **argv){
 if(argc!=4){fprintf(stderr,"usage: Lean49SharedFrontends INPUT.jsonl SYSROOT WORKERS\n");return 2;}
 size_t width=0;
 for(const char *p=argv[3];*p;p++){if(*p<'0'||*p>'9'||width>(SIZE_MAX-size_t(*p-'0'))/10)return 2;width=width*10+size_t(*p-'0');}
 if(!width)return 2;
 const uint64_t launch=ns();
 std::ifstream input(argv[1]);if(!input)return 2;
 std::vector<std::string> lines;std::string line;
 while(std::getline(input,line))if(!line.empty())lines.push_back(line);
 input.close();if(lines.empty())return 2;
 lean_initialize();lean_set_panic_messages(false);
 if(!take(initialize_bench_Lean49SharedFrontends(1,lean_io_mk_world())))return 1;
 lean_set_panic_messages(true);lean_io_mark_end_initialization();
 lean_init_task_manager_using(0);
 auto *seed=take(gpu_smt_lean49_start(lean_mk_string(argv[2]),lean_io_mk_world()));
 if(!seed)return 1;
 setenv("GPU_SMT_PARENT_PREPARATION","header-cache",1);
 lean_inc(seed);auto *prepared=take(gpu_smt_lean49_prepare(seed,lean_mk_string(lines[0].c_str()),lean_io_mk_world()));
 if(!prepared)return 1;lean_dec(seed);seed=prepared;
 // The baseline likewise makes its import/cache seed process-lifetime persistent.
 // Candidate Root updates are never marked persistent.
 lean_mark_persistent(seed);
 lean_finalize_task_manager();lean_init_task_manager();
 emit("{\"event\":\"initialized\",\"pid\":"+std::to_string(getpid())+
  ",\"seed_roots\":"+std::to_string(lean_array_size(seed))+
  ",\"inputs\":"+std::to_string(lines.size())+
  ",\"workers\":"+std::to_string(width)+",\"elapsed_ns\":"+std::to_string(ns()-launch)+"}");
 std::mutex queue_mutex;pthread_cond_t progress;pthread_condattr_t attr;
 pthread_condattr_init(&attr);pthread_condattr_setclock(&attr,CLOCK_MONOTONIC);
 pthread_cond_init(&progress,&attr);pthread_condattr_destroy(&attr);
 size_t next=0,completed=0;std::vector<WorkerState> states(width);
 std::vector<std::unique_ptr<lean::lthread>> workers;
 for(size_t id=0;id<width;id++){
  workers.emplace_back(new lean::lthread([&,id](){
   lean_object *roots=seed;lean_inc(roots);
   for(;;){
    size_t ordinal;uint64_t begin;
    {std::lock_guard<std::mutex> guard(queue_mutex);
     if(next==lines.size())break;
     ordinal=next++;begin=ns();
     states[id]={true,ordinal,begin,(ordinal?begin:launch)+UINT64_C(300000000000)};
    }
    pthread_cond_broadcast(&progress);
    emit("{\"event\":\"admitted\",\"ordinal\":"+std::to_string(ordinal)+",\"worker\":"+std::to_string(id)+
      ",\"monotonic_ns\":"+std::to_string(begin)+"}");
    lean_inc(roots);
    auto *result=gpu_smt_lean49_shared_evaluate(roots,lean_mk_string(lines[ordinal].c_str()),lean_io_mk_world());
    bool ok=lean_io_result_is_ok(result);std::string response="null";
    if(ok){
     auto *pair=take(result);auto *new_roots=lean_ctor_get(pair,0);
     lean_inc(new_roots);lean_dec(roots);roots=new_roots;
     response=lean_string_cstr(lean_ctor_get(pair,1));lean_dec(pair);
    }else{
     lean_io_result_show_error(result);lean_dec(result);
     lean_dec(roots);roots=seed;lean_inc(roots);
    }
    emit("{\"event\":\"candidate\",\"ordinal\":"+std::to_string(ordinal)+
      ",\"worker\":"+std::to_string(id)+",\"response_ready\":"+(ok?"true":"false")+
      ",\"returncode\":"+(ok?"0":"1")+",\"elapsed_ns\":"+std::to_string(ns()-begin)+
      ",\"native_response\":"+response+"}");
    {std::lock_guard<std::mutex> guard(queue_mutex);states[id].active=false;++completed;}
    pthread_cond_broadcast(&progress);
   }
   lean_dec(roots);
  }));
 }
 {
  std::unique_lock<std::mutex> lock(queue_mutex);
  while(completed<lines.size()){
   uint64_t deadline=UINT64_MAX;
   for(auto const &s:states)if(s.active&&s.deadline<deadline)deadline=s.deadline;
   if(deadline==UINT64_MAX)pthread_cond_wait(&progress,queue_mutex.native_handle());
   else{
    timespec when{time_t(deadline/UINT64_C(1000000000)),long(deadline%UINT64_C(1000000000))};
    pthread_cond_timedwait(&progress,queue_mutex.native_handle(),&when);
    uint64_t now=ns();
    for(auto const &s:states)if(s.active&&now>=s.deadline){
     emit("{\"event\":\"process_timeout\",\"ordinal\":"+std::to_string(s.ordinal)+",\"completed\":"+std::to_string(completed)+"}");
     fflush(nullptr);_Exit(124); // retain actual shared-failure boundary; never fake other results
    }
   }
  }
 }
 for(auto &worker:workers)worker->join();
 lean_finalize_task_manager();lean_dec(seed);pthread_cond_destroy(&progress);
 emit("{\"event\":\"finish\",\"inputs\":"+std::to_string(lines.size())+
  ",\"result_records\":"+std::to_string(completed)+",\"elapsed_ns\":"+std::to_string(ns()-launch)+"}");
 return 0;
}
