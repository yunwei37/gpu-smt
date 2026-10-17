#include <lean/lean.h>
#include <time.h>
LEAN_EXPORT lean_obj_res gpu_smt_thread_cpu_ns(lean_obj_arg w) {struct timespec t; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);return lean_io_result_mk_ok(lean_box_uint64((uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec));}
LEAN_EXPORT lean_obj_res l_GpuArithmetic_Stages_threadCpuNs(lean_obj_arg w) {return gpu_smt_thread_cpu_ns(w);}
