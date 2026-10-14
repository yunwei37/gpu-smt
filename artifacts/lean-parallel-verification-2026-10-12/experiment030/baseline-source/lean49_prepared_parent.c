/* A native boundary prototype, not a qualified service/fork contract.
 * Parent: import-only by default; optional full snapshot preparation uses
 * an ordinary task manager, finishes visible tasks, and tears the manager down.
 * Child: ordinary one-worker manager, untouched native frontend, disposable.
 * Guard refuses foreign threads/descriptors. Counts alone do not prove safety.
 */
#define _GNU_SOURCE
#include <lean/lean.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

extern void lean_initialize(void);
extern lean_object *initialize_Lean49PreparedBranches(uint8_t, lean_object *);
extern lean_object *gpu_smt_lean49_start(lean_object *, lean_object *);
extern lean_object *gpu_smt_lean49_prepare(lean_object *, lean_object *, lean_object *);
extern lean_object *gpu_smt_lean49_execute(lean_object *, lean_object *, lean_object *);
extern lean_object *gpu_smt_lean49_stream(lean_object *, lean_object *);
/* Native process-lifetime retention avoids reference-count writes to the
 * shared prepared graph. Ordinary new candidate state remains reclaimable. */
LEAN_EXPORT lean_obj_res gpu_smt_native_persist_root(lean_obj_arg root, lean_obj_arg world) {
    (void)world;
    lean_mark_persistent(root);
    return lean_io_result_mk_ok(lean_box(0));
}

static volatile sig_atomic_t stopped = 0;
static int snapshot_mode = 0;
static int snapshot_runtime_active = 0;
static int in_candidate_child = 0;
static void stop_signal(int number) { stopped = number; }

/* Optional fault-only checkpoint. Default executions have no pause or output.
 * A configured stage stops this whole owned child process, never the prepared
 * parent. The external owner must verify this marker/TID/stop before killing.
 * This is not a timing sample or proof of arbitrary cancellation safety. */
LEAN_EXPORT lean_obj_res gpu_smt_native_checkpoint(uint64_t index, lean_obj_arg stage, lean_obj_arg world) {
    /* Both methods prepare imports/cache synchronously. The snapshot stream
     * starts the ordinary candidate scheduler at the same frontend boundary. */
    if (snapshot_mode && !snapshot_runtime_active) {
        lean_init_task_manager(); snapshot_runtime_active = 1;
    }
    const char *target = getenv("GPU_SMT_CHECKPOINT_INDEX");
    const char *point = getenv("GPU_SMT_CHECKPOINT_STAGE");
    unsigned long long number = (unsigned long long)index;
    char expected[32]; snprintf(expected, sizeof(expected), "%llu", number);
    if (in_candidate_child && target && point && !strcmp(target, expected) &&
        !strcmp(point, lean_string_cstr(stage))) {
        fprintf(stderr, "{\"gpu_smt_checkpoint\":true,\"source_index\":%llu,\"pid\":%d,\"stage\":\"%s\"}\n",
                number, getpid(), point); fflush(stderr);
        raise(SIGSTOP);
    }
    lean_dec(stage); lean_dec(world);
    return lean_io_result_mk_ok(lean_box(0));
}

static uint64_t nanos(void) {
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC, &t)) abort();
    return (uint64_t)t.tv_sec * 1000000000u + t.tv_nsec;
}

static int write_all(int fd, const char *data, size_t size) {
    while (size) {
        ssize_t n = write(fd, data, size);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        data += n; size -= (size_t)n;
    }
    return 0;
}

static lean_object *take_value(lean_object *result) {
    if (!lean_io_result_is_ok(result)) {
        lean_io_result_show_error(result);
        lean_dec(result);
        return NULL;
    }
    lean_object *value = lean_io_result_get_value(result);
    lean_inc(value); lean_dec(result);
    return value;
}

