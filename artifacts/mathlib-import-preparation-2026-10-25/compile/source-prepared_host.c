/* Native single-threaded import parent; Rust owns scheduling/admission.
 * This host is a context-specific backend, not a generic threaded-fork claim.
 * No candidate command executes in the parent. Each connection owns one child.
 */
#define _GNU_SOURCE
#include <lean/lean.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <poll.h>
#include <sched.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <unistd.h>

extern void lean_initialize(void);
extern lean_object *initialize_GpuSmtPrepared(uint8_t, lean_object *);
extern lean_object *gpu_smt_prepared_create(lean_object *, lean_object *, lean_object *);
extern lean_object *gpu_smt_prepared_stats(lean_object *);
extern lean_object *gpu_smt_prepared_check(lean_object *, lean_object *, lean_object *);

struct branch { pid_t pid; int channel; struct branch *next; };
/* Modern Lean starts libuv service threads in runtime initialization.
   For audited synchronous import contexts, construct those services only in
   disposable children. No live libuv thread or event descriptor is forked. */
#ifdef GPU_SMT_DEFER_LIBUV
static int deferred_libuv;
extern void __real_initialize_libuv(void);
void __wrap_initialize_libuv(void) { deferred_libuv=1; }
#endif
static volatile sig_atomic_t stopping;
static void stop(int sig) { stopping = sig; }
static void changed(int sig) { (void)sig; }
static int send_all(int fd, const char *text) {
    size_t left = strlen(text);
    while (left) {
        ssize_t n = send(fd, text, left, MSG_NOSIGNAL);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) return -1;
        text += n; left -= (size_t)n;
    }
    return 0;
}
static lean_object *value(lean_object *result) {
    if (!lean_io_result_is_ok(result)) {
        lean_io_result_show_error(result); lean_dec(result); return NULL;
    }
    lean_object *v = lean_io_result_get_value(result);
    lean_inc(v); lean_dec(result); return v;
}
static unsigned threads(void) {
    DIR *d=opendir("/proc/self/task"); if (!d) return 0;
    unsigned n=0; struct dirent *e;
    while ((e=readdir(d))) if (e->d_name[0]!='.') ++n;
    closedir(d); return n;
}
static int foreign_fds(void) {
    DIR *d=opendir("/proc/self/fd"); if (!d) return 1;
    int own=dirfd(d),foreign=0; struct dirent *e;
    while ((e=readdir(d))) {
        if (e->d_name[0]=='.') continue;
        int fd=atoi(e->d_name);
        if (fd>2 && fd!=own) ++foreign;
    }
    closedir(d); return foreign;
}
static void describe_foreign_fds(void) {
    DIR *d=opendir("/proc/self/fd"); if (!d) return;
    int own=dirfd(d); struct dirent *e;
    while ((e=readdir(d))) {
        if (e->d_name[0]=='.') continue;
        int fd=atoi(e->d_name); if (fd<=2 || fd==own) continue;
        char path[64],target[1024]; struct stat st={0};
        snprintf(path,sizeof(path),"/proc/self/fd/%d",fd);
        ssize_t n=readlink(path,target,sizeof(target)-1);
        if (n<0) strcpy(target,"unavailable"); else target[n]=0;
        fstat(fd,&st);
        fprintf(stderr,"prepared fd=%d mode=%o flags=%d target=%s\n",fd,
            (unsigned)st.st_mode,fcntl(fd,F_GETFL),target);
    }
    closedir(d);
}
/* This executable accepts only stdin/stdout/stderr as inherited channels.
   Close unexpected launcher descriptors before initializing any Lean resources;
   never sweep descriptors created later by Lean or imported native code. */
