/* Finite warm-pool acquisition: native snapshots stay worker-private. */
#include <sys/socket.h>
extern lean_object *gpu_smt_lean49_seeded_stream(lean_object *, lean_object *, lean_object *);

static int warm_spawn(struct branch *workers, size_t width, size_t slot,
                      lean_object *roots, const char *sysroot, size_t count) {
    if (tids() != 1 || pool_foreign_fds(workers, width)) return -1;
    int channel[2];
    if (socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, channel)) return -1;
    pid_t owner = getpid(), child = fork();
    if (!child) {
        in_candidate_child = 1;
        if (setpgid(0, 0) || prctl(PR_SET_PDEATHSIG, SIGKILL) || getppid() != owner) _exit(125);
        close(channel[0]);
        for (size_t i = 0; i < width; ++i) if (workers[i].active) {
            close(workers[i].pipefd); close(workers[i].pidfd);
        }
        if (dup2(channel[1], STDIN_FILENO) < 0 || dup2(channel[1], STDOUT_FILENO) < 0) _exit(125);
        close(channel[1]);
        signal(SIGINT, SIG_DFL); signal(SIGTERM, SIG_DFL); signal(SIGPIPE, SIG_DFL);
        snapshot_mode = 1;
        char retirement[32]; snprintf(retirement, sizeof(retirement), "%zu", count);
        const char *values[] = {"full", "-", sysroot, retirement};
        lean_object *args = lean_box(0);
        for (int i = 3; i >= 0; --i) {
            lean_object *next = lean_alloc_ctor(1, 2, 0);
            lean_ctor_set(next, 0, lean_mk_string(values[i]));
            lean_ctor_set(next, 1, args); args = next;
        }
        lean_inc(roots);
        lean_object *value = take_value(gpu_smt_lean49_seeded_stream(roots, args, lean_io_mk_world()));
        int code = value ? (int)lean_unbox(value) : 1;
        if (value) lean_dec(value);
        if (snapshot_runtime_active) lean_finalize_task_manager();
        fflush(NULL); _exit(code);
    }
    close(channel[1]);
    if (child < 0) { close(channel[0]); return -1; }
    struct branch *b = &workers[slot]; memset(b, 0, sizeof(*b));
    b->active = 1; b->pid = child; b->pipefd = channel[0];
    b->pidfd = (int)syscall(SYS_pidfd_open, child, 0);
    int flags = fcntl(b->pipefd, F_GETFL);
    b->pipe_nonblocking = flags >= 0 && !fcntl(b->pipefd, F_SETFL, flags | O_NONBLOCK);
    if (fstat(b->pipefd, &b->pipe_identity) || b->pidfd < 0 ||
        fstat(b->pidfd, &b->pid_identity) || !b->pipe_nonblocking ||
        (setpgid(child, child) && errno != EACCES && errno != ESRCH)) return -1;
    printf("{\"event\":\"worker_started\",\"slot\":%zu,\"child_pid\":%d}\n", slot, child); fflush(stdout);
    return 0;
}

static int warm_send(struct branch *b, const char *data, size_t size) {
    while (size && !stopped) {
        ssize_t n = send(b->pipefd, data, size, MSG_NOSIGNAL);
        if (n > 0) { data += n; size -= (size_t)n; continue; }
        if (n < 0 && errno == EINTR) continue;
        if (n < 0 && errno == EAGAIN && nanos() < b->deadline) {
            uint64_t now = nanos();
            uint64_t ms = b->deadline > now ? (b->deadline - now + 999999) / 1000000 : 0;
            struct pollfd p = {b->pipefd, POLLOUT, 0};
            if (poll(&p, 1, ms > INT_MAX ? INT_MAX : (int)ms) >= 0) continue;
            if (errno == EINTR) continue;
        }
        return -1;
    }
    return size ? -1 : 0;
}

/* Reap only an owned worker. An emitted response is distinct from its exit. */
static int warm_reap(struct branch *b, int force) {
    if (force) { kill(-b->pid, SIGKILL); kill(b->pid, SIGKILL); }
    int status = 0;
    while (waitpid(b->pid, &status, 0) < 0) if (errno != EINTR) { status = -1; break; }
    if (same_fd(b->pipefd, &b->pipe_identity)) close(b->pipefd);
    if (same_fd(b->pidfd, &b->pid_identity)) close(b->pidfd);
    int code = status == -1 ? -1 : WIFEXITED(status) ? WEXITSTATUS(status) :
        WIFSIGNALED(status) ? 128 + WTERMSIG(status) : -1;
    printf("{\"event\":\"worker_exited\",\"child_pid\":%d,\"returncode\":%d}\n", b->pid, code);
    fflush(stdout); free(b->output); b->output = NULL; b->active = 0;
    return code;
}