/* Optional full preparation is not a general fork barrier. Its visible task
 * checks precede teardown; the existing TID/FD guards still refuse any residue. */
static lean_object *prepare_native(lean_object *roots, const char *line) {
    const char *mode = getenv("GPU_SMT_PARENT_PREPARATION");
    /* Real published headers may allocate native promises. Supply the ordinary
     * manager during preparation, then use its existing owned teardown before
     * the unchanged parent TID/FD checks and disposable branch launch. */
    int full = mode && (!strcmp(mode, "full") || !strcmp(mode, "header"));
    if (full) lean_init_task_manager();
    lean_object *result = gpu_smt_lean49_prepare(roots, lean_mk_string(line), lean_io_mk_world());
    if (full) lean_finalize_task_manager();
    return result;
}

static unsigned tids(void) {
    DIR *d = opendir("/proc/self/task");
    if (!d) return UINT_MAX;
    unsigned count = 0;
    struct dirent *entry;
    while ((entry = readdir(d))) if (entry->d_name[0] != '.') ++count;
    closedir(d); return count;
}

static unsigned foreign_fds(void) {
    DIR *d = opendir("/proc/self/fd");
    if (!d) return UINT_MAX;
    int own = dirfd(d);
    unsigned count = 0;
    struct dirent *entry;
    while ((entry = readdir(d))) {
        if (entry->d_name[0] == '.') continue;
        long fd = 0; int valid = 1;
        for (const char *p = entry->d_name; *p; ++p) {
            if (*p < '0' || *p > '9' || fd > INT_MAX / 10) { valid = 0; break; }
            fd = fd * 10 + (*p - '0');
        }
        if (!valid || (fd > 2 && fd != own)) ++count;
    }
    closedir(d); return count;
}

static int append(char **data, size_t *length, const char *bytes, size_t count) {
    if (count > SIZE_MAX - *length - 1) return -1;
    char *next = realloc(*data, *length + count + 1);
    if (!next) return -1;
    *data = next;
    memcpy(next + *length, bytes, count); *length += count;
    next[*length] = 0; return 0;
}

static void print_hex(const char *data, size_t size) {
    static const char digits[] = "0123456789abcdef";
    for (size_t i = 0; i < size; ++i) {
        unsigned char b = (unsigned char)data[i];
        putchar(digits[b >> 4]); putchar(digits[b & 15]);
    }
}