static unsigned close_inherited_fds(void) {
    DIR *d=opendir("/proc/self/fd"); if (!d) return 0;
    int own=dirfd(d); unsigned closed=0; struct dirent *e;
    while ((e=readdir(d))) {
        if (e->d_name[0]=='.') continue;
        int fd=atoi(e->d_name);
        if (fd>2 && fd!=own && close(fd)==0) ++closed;
    }
    closedir(d); return closed;
}
static int bind_worker(char *text) {
    cpu_set_t mask; CPU_ZERO(&mask); size_t count=0;
    char *next=NULL, *token=strtok_r(text,",\n",&next);
    while (token) {
        char *end=NULL; errno=0; unsigned long cpu=strtoul(token,&end,10);
        if (errno || end==token || *end || cpu>=CPU_SETSIZE) return -1;
        CPU_SET(cpu,&mask); ++count; token=strtok_r(NULL,",\n",&next);
    }
    return count ? sched_setaffinity(0,sizeof(mask),&mask) : -1;
}
static unsigned long long birth_ticks(void) {
    FILE *f=fopen("/proc/self/stat","r"); if (!f) return 0;
    char *raw=NULL; size_t cap=0; ssize_t n=getline(&raw,&cap,f); fclose(f);
    if (n<0) { free(raw); return 0; }
    char *end=strrchr(raw,')'),*save=NULL,*field=end?strtok_r(end+1," ",&save):NULL;
    for (unsigned i=0;i<19 && field;++i) field=strtok_r(NULL," ",&save);
    unsigned long long ticks=field?strtoull(field,NULL,10):0;
    free(raw); return ticks;
}
static void child(int fd, int listener, struct branch *siblings, lean_object *root, pid_t owner) {
    if (setpgid(0,0) || prctl(PR_SET_PDEATHSIG,SIGKILL) || getppid()!=owner) _exit(125);
    close(listener);
    for (struct branch *b=siblings;b;b=b->next) close(b->channel);
    signal(SIGINT,SIG_DFL); signal(SIGTERM,SIG_DFL); signal(SIGCHLD,SIG_DFL);
    char started[160]; snprintf(started,sizeof(started),"{\"started\":%ld,\"start_ticks\":%llu}\n",(long)getpid(),birth_ticks());
    if (send_all(fd,started)) _exit(126);
    /* Dedicated request stream; stdout/stderr remain diagnostic channels.
       Parent stdio/control input is never consumed by a candidate. */
    FILE *input=fdopen(dup(fd),"r"); if (!input) _exit(126);
    char *line=NULL; size_t capacity=0;
    if (getline(&line,&capacity,input)<0 || bind_worker(line)) _exit(126);
    if (getline(&line,&capacity,input)<0) _exit(126);
    close(STDIN_FILENO);
#ifdef GPU_SMT_DEFER_LIBUV
    if (deferred_libuv) __real_initialize_libuv();
#endif
    lean_init_task_manager();
    lean_inc(root);
    lean_object *response=value(gpu_smt_prepared_check(root,lean_mk_string(line),lean_io_mk_world()));
    int code=1;
    if (response) {
        code=send_all(fd,lean_string_cstr(response)) || send_all(fd,"\n") ? 1 : 0;
        lean_dec(response);
    } else send_all(fd,"{\"backend_error\":\"native child exception\"}\n");
    lean_finalize_task_manager();
    fclose(input); free(line); close(fd);
    fflush(NULL); _exit(code);
}
static void reap(struct branch **active) {
    struct branch **at=active;
    while (*at) {
        struct branch *b=*at; int status=0;
        /* WNOWAIT keeps the child PID reserved until its entire group is killed. */
        siginfo_t info; memset(&info,0,sizeof(info));
        int ready=waitid(P_PID,(id_t)b->pid,&info,WEXITED|WNOHANG|WNOWAIT);
        if (!ready && info.si_pid==b->pid) {
            kill(-b->pid,SIGKILL);
            struct rusage usage={0};
            while (wait4(b->pid,&status,0,&usage)<0 && errno==EINTR) {}
            char text[96]; int code=WIFEXITED(status)?WEXITSTATUS(status):128+WTERMSIG(status);
            snprintf(text,sizeof(text),"{\"retired\":%d,\"peak_rss_bytes\":%llu}\n",code,(unsigned long long)usage.ru_maxrss*1024);
            send_all(b->channel,text); close(b->channel);
            *at=b->next; free(b);
        } else at=&b->next;
    }
}
int main(int argc,char **argv) {
    if (argc!=3) { fprintf(stderr,"usage: prepared-host SOCKET SYSROOT\n"); return 2; }
    unsigned closed_inherited=close_inherited_fds();
    struct sigaction action={0}; sigemptyset(&action.sa_mask);
    action.sa_handler=stop; sigaction(SIGTERM,&action,NULL); sigaction(SIGINT,&action,NULL);
    action.sa_handler=changed; sigaction(SIGCHLD,&action,NULL);
    signal(SIGPIPE,SIG_IGN);
    pid_t owner=getppid();
    if (prctl(PR_SET_PDEATHSIG,SIGTERM) || getppid()!=owner) return 125;
    char *encoded=NULL; size_t capacity=0;
    if (getline(&encoded,&capacity,stdin)<0) return 2;
    lean_initialize(); lean_set_panic_messages(false);
    if (!value(initialize_GpuSmtPrepared(1,lean_io_mk_world()))) return 1;
    lean_set_panic_messages(true); lean_io_mark_end_initialization();
    /* Stock environment construction can create native promises and requires
       the ordinary manager. Tear down/join its owned workers before any fork. */
    lean_init_task_manager();
    lean_object *root=value(gpu_smt_prepared_create(lean_mk_string(encoded),lean_mk_string(argv[2]),lean_io_mk_world()));
    free(encoded);
    if (root) lean_mark_persistent(root);
    lean_finalize_task_manager();
    if (!root) return 1;
    /* No work manager at the branch point; imports must leave one thread. */
    unsigned live_threads=threads(); int extra_fds=foreign_fds();
    if (live_threads!=1 || extra_fds) {
        fprintf(stderr,"prepared context residue: threads=%u extra_fds=%d\n",live_threads,extra_fds);
        describe_foreign_fds();
        return 1;
    }
    struct sockaddr_un address={0}; address.sun_family=AF_UNIX;
    if (strlen(argv[1])>=sizeof(address.sun_path)) return 2;
    strcpy(address.sun_path,argv[1]);
    int listener=socket(AF_UNIX,SOCK_STREAM|SOCK_CLOEXEC,0);
    if (listener<0 || bind(listener,(void *)&address,sizeof(address)) || listen(listener,SOMAXCONN)) { perror("prepared listener"); return 1; }
    int uv_deferred=0;
#ifdef GPU_SMT_DEFER_LIBUV
    uv_deferred=deferred_libuv;
#endif
    lean_inc(root);
    lean_object *prepared_stats=gpu_smt_prepared_stats(root);
    printf("{\"ready\":true,\"parent_pid\":%ld,\"parent_threads\":1,\"preparations\":1,\"closed_inherited_fds\":%u,\"libuv_deferred\":%s,\"prepared_context\":%s}\n",
        (long)getpid(),closed_inherited,uv_deferred?"true":"false",lean_string_cstr(prepared_stats)); fflush(stdout);
    lean_dec(prepared_stats);
    struct branch *active=NULL;
    while (!stopping) {
        reap(&active);
        struct pollfd fds[2]={{listener,POLLIN,0},{STDIN_FILENO,POLLIN|POLLHUP,0}};
        /* The finite poll interval closes the signal-arrival-before-poll race;
           it does not implement proof timeouts or limit candidate execution. */
        int n=poll(fds,2,100);
        if (n<0 && errno==EINTR) continue;
        if (n<0 || (fds[1].revents&(POLLIN|POLLHUP|POLLERR))) break;
        if (fds[0].revents&POLLIN) {
            int fd=accept4(listener,NULL,NULL,SOCK_CLOEXEC); if (fd<0) continue;
            if (threads()!=1) { send_all(fd,"{\"backend_error\":\"parent is not single threaded\"}\n"); close(fd); continue; }
            pid_t parent=getpid(),pid=fork();
            if (!pid) child(fd,listener,active,root,parent);
            if (pid<0) { close(fd); continue; }
            setpgid(pid,pid);
            struct branch *b=malloc(sizeof(*b));
            if (!b) { kill(-pid,SIGKILL); kill(pid,SIGKILL); waitpid(pid,NULL,0); close(fd); stopping=SIGTERM; break; }
            *b=(struct branch){pid,fd,active}; active=b;
        }
    }
    close(listener); unlink(argv[1]);
    for (struct branch *b=active;b;b=b->next) { kill(-b->pid,SIGKILL); kill(b->pid,SIGKILL); }
    while (active) {
        struct branch *b=active; active=b->next;
        while (waitpid(b->pid,NULL,0)<0 && errno==EINTR) {}
        close(b->channel); free(b);
    }
    return 0;
}
