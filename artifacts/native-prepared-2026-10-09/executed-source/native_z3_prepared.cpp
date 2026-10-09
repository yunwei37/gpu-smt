// Thin pinned Z3 shell SMT2 frontend adapter. No API manager or reconstruction.
#include <iostream>
#include <fstream>
#include <filesystem>
#include <chrono>
#include <stdexcept>
#include <cerrno>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <csignal>
#include <cstring>
#include "util/memory_manager.h"
#include "util/env_params.h"
#include "util/timeout.h"
#include "util/error_codes.h"
#include "util/z3_exception.h"
#include "util/mutex.h"
#include "parsers/smt2/smt2parser.h"
#include "muz/fp/dl_cmds.h"
#include "cmd_context/extra_cmds/dbg_cmds.h"
#include "cmd_context/extra_cmds/proof_cmds.h"
#include "opt/opt_cmds.h"
#include "cmd_context/extra_cmds/polynomial_cmds.h"
#include "cmd_context/extra_cmds/subpaving_cmds.h"
#include "smt/smt2_extra_cmds.h"
#include "smt/smt_solver.h"

// Restricted to the retained preparation prefixes: no verification, timeout,
// parallel tactic, external callback, or input-directed stream replacement.
// Observing one task is a refusal guard, not a universal fork-safety proof.
namespace fs = std::filesystem;
static volatile sig_atomic_t owned_child = 0;
static void on_timeout() { _Exit(0); }
static void STD_CALL interrupted(int sig) {
    if (owned_child > 0) {
        kill(-owned_child, SIGKILL);
        while (waitpid(owned_child, nullptr, 0) < 0 && errno == EINTR) {}
    }
    signal(sig, SIG_DFL); raise(sig);
}
static unsigned threads() {
    unsigned n = 0;
    for (auto const& entry : fs::directory_iterator("/proc/self/task")) { (void)entry; ++n; }
    return n;
}
static double elapsed(std::chrono::steady_clock::time_point t) {
    return std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();
}
static void snapshot(fs::path path, pid_t pid = 0) {
    std::ifstream in(pid ? "/proc/"+std::to_string(pid)+"/smaps_rollup" : "/proc/self/smaps_rollup");
    std::ofstream out(path); out << in.rdbuf();
}
static void redirect(fs::path path, int target) {
    int fd = open(path.c_str(), O_WRONLY|O_CREAT|O_TRUNC, 0600);
    if (fd < 0 || dup2(fd,target)<0) throw std::runtime_error("output redirect failed: "+path.string());
    close(fd);
}
static unsigned parse(cmd_context& ctx, char const* path) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error(std::string("Cannot read ")+path);
    // Exact native file path: no tokenization, transformation or inserted commands.
    // Match stock -in -smt2 and the qualified lazy frontend's parser flag.
    return parse_smt2_commands(ctx, in, true) ? 0 : 1;
}
static void flush() { std::cout.flush(); std::cerr.flush(); }
static void record(std::ofstream& cost, std::string const& name, double wall, int status,
                   rusage const& r, int task_count, bool marker=false, int kill_result=-2) {
    cost << name << '\t' << wall << '\t' << status << '\t'
         << (WIFEXITED(status)?WEXITSTATUS(status):-1) << '\t'
         << (WIFSIGNALED(status)?WTERMSIG(status):0) << '\t'
         << r.ru_utime.tv_sec+r.ru_utime.tv_usec/1e6 << '\t'
         << r.ru_stime.tv_sec+r.ru_stime.tv_usec/1e6 << '\t' << r.ru_maxrss
         << '\t' << task_count << '\t' << marker << '\t' << kill_result << '\n'; cost.flush();
}
static unsigned run(int argc, char** argv) {
    std::string mode = argv[1];
    bool fresh=mode=="fresh", split=mode=="split", cancel=mode=="branch-cancel";
    if ((!fresh&&!split&&!cancel&&mode!="branch"&&mode!="branch-reverse") ||
        (fresh&&argc!=4)||(split&&argc!=5)||(!fresh&&!split&&argc<(cancel?6:5)))
        throw std::runtime_error("fresh FULL OUTDIR | split PREFIX SUFFIX OUTDIR | branch[-reverse] PREFIX OUTDIR SUFFIX... | branch-cancel PREFIX OUTDIR CANCEL_SUFFIX SUFFIX...");
    fs::path out=argv[split?4:3]; fs::create_directories(out);
    std::ofstream cost(out/"cost.tsv");
    cost << "name\twall_seconds\twait_status\texit_code\tsignal\tuser_seconds\tsystem_seconds\tmaxrss_kib\tobserved_tasks\tdone_marker\tkill_return\n";
    int savedout=dup(1), savederr=dup(2);
    register_on_timeout_proc(on_timeout); signal(SIGINT,interrupted); signal(SIGTERM,interrupted);
    cmd_context ctx;
    ctx.set_solver_factory(mk_smt_strategic_solver_factory());
    install_dl_cmds(ctx); install_dbg_cmds(ctx); install_polynomial_cmds(ctx);
    install_subpaving_cmds(ctx); install_opt_cmds(ctx); install_smt2_extra_cmds(ctx); install_proof_cmds(ctx);
    ctx.set_regular_stream(std::cout); ctx.set_diagnostic_stream(std::cerr);
    redirect(out/(fresh||split?"0.stdout":"prefix.stdout"),1);
    redirect(out/(fresh||split?"0.stderr":"prefix.stderr"),2);
    auto start=std::chrono::steady_clock::now(); unsigned result=parse(ctx,argv[2]);
    if(split && !result) result=parse(ctx,argv[3]);
    flush(); snapshot(out/"parent.smaps"); rusage usage{}; getrusage(RUSAGE_SELF,&usage);
    unsigned task_count=threads(); record(cost,fresh?"fresh":split?"split":"prefix",elapsed(start),result<<8,usage,task_count);
    dup2(savedout,1); dup2(savederr,2); close(savedout); close(savederr);
    if(fresh||split||result) return result;
    if(task_count!=1) throw std::runtime_error("Refusing fork: prepared parent task count is not one");
    auto child=[&](char const* suffix,std::string name,bool cancellation) {
        if(threads()!=1) throw std::runtime_error("Refusing fork: current task count is not one");
        int pipefd[2]={-1,-1}; if(cancellation&&pipe(pipefd)) throw std::runtime_error("pipe failed");
        flush(); auto begin=std::chrono::steady_clock::now(); pid_t parent=getpid(), pid=fork();
        if(pid<0) throw std::runtime_error("fork failed");
        if(!pid) {
            owned_child=0; setpgid(0,0); prctl(PR_SET_PDEATHSIG,SIGKILL);
            if(getppid()!=parent) _exit(3);
            try {
                redirect(out/(name+".stderr"),2);
                if(cancellation) { close(pipefd[0]); if(dup2(pipefd[1],1)<0) _exit(3); close(pipefd[1]); }
                else redirect(out/(name+".stdout"),1);
                unsigned rc=parse(ctx,suffix); flush(); snapshot(out/(name+".smaps"));
                std::ofstream tasks(out/(name+".tasks")); tasks << threads() << '\n'; tasks.close();
                _exit(rc);
            } catch(z3_exception const& ex) { std::cerr << "ERROR: " << ex.what() << std::endl; _exit(ex.has_error_code()?ex.error_code():ERR_INTERNAL_FATAL); }
            catch(std::exception const& ex) { std::cerr << ex.what() << std::endl; _exit(3); }
        }
        owned_child=pid; setpgid(pid,pid); bool marker=false; int kill_result=-2;
        if(cancellation) {
            close(pipefd[1]); std::ofstream partial(out/(name+".stdout")); std::string line; char buf[4096]; bool decision_seen=false;
            while(true) {
                ssize_t n=read(pipefd[0],buf,sizeof(buf));
                if(n<0&&errno==EINTR) continue;
                if(n<0) { kill(-pid,SIGKILL); break; }
                if(!n) break;
                partial.write(buf,n); partial.flush();
                for(ssize_t i=0;i<n;++i) {
                    if(buf[i]=='\n') {
                        if(line=="sat"||line=="unsat"||line=="unknown") decision_seen=true;
                        if(decision_seen&&!marker&&(line=="<<DONE>>"||line=="\"<<DONE>>\"")) {
                            marker=true;
                            std::ofstream live(out/(name+".proc-at-marker"));
                            for (auto const* leaf : {"status", "stat"}) {
                                std::ifstream proc("/proc/"+std::to_string(pid)+"/"+leaf);
                                live << leaf << '\n' << proc.rdbuf() << '\n';
                            }
                            live.close(); snapshot(out/(name+".smaps-at-marker"),pid);
                            kill_result=kill(pid,SIGKILL);
                        }
                        line.clear();
                    } else line+=buf[i];
                }
            }
            close(pipefd[0]);
        }
        int status=0; rusage r{}; pid_t reaped;
        do { reaped=wait4(pid,&status,0,&r); } while(reaped<0&&errno==EINTR);
        owned_child=0;
        if(reaped!=pid) throw std::runtime_error("wait4 failed");
        record(cost,name,elapsed(begin),status,r,-1,marker,kill_result);
    };
    if(cancel) child(argv[4],"cancel",true);
    // The root supplies forward/reverse argument order; names index that order.
    for(int i=cancel?5:4;i<argc;++i) child(argv[i],std::to_string(i-(cancel?5:4)),false);
    return 0;
}
int STD_CALL main(int argc,char** argv) {
    if(argc<4) { std::cerr << "Insufficient arguments\n"; return 2; }
    try {
        memory::initialize(0); memory::exit_when_out_of_memory(true,"ERROR: out of memory");
        env_params::updt_params(); memory::exit_when_out_of_memory(true,"(error \"out of memory\")");
        unsigned result=run(argc,argv); disable_timeout(); memory::finalize(); return result;
    } catch(z3_exception& ex) {
        std::cerr << "ERROR: " << ex.what() << '\n'; return ex.has_error_code()?ex.error_code():ERR_INTERNAL_FATAL;
    } catch(std::exception const& ex) { std::cerr << ex.what() << '\n'; return 3; }
}