static int serial_main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: Lean49PreparedBranches INPUT.jsonl SYSROOT\n");
        return 2;
    }
    /* Read and close the ordinary offline input before any branch. No FILE
     * buffer/descriptor is inherited as a second candidate input reader. */
    FILE *input = fopen(argv[1], "r");
    if (!input) { perror("input"); return 2; }
    char **lines = NULL, *line = NULL; size_t count = 0, capacity = 0;
    ssize_t length;
    while ((length = getline(&line, &capacity, input)) >= 0) {
        if (length == 1 && line[0] == '\n') continue;
        char **next = realloc(lines, (count + 1) * sizeof(char *));
        if (!next) abort();
        lines = next; lines[count++] = strndup(line, (size_t)length);
        if (!lines[count - 1]) abort();
    }
    int failed_read = ferror(input); fclose(input); free(line);
    if (failed_read || !count) return 2;
    struct sigaction action = {0}; action.sa_handler = stop_signal;
    sigemptyset(&action.sa_mask);
    sigaction(SIGINT, &action, NULL); sigaction(SIGTERM, &action, NULL);
    uint64_t launch = nanos();
    /* Follow the stock generated entrypoint order, explicitly choosing zero
     * before ANY imports. Optional full preparation uses explicit teardown
     * before the unchanged runtime guard; module initializers are not rerun. */
    lean_initialize();
    lean_set_panic_messages(false);
    lean_object *init = initialize_Lean49PreparedBranches(1, lean_io_mk_world());
    lean_set_panic_messages(true);
    if (!take_value(init)) return 1;
    lean_io_mark_end_initialization();
    lean_init_task_manager_using(0);
    lean_object *roots = take_value(gpu_smt_lean49_start(lean_mk_string(argv[2]), lean_io_mk_world()));
    if (!roots) return 1;
    printf("{\"event\":\"initialized\",\"parent_pid\":%d,\"parent_workers\":0,\"child_workers\":\"native_default\",\"inputs\":%zu,\"elapsed_ns\":%llu}\n",
           getpid(), count, (unsigned long long)(nanos() - launch)); fflush(stdout);
    size_t completed = 0;
    for (size_t index = 0; index < count && !stopped; ++index) {
        uint64_t admitted = nanos();
        printf("{\"event\":\"admitted\",\"source_index\":%zu,\"monotonic_ns\":%llu}\n",
               index, (unsigned long long)admitted); fflush(stdout);
        /* Charge process startup to the first admission's300s budget. */
        uint64_t deadline = (index ? admitted : launch) + UINT64_C(300000000000);
        lean_inc(roots);
        lean_object *next = take_value(prepare_native(roots, lines[index]));
        if (!next) return 1;
        lean_dec(roots); roots = next;
            if (getenv("GPU_SMT_PARENT_PREPARATION") && !strcmp(getenv("GPU_SMT_PARENT_PREPARATION"), "header-cache")) lean_mark_persistent(roots);
        unsigned live = tids(), descriptors = foreign_fds();
        if (live != 1 || descriptors || nanos() >= deadline || stopped) {
            printf("{\"event\":\"refused\",\"source_index\":%zu,\"live_tids\":%u,\"foreign_fds\":%u,\"elapsed_ns\":%llu}\n",
                   index, live, descriptors, (unsigned long long)(nanos() - admitted)); fflush(stdout);
            return stopped ? 128 + stopped : 1;
        }
        int pipefd[2];
        if (pipe2(pipefd, O_CLOEXEC)) { perror("pipe"); return 1; }
        pid_t owner = getpid(), child = fork();
        if (child == 0) {
                in_candidate_child = 1;
            /* No parent control/stdout FD survives as the child's output. */
            if (setpgid(0, 0) || prctl(PR_SET_PDEATHSIG, SIGKILL) || getppid() != owner) _exit(125);
            close(pipefd[0]);
            if (dup2(pipefd[1], STDOUT_FILENO) < 0) _exit(125);
            close(pipefd[1]);
            signal(SIGINT, SIG_DFL); signal(SIGTERM, SIG_DFL);
            lean_init_task_manager();
            lean_inc(roots);
            lean_object *result = gpu_smt_lean49_execute(roots, lean_mk_string(lines[index]), lean_io_mk_world());
            int code = 1;
            if (lean_io_result_is_ok(result)) {
                const char *text = lean_string_cstr(lean_io_result_get_value(result));
                code = write_all(STDOUT_FILENO, text, strlen(text)) || write_all(STDOUT_FILENO, "\n", 1) ? 1 : 0;
            } else lean_io_result_show_error(result);
            lean_dec(result);
            lean_finalize_task_manager();
            fflush(NULL); _exit(code);
        }
        close(pipefd[1]);
        if (child < 0) { perror("fork"); close(pipefd[0]); return 1; }
        /* Either parent or child establishes this exclusively owned group. */
        if (setpgid(child, child) && errno != EACCES && errno != ESRCH) {
            kill(child, SIGKILL); waitpid(child, NULL, 0); close(pipefd[0]); return 1;
        }
        printf("{\"event\":\"launched\",\"source_index\":%zu,\"child_pid\":%d,\"live_parent_tids\":%u,\"preparation_ns\":%llu}\n",
               index, child, live, (unsigned long long)(nanos() - admitted)); fflush(stdout);
        int pidfd = (int)syscall(SYS_pidfd_open, child, 0);
        int flags = fcntl(pipefd[0], F_GETFL);
        int nonblocking_error = flags < 0 ? 1 : fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK);
        int transport_error = pidfd < 0 || nonblocking_error;
        char *output = NULL; size_t bytes = 0; int timeout = 0, status = 0, exited = 0, pipe_done = 0;
        while (!transport_error && !stopped && !exited) {
            uint64_t now = nanos();
            if (now >= deadline) { timeout = 1; break; }
            uint64_t ms = (deadline - now + 999999) / 1000000;
            struct pollfd descriptors[2] = {{pipe_done ? -1 : pipefd[0], POLLIN, 0}, {pidfd, POLLIN, 0}};
            int ready = poll(descriptors, 2, ms > INT_MAX ? INT_MAX : (int)ms);
            if (ready < 0 && errno == EINTR) continue;
            if (ready < 0) { transport_error = 1; break; }
            char chunk[65536]; ssize_t n;
            while ((n = read(pipefd[0], chunk, sizeof(chunk))) > 0)
                if (append(&output, &bytes, chunk, (size_t)n)) { transport_error = 1; break; }
            if (n == 0) pipe_done = 1;
            if (n < 0 && errno != EAGAIN && errno != EINTR) transport_error = 1;
            exited = !!(descriptors[1].revents & POLLIN);
        }
        /* Reserve the child PID until group cleanup is complete; never kill a
         * potentially reused process-group ID after reaping the leader. */
        kill(-child, SIGKILL); kill(child, SIGKILL);
        while (waitpid(child, &status, 0) < 0) if (errno != EINTR) { transport_error = 1; break; }
        char chunk[65536]; ssize_t n;
        while ((n = read(pipefd[0], chunk, sizeof(chunk))) > 0)
            if (append(&output, &bytes, chunk, (size_t)n)) { transport_error = 1; break; }
        close(pipefd[0]); if (pidfd >= 0) close(pidfd);
        int code = WIFEXITED(status) ? WEXITSTATUS(status) : WIFSIGNALED(status) ? 128 + WTERMSIG(status) : -1;
        printf("{\"event\":\"candidate\",\"source_index\":%zu,\"child_pid\":%d,\"returncode\":%d,\"timeout\":%s,\"transport_error\":%s,\"interrupted\":%s,\"elapsed_ns\":%llu,\"stdout_hex\":\"",
               index, child, code, timeout ? "true" : "false", transport_error ? "true" : "false",
               stopped ? "true" : "false", (unsigned long long)(nanos() - admitted));
        print_hex(output, bytes); printf("\"}\n"); fflush(stdout); free(output);
        ++completed;
        if (transport_error) return 1;
    }
    printf("{\"event\":\"finish\",\"inputs\":%zu,\"result_records\":%zu,\"interrupted\":%s,\"elapsed_ns\":%llu}\n", count, completed, stopped ? "true" : "false", (unsigned long long)(nanos() - launch)); fflush(stdout);
    return stopped ? 128 + stopped : 0;
}

