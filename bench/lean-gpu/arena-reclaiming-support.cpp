// SPDX-License-Identifier: Apache-2.0
// E040 integrated host setup. All native checks still execute in the caller.
#include "closure-reclaiming.cu"
#include <atomic>
#include <exception>
#include <thread>
#include <vector>
#include <time.h>
#include <cstdlib>
#include <cstdio>
#include <algorithm>
extern "C" uint64_t arena_thread_cpu_ns() {
 timespec value{};
 if(clock_gettime(CLOCK_THREAD_CPUTIME_ID,&value)!=0)std::terminate();
 return uint64_t(value.tv_sec)*1000000000ull+uint64_t(value.tv_nsec);
}
extern "C" void arena_canonical_run(Input in,Answer* answers,U threads) {
 constexpr U cap=65536,fcap=8192,maxsteps=2000000;
 static_assert(sizeof(Node)==20&&sizeof(Decl)==64&&sizeof(Answer)==28);
 std::atomic<U> next{0};
 std::atomic<uint64_t> passes{0},freed_t{0},freed_e{0},freed_l{0},retry_failures{0};
 bool enabled=std::getenv("GPU_SMT_RECLAIM_OFF")==nullptr;
 std::vector<std::thread> workers;
 for(U worker=0;worker<threads;worker++)workers.emplace_back([&]{
  std::vector<Term> terms(cap);
  std::vector<Env> envs(cap);
  std::vector<LVal> levels(cap);
  std::vector<Frame> frames(fcap);
  std::vector<Slot> ts(cap*2),es(cap*2),ls(cap*2);
  std::vector<Memo> memo(cap*2);
  std::vector<unsigned char> ta(cap),ea(cap),la(cap);
  std::vector<U> tn(cap),en(cap),ln(cap);
  std::vector<GCItem> queue(cap*3);
  GCState gc{ta.data(),ea.data(),la.data(),tn.data(),en.data(),ln.data(),queue.data(),
   N,N,N,enabled,0,0,0,0,0};
  Scratch scratch{terms.data(),envs.data(),levels.data(),frames.data(),cap,fcap,
   ts.data(),es.data(),ls.data(),memo.data(),0,true,&gc};
  U old_nt=0,old_ne=0,old_nl=0;
  for(;;){
   U start=next.fetch_add(64,std::memory_order_relaxed);
   if(start>=in.nd)break;
   for(U q=start;q<in.nd&&q-start<64;q++){
    if(++scratch.epoch==0){
     std::fill(ts.begin(),ts.end(),Slot{});std::fill(es.begin(),es.end(),Slot{});
     std::fill(ls.begin(),ls.end(),Slot{});std::fill(memo.begin(),memo.end(),Memo{});
     scratch.epoch=1;
    }
    std::fill(ta.begin(),ta.begin()+old_nt,0);
    std::fill(ea.begin(),ea.begin()+old_ne,0);
    std::fill(la.begin(),la.begin()+old_nl,0);
    gc.th=gc.eh=gc.lh=N;
    Decl d=in.decls[q];
    answers[q]=d.kind>=1&&d.kind<=3?execute(in,scratch,CHECK,q,0,maxsteps):
     Answer{0,UNSUPPORTED,0,0,0,0,0};
    old_nt=answers[q].terms;old_ne=answers[q].envs;old_nl=answers[q].levels;
   }
  }
  passes.fetch_add(gc.passes,std::memory_order_relaxed);
  freed_t.fetch_add(gc.freed_t,std::memory_order_relaxed);
  freed_e.fetch_add(gc.freed_e,std::memory_order_relaxed);
  freed_l.fetch_add(gc.freed_l,std::memory_order_relaxed);
  retry_failures.fetch_add(gc.retry_failures,std::memory_order_relaxed);
 });
 for(auto& w:workers)w.join();
 std::fprintf(stderr,"{\"component\":\"E040_reclaiming_native_setup\",\"enabled\":%s,\"collections\":%llu,\"freed_terms\":%llu,\"freed_envs\":%llu,\"freed_levels\":%llu,\"same_step_insufficient_space\":%llu}\n",
  enabled?"true":"false",(unsigned long long)passes.load(),(unsigned long long)freed_t.load(),
  (unsigned long long)freed_e.load(),(unsigned long long)freed_l.load(),
  (unsigned long long)retry_failures.load());
}
