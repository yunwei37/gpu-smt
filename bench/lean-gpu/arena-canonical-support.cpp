// SPDX-License-Identifier: Apache-2.0
// E037 host-only diagnostic for native typed graph input. This is NOT the GPU
// backend and never supplies replacement verdicts to the native checker.
#include "closure-canonical.cu"
#include <atomic>
#include <exception>
#include <thread>
#include <vector>
#include <time.h>
#include <cstdlib>
#include <algorithm>
extern "C" uint64_t arena_thread_cpu_ns() {
    timespec value{};
    if (clock_gettime(CLOCK_THREAD_CPUTIME_ID, &value) != 0) std::terminate();
    return uint64_t(value.tv_sec)*1000000000ull + uint64_t(value.tv_nsec);
}
extern "C" void arena_canonical_run(Input in, Answer* answers, U threads) {
    // Same bounded interpreter defaults as closure-resident.py. Exhaustion is
    // an unsupported prospective task, never native rejection.
    constexpr U cap=65536, fcap=8192, maxsteps=2000000;
    static_assert(sizeof(Node)==20 && sizeof(Decl)==64 && sizeof(Answer)==28);
    std::atomic<U> next{0};
    std::vector<std::thread> workers;
    for(U worker=0;worker<threads;worker++) workers.emplace_back([&] {
        std::vector<Term> terms(cap);
        std::vector<Env> envs(cap);
        std::vector<LVal> levels(cap);
        std::vector<Frame> frames(fcap);
        std::vector<Slot> ts(cap*2),es(cap*2),ls(cap*2);
        std::vector<Memo> memo(cap*2);
        Scratch scratch{terms.data(),envs.data(),levels.data(),frames.data(),cap,fcap,
          ts.data(),es.data(),ls.data(),memo.data(),0,std::getenv("GPU_SMT_CANONICAL_OFF")==nullptr};
        for(;;) {
            U start=next.fetch_add(64,std::memory_order_relaxed);
            if(start>=in.nd) break;
            for(U q=start;q<in.nd && q-start<64;q++) {
                if(++scratch.epoch==0){
                  std::fill(ts.begin(),ts.end(),Slot{});std::fill(es.begin(),es.end(),Slot{});
                  std::fill(ls.begin(),ls.end(),Slot{});std::fill(memo.begin(),memo.end(),Memo{});
                  scratch.epoch=1;
                }
                Decl d=in.decls[q];
                answers[q]=d.kind>=1 && d.kind<=3
                    ?execute(in,scratch,CHECK,q,0,maxsteps)
                    :Answer{0,UNSUPPORTED,0,0,0,0,0};
            }
        }
    });
    for(auto& worker:workers) worker.join();
}