/* Concurrent mode retains the same import-only native boundary. Every live
 * pipe/pidfd is identified from the master-owned table; other FDs still refuse
 * a fork. Children close sibling channels before entering ordinary Lean. */
struct branch {
    int active, pipefd, pidfd, pipe_done, transport_error, pipe_nonblocking;
    pid_t pid;
    size_t index, bytes;
    uint64_t admitted, deadline;
    char *output;
    struct stat pipe_identity, pid_identity;
};

static int same_fd(int fd, const struct stat *identity) {
    struct stat actual;
    return fd >= 0 && !fstat(fd, &actual) && actual.st_dev == identity->st_dev &&
        actual.st_ino == identity->st_ino && actual.st_mode == identity->st_mode;
}

static int owned_pidfd(struct branch *b) {
    if (!same_fd(b->pidfd, &b->pid_identity)) return 0;
    char path[64], line[256];
    snprintf(path, sizeof(path), "/proc/self/fdinfo/%d", b->pidfd);
    FILE *info = fopen(path, "r"); if (!info) return 0;
    int matches = 0;
    while (fgets(line, sizeof(line), info)) if (!strncmp(line, "Pid:", 4)) {
        const char *s = line + 4; while (*s == ' ' || *s == '\t') ++s;
        unsigned long value = 0; int digits = 0, valid = 1;
        while (*s >= '0' && *s <= '9') {
            if (value > ((unsigned long)INT_MAX - (unsigned long)(*s - '0')) / 10) { valid = 0; break; }
            value = value * 10 + (unsigned long)(*s++ - '0'); ++digits;
        }
        matches = valid && digits && value == (unsigned long)b->pid;
        break;
    }
    fclose(info); return matches;
}

