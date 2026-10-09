// Thin Linux experiment hook for Lean 4.21.0. This is a qualified candidate
// boundary, not a general guarantee for arbitrary Lean plugins or FFI code.
#include <lean/lean.h>
#include <cerrno>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <dirent.h>
#include <sys/wait.h>
#include <sys/syscall.h>
#include <unistd.h>

int prepared_uv_stop();
int prepared_uv_restart(bool child);

static unsigned own_thread_count() {
    DIR *d = opendir("/proc/self/task");
    if (!d) return 0;
    unsigned n = 0;
    while (dirent *e = readdir(d)) {
        if (std::isdigit(static_cast<unsigned char>(e->d_name[0]))) ++n;
    }
    closedir(d);
    return n;
}

extern "C" lean_obj_res gpu_smt_prepared_fork(uint32_t parent_workers,
                                               lean_obj_arg) {
    // Caller: native main thread, complete snapshot traversal and checked
    // environment already forced, no managed task wrapping this call.
    // No Lean allocation/destruction/callback in the manager-free region.
    if (syscall(SYS_gettid) != getpid() || parent_workers == 0) {
        return lean_io_result_mk_ok(lean_box_uint64((uint64_t(1) << 63) | EINVAL));
    }
    int uv_error = prepared_uv_stop();
    if (uv_error) {
        std::fprintf(stderr, "prepared fork: UV stop refused/error=%d\n", uv_error);
        return lean_io_result_mk_ok(lean_box_uint64((uint64_t(1) << 63) | uint32_t(uv_error)));
    }
    lean_finalize_task_manager();
    unsigned threads = own_thread_count();
    pid_t pid = -1;
    int failure = EBUSY;
    if (threads == 1) {
        pid = fork();
        failure = errno;
    }
    lean_init_task_manager_using(pid == 0 ? 1 : parent_workers);
    uv_error = prepared_uv_restart(pid == 0);
    if (uv_error) {
        std::fprintf(stderr, "prepared fork: UV restart failure=%d pid=%d\n", uv_error, int(pid));
        if (pid == 0) _exit(70);
        failure = uv_error;
        pid = -1;
    }
    std::fprintf(stderr, "prepared fork: stopped_threads=%u fork_result=%d error=%d\n",
                 threads, int(pid), pid < 0 ? failure : 0);
    // A native result is allocated only after reinitialization in both paths.
    // Encode pid or error without depending on Lean filename-error ABI.
    uint64_t result = pid < 0
        ? (uint64_t(1) << 63) | (uint64_t(threads) << 32) | uint32_t(failure)
        : uint64_t(pid);
    return lean_io_result_mk_ok(lean_box_uint64(result));
}

extern "C" lean_obj_res gpu_smt_wait_child(lean_obj_arg) {
    int status = 0;
    pid_t pid;
    do { pid = waitpid(-1, &status, 0); } while (pid < 0 && errno == EINTR);
    uint64_t result = pid < 0
        ? (uint64_t(1) << 63) | uint32_t(errno)
        : (uint64_t(pid) << 32) | uint32_t(status);
    return lean_io_result_mk_ok(lean_box_uint64(result));
}

extern "C" lean_obj_res gpu_smt_own_pid(lean_obj_arg) {
    return lean_io_result_mk_ok(lean_box_uint32(uint32_t(getpid())));
}
