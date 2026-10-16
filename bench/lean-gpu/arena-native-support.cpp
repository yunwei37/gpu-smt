// SPDX-License-Identifier: Apache-2.0
// E036 host-only diagnostic for native typed graph input. This is NOT the GPU
// backend and never supplies replacement verdicts to the native checker.
#include "closure-checker.cu"
#include <atomic>
#include <exception>
#include <thread>
#include <vector>
#include <time.h>
extern "C" uint64_t arena_thread_cpu_ns() {
    timespec value{};
    if (clock_gettime(CLOCK_THREAD_CPUTIME_ID, &value) != 0) std::terminate();
    return uint64_t(value.tv_sec)*1000000000ull + uint64_t(value.tv_nsec);
}
extern "C" void arena_support_run(Input in, Answer* answers, U threads) {
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
        Scratch scratch{terms.data(),envs.data(),levels.data(),frames.data(),cap,fcap};
        for(;;) {
            U start=next.fetch_add(64,std::memory_order_relaxed);
            if(start>=in.nd) break;
            for(U q=start;q<in.nd && q-start<64;q++) {
                Decl d=in.decls[q];
                answers[q]=d.kind>=1 && d.kind<=3
                    ?execute(in,scratch,CHECK,q,0,maxsteps)
                    :Answer{0,UNSUPPORTED,0,0,0,0,0};
            }
        }
    });
    for(auto& worker:workers) worker.join();
}