static unsigned pool_foreign_fds(struct branch *branches, size_t width) {
    /* Missing/replaced owned handles also refuse, even if /proc omits them. */
    for (size_t i = 0; i < width; ++i) if (branches[i].active &&
        (!same_fd(branches[i].pipefd, &branches[i].pipe_identity) || !owned_pidfd(&branches[i]))) return UINT_MAX;
    DIR *d = opendir("/proc/self/fd");
    if (!d) return UINT_MAX;
    int own = dirfd(d);
    unsigned count = 0;
    struct dirent *entry;
    while ((entry = readdir(d))) {
        if (entry->d_name[0] == '.') continue;
        long fd = 0; int valid = 1;
        for (const char *s = entry->d_name; *s; ++s) {
            if (*s < '0' || *s > '9' || fd > INT_MAX / 10) { valid = 0; break; }
            fd = fd * 10 + (*s - '0');
        }
        if (!valid) { ++count; continue; }
        if (fd <= 2 || fd == own) continue;
        int identified = 0;
        for (size_t i = 0; i < width; ++i) {
            struct branch *b = &branches[i];
            if (!b->active) continue;
            if ((fd == b->pipefd && same_fd(b->pipefd, &b->pipe_identity)) ||
                (fd == b->pidfd && same_fd(b->pidfd, &b->pid_identity))) {
                identified = 1; break;
            }
        }
        if (!identified) ++count;
    }
    closedir(d); return count;
}

static void pool_read(struct branch *b) {
    if (!b->pipe_nonblocking || !same_fd(b->pipefd, &b->pipe_identity)) {
        b->transport_error = 1; return;
    }
    char chunk[65536]; ssize_t n;
    while ((n = read(b->pipefd, chunk, sizeof(chunk))) > 0) {
        if (append(&b->output, &b->bytes, chunk, (size_t)n)) {
            b->transport_error = 1; return;
        }
    }
    if (n == 0) b->pipe_done = 1;
    if (n < 0 && errno != EAGAIN && errno != EINTR) b->transport_error = 1;
}

static void pool_finish(struct branch *b, int timeout, int aborted) {
    int status = 0, reaped = 0;
    /* Keep the leader reserved until every owned group has been disposed. */
    kill(-b->pid, SIGKILL); kill(b->pid, SIGKILL);
    for (;;) {
        if (waitpid(b->pid, &status, 0) == b->pid) { reaped = 1; break; }
        if (errno != EINTR) { b->transport_error = 1; break; }
    }
    pool_read(b);
    if (same_fd(b->pipefd, &b->pipe_identity)) close(b->pipefd);
    if (same_fd(b->pidfd, &b->pid_identity)) close(b->pidfd);
    int code = !reaped ? -1 : WIFEXITED(status) ? WEXITSTATUS(status) : WIFSIGNALED(status) ? 128 + WTERMSIG(status) : -1;
    printf("{\"event\":\"candidate\",\"source_index\":%zu,\"child_pid\":%d,\"returncode\":%d,\"timeout\":%s,\"transport_error\":%s,\"interrupted\":%s,\"elapsed_ns\":%llu,\"stdout_hex\":\"",
        b->index, b->pid, code, timeout ? "true" : "false",
        b->transport_error || aborted ? "true" : "false", stopped ? "true" : "false",
        (unsigned long long)(nanos() - b->admitted));
    print_hex(b->output, b->bytes); printf("\"}\n"); fflush(stdout);
    free(b->output); b->output = NULL; b->active = 0;
}

