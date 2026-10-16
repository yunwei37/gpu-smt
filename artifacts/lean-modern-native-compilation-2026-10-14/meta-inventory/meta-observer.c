#define _GNU_SOURCE
#include <lean/lean.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <time.h>

extern uint64_t lean_expr_data(b_lean_obj_arg);
extern lean_obj_res __real_lean_is_expr_def_eq(
    lean_obj_arg, lean_obj_arg, lean_obj_arg,
    lean_obj_arg, lean_obj_arg, lean_obj_arg);

enum { CATEGORIES = 64 };
struct meta_stats {
    uint64_t magic, version, pid, tid, depth, max_depth, clock_errors, created_ns;
    uint64_t all_entered[CATEGORIES], all_completed[CATEGORIES];
    uint64_t outer_entered[CATEGORIES], outer_completed[CATEGORIES];
    uint64_t outer_cpu_ns[CATEGORIES];
};
static _Thread_local volatile struct meta_stats *stats;
static _Thread_local unsigned depth;
static _Thread_local int initialized;

static uint64_t as_ns(struct timespec t) {
    return (uint64_t)t.tv_sec * UINT64_C(1000000000) + (uint64_t)t.tv_nsec;
}
static void initialize_stats(void) {
    initialized = 1;
    const char *dir = getenv("GPU_SMT_META_OBSERVER_DIR");
    if (!dir || !*dir) return;
    long tid = syscall(SYS_gettid);
    char path[4096];
    int n = snprintf(path, sizeof(path), "%s/meta-%ld-%ld.bin",
                     dir, (long)getpid(), tid);
    if (n < 0 || n >= (int)sizeof(path)) {
        fprintf(stderr, "META_OBSERVER_INIT_ERROR path_length\n"); return;
    }
    int fd = open(path, O_RDWR | O_CREAT | O_EXCL | O_CLOEXEC, 0666);
    if (fd < 0) {
        fprintf(stderr, "META_OBSERVER_INIT_ERROR open %d\n", errno); return;
    }
    if (ftruncate(fd, sizeof(struct meta_stats)) != 0) {
        fprintf(stderr, "META_OBSERVER_INIT_ERROR truncate %d\n", errno);
        close(fd); return;
    }
    void *p = mmap(NULL, sizeof(struct meta_stats), PROT_READ | PROT_WRITE,
                   MAP_SHARED, fd, 0);
    close(fd);
    if (p == MAP_FAILED) {
        fprintf(stderr, "META_OBSERVER_INIT_ERROR mmap %d\n", errno); return;
    }
    stats = p;
    stats->magic = UINT64_C(0x47534d5444455131);
    stats->version = 1;
    stats->pid = (uint64_t)getpid(); stats->tid = (uint64_t)tid;
    struct timespec now;
    if (clock_gettime(CLOCK_MONOTONIC, &now) == 0)
        stats->created_ns = as_ns(now);
}

LEAN_EXPORT lean_obj_res __wrap_lean_is_expr_def_eq(
        lean_obj_arg t, lean_obj_arg s, lean_obj_arg a,
        lean_obj_arg b, lean_obj_arg c, lean_obj_arg d) {
    if (!initialized) initialize_stats();
    if (!stats) return __real_lean_is_expr_def_eq(t,s,a,b,c,d);
    /* Expr.data is borrowed. The exported has*Ex helpers consume their Expr;
       using the same cached data bits avoids changing reference ownership. */
    uint64_t data = lean_expr_data(t) | lean_expr_data(s);
    unsigned cat = ((data >> 41) & 1u)
                 | (((data >> 42) & 1u) << 1)
                 | (((data >> 40) & 1u) << 2)
                 | ((data >> 44 ? 1u : 0u) << 3)
                 | (((data >> 43) & 1u) << 4)
                 | ((t == s ? 1u : 0u) << 5);
    int outer = (depth == 0);
    stats->all_entered[cat]++;
    stats->depth = ++depth;
    if (depth > stats->max_depth) stats->max_depth = depth;
    struct timespec start, stop;
    int timed = 0;
    if (outer) {
        stats->outer_entered[cat]++;
        timed = (clock_gettime(CLOCK_THREAD_CPUTIME_ID, &start) == 0);
        if (!timed) stats->clock_errors++;
    }
    lean_obj_res result = __real_lean_is_expr_def_eq(t,s,a,b,c,d);
    if (outer) {
        if (timed && clock_gettime(CLOCK_THREAD_CPUTIME_ID, &stop) == 0) {
            uint64_t first = as_ns(start), last = as_ns(stop);
            if (last >= first) stats->outer_cpu_ns[cat] += last - first;
            else stats->clock_errors++;
        } else if (timed) stats->clock_errors++;
        stats->outer_completed[cat]++;
    }
    stats->all_completed[cat]++;
    stats->depth = --depth;
    return result;
}