static void warm_reply(struct branch *b, int ready, int code, int timeout) {
    printf("{\"event\":\"candidate\",\"source_index\":%zu,\"child_pid\":%d,\"response_ready\":%s,\"returncode\":",
        b->index, b->pid, ready ? "true" : "false");
    if (ready) printf("null"); else printf("%d", code);
    printf(",\"timeout\":%s,\"transport_error\":%s,\"interrupted\":%s,\"elapsed_ns\":%llu,\"stdout_hex\":\"",
        timeout ? "true" : "false", b->transport_error ? "true" : "false",
        stopped ? "true" : "false", (unsigned long long)(nanos() - b->admitted));
    print_hex(b->output, b->bytes); printf("\"}\n"); fflush(stdout);
    free(b->output); b->output = NULL; b->bytes = 0;
}

static int warm_pool_main(int argc, char **argv) {
    if (argc != 5) return 2;
    size_t requested = 0;
    if (!argv[4][0]) return 2;
    for (const char *s = argv[4]; *s; ++s) {
        if (*s < '0' || *s > '9' || requested > (SIZE_MAX - (size_t)(*s - '0')) / 10) return 2;
        requested = requested * 10 + (size_t)(*s - '0');
    }
    if (!requested) return 2;
    FILE *input = fopen(argv[2], "r"); if (!input) return 2;
    char **lines = NULL, *line = NULL; size_t capacity = 0, count = 0;
    ssize_t length;
    while ((length = getline(&line, &capacity, input)) >= 0) {
        if (length <= 1) continue;
        char **next = realloc(lines, (count + 1) * sizeof(*lines));
        if (!next) { fclose(input); free(line); return 1; }
        lines = next; lines[count++] = strdup(line);
        if (!lines[count - 1]) { fclose(input); free(line); return 1; }
    }
    int failed = ferror(input); fclose(input); free(line);
    if (failed || !count) return 2;
    size_t retirement = count;
    const char *configured = getenv("GPU_SMT_WORKER_RETIRE_AFTER");
    if (configured && configured[0]) {
        retirement = 0;
        for (const char *s = configured; *s; ++s) {
            if (*s < '0' || *s > '9' || retirement > (SIZE_MAX-(size_t)(*s-'0'))/10) return 2;
            retirement = retirement*10+(size_t)(*s-'0');
        }
        if (!retirement) return 2;
    }
    int first_header_only = getenv("GPU_SMT_PARENT_SEED_FIRST_HEADER") &&
        !strcmp(getenv("GPU_SMT_PARENT_SEED_FIRST_HEADER"), "1");
    struct sigaction action = {0}; action.sa_handler = stop_signal;
    sigemptyset(&action.sa_mask);
    sigaction(SIGINT, &action, NULL); sigaction(SIGTERM, &action, NULL);
    signal(SIGPIPE, SIG_IGN);
    uint64_t launch = nanos();
    lean_initialize(); lean_set_panic_messages(false);
    if (!take_value(initialize_Lean49PreparedBranches(1, lean_io_mk_world()))) return 1;
    lean_set_panic_messages(true); lean_io_mark_end_initialization();
    lean_init_task_manager_using(0);
    lean_object *roots = take_value(gpu_smt_lean49_start(lean_mk_string(argv[3]), lean_io_mk_world()));
    if (!roots) return 1;
    /* prepareOne has an exact-header fast path; no candidate body is run. */
    setenv("GPU_SMT_PARENT_PREPARATION", "header-cache", 1);
    for (size_t i = 0; i < (first_header_only ? 1 : count); ++i) {
        lean_inc(roots);
        lean_object *next = take_value(prepare_native(roots, lines[i]));
        if (!next) return 1;
        lean_dec(roots); roots = next;
        if (stopped || nanos() - launch >= UINT64_C(300000000000)) return 1;
    }
    lean_mark_persistent(roots);
    printf("{\"event\":\"initialized\",\"parent_pid\":%d,\"parent_workers\":0,\"child_workers\":\"native_default\",\"inputs\":%zu,\"seed_roots\":%zu,\"elapsed_ns\":%llu}\n",
        getpid(), count, lean_array_size(roots), (unsigned long long)(nanos() - launch)); fflush(stdout);
    size_t width = requested < count ? requested : count;
    struct branch *workers = calloc(width, sizeof(*workers));
    int *busy = calloc(width, sizeof(*busy));
    size_t *uses = calloc(width, sizeof(*uses));
    struct pollfd *polling = calloc(width * 2, sizeof(*polling));
    if (!workers || !busy || !uses || !polling) return 1;
    printf("{\"event\":\"worker_policy\",\"retire_after\":%zu,\"first_header_only\":%s}\n",
        retirement, first_header_only ? "true" : "false"); fflush(stdout);
    size_t next = 0, completed = 0; int fatal = 0;
    while ((next < count || completed < next) && !fatal && !stopped) {
        for (size_t i = 0; i < width && next < count && !fatal && !stopped; ++i) {
            struct branch *b = &workers[i]; if (busy[i]) continue;
            /* An idle native worker can exit after its last response. */
            if (b->active) {
                struct pollfd p = {b->pidfd, POLLIN, 0};
                if (poll(&p, 1, 0) > 0) warm_reap(b, 1);
            }
            uint64_t admitted = nanos();
            printf("{\"event\":\"admitted\",\"source_index\":%zu,\"monotonic_ns\":%llu}\n", next, (unsigned long long)admitted); fflush(stdout);
            /* Match the native warm comparator: EOF and ordinary waited exit
             * at the next request's admission, charging replacement latency.
             * No extra deadline or same-input retry is introduced. */
            if (b->active && uses[i] >= retirement) {
                printf("{\"event\":\"worker_retirement\",\"child_pid\":%d,\"uses\":%zu}\n",b->pid,uses[i]); fflush(stdout);
                shutdown(b->pipefd, SHUT_WR);
                if (warm_reap(b, 0)) { fatal = 1; break; }
            }
            if (!b->active) {
                uses[i] = 0;
                if (warm_spawn(workers, width, i, roots, argv[3], retirement)) { fatal = 1; break; }
            }
            b->index = next++; b->admitted = admitted;
            b->deadline = (b->index ? admitted : launch) + UINT64_C(300000000000);
            busy[i] = 1;
            printf("{\"event\":\"launched\",\"source_index\":%zu,\"child_pid\":%d}\n", b->index, b->pid); fflush(stdout);
            if (warm_send(b, lines[b->index], strlen(lines[b->index]))) b->transport_error = 1;
        }
        uint64_t earliest = UINT64_MAX, now = nanos();
        for (size_t i = 0; i < width; ++i) {
            struct branch *b = &workers[i];
            polling[2*i] = (struct pollfd){busy[i] ? b->pipefd : -1, POLLIN, 0};
            polling[2*i+1] = (struct pollfd){busy[i] ? b->pidfd : -1, POLLIN, 0};
            if (busy[i] && b->deadline < earliest) earliest = b->deadline;
            if (busy[i] && b->transport_error) earliest = now;
        }
        if (earliest == UINT64_MAX) continue;
        uint64_t ms = earliest > now ? (earliest - now + 999999)/1000000 : 0;
        int ready = poll(polling, width*2, ms > INT_MAX ? INT_MAX : (int)ms);
        if (ready < 0 && errno == EINTR) continue;
        if (ready < 0) { fatal = 1; break; }
        for (size_t i = 0; i < width; ++i) if (busy[i]) {
            struct branch *b = &workers[i];
            if (polling[2*i].revents & (POLLIN|POLLHUP|POLLERR)) pool_read(b);
            if ((polling[2*i].revents|polling[2*i+1].revents)&POLLNVAL) b->transport_error = 1;
            char *newline = b->output ? memchr(b->output, '\n', b->bytes) : NULL;
            if (newline && newline != b->output + b->bytes - 1) b->transport_error = 1;
            int timeout = nanos() >= b->deadline;
            int exited = polling[2*i+1].revents & (POLLIN|POLLHUP|POLLERR);
            if (newline && !timeout && !b->transport_error) {
                warm_reply(b, 1, 0, 0); busy[i] = 0; ++completed; ++uses[i];
            } else if (timeout || exited || b->pipe_done || b->transport_error) {
                /* Preserve all native bytes before reaping; never retry this input. */
                kill(-b->pid, SIGKILL); kill(b->pid, SIGKILL);
                int status = 0;
                while (waitpid(b->pid, &status, 0) < 0) if (errno != EINTR) { status = -1; break; }
                pool_read(b);
                int code = status == -1 ? -1 : WIFEXITED(status) ? WEXITSTATUS(status) :
                    WIFSIGNALED(status) ? 128+WTERMSIG(status) : -1;
                warm_reply(b, 0, code, timeout); busy[i] = 0; ++completed;
                if (same_fd(b->pipefd, &b->pipe_identity)) close(b->pipefd);
                if (same_fd(b->pidfd, &b->pid_identity)) close(b->pidfd);
                printf("{\"event\":\"worker_exited\",\"child_pid\":%d,\"returncode\":%d}\n", b->pid, code); fflush(stdout);
                b->active = 0;
            }
        }
    }
    /* EOF first to all idle workers; ordinary runtime finalization is charged. */
    for (size_t i = 0; i < width; ++i) if (workers[i].active && !fatal && !stopped)
        shutdown(workers[i].pipefd, SHUT_WR);
    for (size_t i = 0; i < width; ++i) if (workers[i].active) {
        if (busy[i]) { workers[i].transport_error = 1; warm_reply(&workers[i], 0, -1, 0); ++completed; }
        int code = warm_reap(&workers[i], fatal || stopped || busy[i]);
        if (code && !stopped) fatal = 1;
    }
    printf("{\"event\":\"finish\",\"inputs\":%zu,\"result_records\":%zu,\"interrupted\":%s,\"transport_failure\":%s,\"elapsed_ns\":%llu}\n",
        count, completed, stopped ? "true":"false", fatal ? "true":"false",
        (unsigned long long)(nanos()-launch)); fflush(stdout);
    for (size_t i = 0; i < count; ++i) free(lines[i]);
    free(lines); free(workers); free(busy); free(uses); free(polling);
    return stopped ? 128+stopped : fatal ? 1 : 0;
}