static int concurrent_main(int argc, char **argv, size_t requested_width) {

    if (argc != 3) {
        fprintf(stderr, "usage: Lean49PreparedBranches INPUT.jsonl SYSROOT\n");
        return 2;
    }
    /* Read and close the ordinary offline input before any branch. No FILE
     * buffer/descriptor is inherited as a second candidate input reader. */
    FILE *input = fopen(argv[1], "r");
    if (!input) { perror("input"); return 2; }
    char **lines = NULL, *line = NULL; size_t count = 0, capacity = 0;
    ssize_t length;
    while ((length = getline(&line, &capacity, input)) >= 0) {
        if (length == 1 && line[0] == '\n') continue;
        char **next = realloc(lines, (count + 1) * sizeof(char *));
        if (!next) abort();
        lines = next; lines[count++] = strndup(line, (size_t)length);
        if (!lines[count - 1]) abort();
    }
    int failed_read = ferror(input); fclose(input); free(line);
    if (failed_read || !count) return 2;
    struct sigaction action = {0}; action.sa_handler = stop_signal;
    sigemptyset(&action.sa_mask);
    sigaction(SIGINT, &action, NULL); sigaction(SIGTERM, &action, NULL);
    uint64_t launch = nanos();
    /* Follow the stock generated entrypoint order, explicitly choosing zero
     * before ANY imports. Optional full preparation uses explicit teardown
     * before the unchanged runtime guard; module initializers are not rerun. */
    lean_initialize();
    lean_set_panic_messages(false);
    lean_object *init = initialize_Lean49PreparedBranches(1, lean_io_mk_world());
    lean_set_panic_messages(true);
    if (!take_value(init)) return 1;
    lean_io_mark_end_initialization();
    lean_init_task_manager_using(0);
    lean_object *roots = take_value(gpu_smt_lean49_start(lean_mk_string(argv[2]), lean_io_mk_world()));
    if (!roots) return 1;
    printf("{\"event\":\"initialized\",\"parent_pid\":%d,\"parent_workers\":0,\"child_workers\":\"native_default\",\"inputs\":%zu,\"elapsed_ns\":%llu}\n",
           getpid(), count, (unsigned long long)(nanos() - launch)); fflush(stdout);

    size_t width = requested_width < count ? requested_width : count;
    struct branch *branches = calloc(width, sizeof(*branches));
    struct pollfd *polling = calloc(width * 2, sizeof(*polling));
    if (!branches || !polling) { perror("branch table"); return 1; }
    printf("{\"event\":\"concurrency\",\"requested_jobs\":%zu,\"active_capacity\":%zu}\n", requested_width, width); fflush(stdout);
    size_t next_index = 0, live_children = 0, completed = 0;
    int fatal = 0;
    while ((next_index < count || live_children) && !stopped && !fatal) {
        while (next_index < count && live_children < width && !stopped && !fatal) {
            size_t slot = 0;
            while (slot < width && branches[slot].active) ++slot;
            struct branch *b = &branches[slot];
            size_t index = next_index;
            uint64_t admitted = nanos();
            printf("{\"event\":\"admitted\",\"source_index\":%zu,\"monotonic_ns\":%llu}\n", index, (unsigned long long)admitted); fflush(stdout);
            uint64_t deadline = (index ? admitted : launch) + UINT64_C(300000000000);
            lean_inc(roots);
            lean_object *prepared = take_value(prepare_native(roots, lines[index]));
            if (!prepared) { fatal = 1; break; }
            lean_dec(roots); roots = prepared;
            if (getenv("GPU_SMT_PARENT_PREPARATION") && !strcmp(getenv("GPU_SMT_PARENT_PREPARATION"), "header-cache")) lean_mark_persistent(roots);
            unsigned live = tids(), descriptors = pool_foreign_fds(branches, width);
            if (live != 1 || descriptors || nanos() >= deadline || stopped) {
                printf("{\"event\":\"refused\",\"source_index\":%zu,\"live_tids\":%u,\"foreign_fds\":%u,\"elapsed_ns\":%llu}\n", index, live, descriptors, (unsigned long long)(nanos() - admitted)); fflush(stdout);
                fatal = 1; break;
            }
            int pipefd[2];
            if (pipe2(pipefd, O_CLOEXEC)) { perror("pipe"); fatal = 1; break; }
            pid_t owner = getpid(), child = fork();
            if (child == 0) {
                in_candidate_child = 1;
                if (setpgid(0, 0) || prctl(PR_SET_PDEATHSIG, SIGKILL) || getppid() != owner) _exit(125);
                close(pipefd[0]);
                /* These are exactly the positively identified inherited own
                 * channels, never sibling stdin/output or unrelated services. */
                for (size_t i = 0; i < width; ++i) if (branches[i].active) {
                    close(branches[i].pipefd); close(branches[i].pidfd);
                }
                if (dup2(pipefd[1], STDOUT_FILENO) < 0) _exit(125);
                close(pipefd[1]); signal(SIGINT, SIG_DFL); signal(SIGTERM, SIG_DFL);
                lean_init_task_manager(); lean_inc(roots);
                lean_object *result = gpu_smt_lean49_execute(roots, lean_mk_string(lines[index]), lean_io_mk_world());
                int code = 1;
                if (lean_io_result_is_ok(result)) {
                    const char *text = lean_string_cstr(lean_io_result_get_value(result));
                    code = write_all(STDOUT_FILENO, text, strlen(text)) || write_all(STDOUT_FILENO, "\n", 1) ? 1 : 0;
                } else lean_io_result_show_error(result);
                lean_dec(result); lean_finalize_task_manager(); fflush(NULL); _exit(code);
            }
            close(pipefd[1]);
            if (child < 0) { perror("fork"); close(pipefd[0]); fatal = 1; break; }
            memset(b, 0, sizeof(*b));
            b->active = 1; b->pid = child; b->pipefd = pipefd[0];
            b->index = index; b->admitted = admitted; b->deadline = deadline;
            b->pidfd = (int)syscall(SYS_pidfd_open, child, 0);
            ++live_children; ++next_index;
            int flags = fcntl(b->pipefd, F_GETFL);
            b->pipe_nonblocking = flags >= 0 && !fcntl(b->pipefd, F_SETFL, flags | O_NONBLOCK);
            int pipe_identified = !fstat(b->pipefd, &b->pipe_identity);
            int pid_identified = b->pidfd >= 0 && !fstat(b->pidfd, &b->pid_identity);
            if ((setpgid(child, child) && errno != EACCES && errno != ESRCH) ||
                !b->pipe_nonblocking || !pipe_identified || !pid_identified) {
                b->transport_error = 1; fatal = 1;
            }
            printf("{\"event\":\"launched\",\"source_index\":%zu,\"child_pid\":%d,\"live_parent_tids\":%u,\"preparation_ns\":%llu,\"live_children\":%zu}\n",
                index, child, live, (unsigned long long)(nanos() - admitted), live_children); fflush(stdout);
        }
        if (stopped || fatal) break;
        uint64_t now = nanos(), earliest = UINT64_MAX;
        for (size_t i = 0; i < width; ++i) {
            struct branch *b = &branches[i];
            polling[i * 2] = (struct pollfd){b->active && !b->pipe_done ? b->pipefd : -1, POLLIN, 0};
            polling[i * 2 + 1] = (struct pollfd){b->active ? b->pidfd : -1, POLLIN, 0};
            if (b->active && b->deadline < earliest) earliest = b->deadline;
        }
        if (!live_children) continue;
        uint64_t milliseconds = earliest > now ? (earliest - now + 999999) / 1000000 : 0;
        int ready = poll(polling, width * 2, milliseconds > INT_MAX ? INT_MAX : (int)milliseconds);
        if (ready < 0 && errno == EINTR) continue;
        if (ready < 0) { fatal = 1; break; }
        now = nanos();
        for (size_t i = 0; i < width; ++i) {
            struct branch *b = &branches[i]; if (!b->active) continue;
            if (polling[i * 2].revents & (POLLIN | POLLHUP | POLLERR)) pool_read(b);
            if ((polling[i * 2].revents | polling[i * 2 + 1].revents) & POLLNVAL) b->transport_error = 1;
            int timeout = now >= b->deadline;
            int exited = polling[i * 2 + 1].revents & (POLLIN | POLLHUP | POLLERR);
            if (timeout || exited || b->transport_error) {
                int error = b->transport_error;
                pool_finish(b, timeout, 0); ++completed; --live_children;
                if (error || b->transport_error) fatal = 1;
            }
        }
    }
    for (size_t i = 0; i < width; ++i) if (branches[i].active) {
        pool_finish(&branches[i], 0, fatal); ++completed;
    }
    printf("{\"event\":\"finish\",\"inputs\":%zu,\"result_records\":%zu,\"interrupted\":%s,\"transport_failure\":%s,\"elapsed_ns\":%llu}\n",
        count, completed, stopped ? "true" : "false", fatal ? "true" : "false", (unsigned long long)(nanos() - launch)); fflush(stdout);
    free(branches); free(polling);
    return stopped ? 128 + stopped : fatal ? 1 : 0;
}

static int snapshot_stream_main(int argc, char **argv) {
    lean_initialize();
    lean_set_panic_messages(false);
    lean_object *init = initialize_Lean49PreparedBranches(1, lean_io_mk_world());
    lean_set_panic_messages(true);
    if (!take_value(init)) return 1;
    lean_io_mark_end_initialization();
    lean_init_task_manager_using(0);
    snapshot_mode = 1;
    lean_object *args = lean_box(0);
    for (int i = argc - 1; i >= 1; --i) {
        lean_object *next = lean_alloc_ctor(1, 2, 0);
        lean_ctor_set(next, 0, lean_mk_string(argv[i]));
        lean_ctor_set(next, 1, args); args = next;
    }
    lean_object *result = take_value(gpu_smt_lean49_stream(args, lean_io_mk_world()));
    if (!result) return 1;
    unsigned status = lean_unbox(result);
    lean_dec(result);
    if (snapshot_runtime_active) lean_finalize_task_manager();
    return (int)status;
}

#include "lean49_prepared_worker_pool.c.inc"

int main(int argc, char **argv) {
    if (argc == 5 && !strcmp(argv[1], "warm-pool")) return warm_pool_main(argc, argv);
    if (argc == 5 && (!strcmp(argv[1], "full") || !strcmp(argv[1], "imports"))) return snapshot_stream_main(argc, argv);
    if (argc == 3) return serial_main(argc, argv);
    if (argc != 4 || !argv[3][0]) {
        fprintf(stderr, "usage: Lean49PreparedBranches INPUT.jsonl SYSROOT [JOBS]\n"); return 2;
    }
    size_t width = 0;
    for (const char *s = argv[3]; *s; ++s) {
        if (*s < '0' || *s > '9' || width > (SIZE_MAX - (size_t)(*s - '0')) / 10) return 2;
        width = width * 10 + (size_t)(*s - '0');
    }
    if (!width) return 2;
    if (width == 1) return serial_main(3, argv);
    return concurrent_main(3, argv, width);
}
