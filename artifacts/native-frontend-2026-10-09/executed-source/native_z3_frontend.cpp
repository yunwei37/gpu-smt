// Thin pinned Z3 shell SMT2 frontend adapter. No API manager or reconstruction.
#include <iostream>
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

// Stock -in -smt2 has no global statistics/model flag. Its interrupt handler
// restores the default disposition and re-raises; timeout exits with zero.
static void on_timeout() { _Exit(0); }
static void STD_CALL on_ctrl_c(int) {
    signal(SIGINT, SIG_DFL);
    raise(SIGINT);
}
static unsigned run(bool eager) {
    register_on_timeout_proc(on_timeout);
    signal(SIGINT, on_ctrl_c);
    cmd_context ctx;
    if (eager) (void)ctx.m(); // Sole condition difference, before factory/options.
    ctx.set_solver_factory(mk_smt_strategic_solver_factory());
    install_dl_cmds(ctx);
    install_dbg_cmds(ctx);
    install_polynomial_cmds(ctx);
    install_subpaving_cmds(ctx);
    install_opt_cmds(ctx);
    install_smt2_extra_cmds(ctx);
    install_proof_cmds(ctx);
    signal(SIGINT, on_ctrl_c);
    return parse_smt2_commands(ctx, std::cin, true) ? 0 : 1;
}
int STD_CALL main(int argc, char** argv) {
    if (argc != 2 || (strcmp(argv[1], "lazy") && strcmp(argv[1], "eager"))) {
        std::cerr << "usage: native-z3-frontend lazy|eager < original.smt2\n";
        return 2;
    }
    try {
        memory::initialize(0);
        memory::exit_when_out_of_memory(true, "ERROR: out of memory");
        env_params::updt_params();
        memory::exit_when_out_of_memory(true, "(error \"out of memory\")");
        unsigned result = run(!strcmp(argv[1], "eager"));
        disable_timeout();
        memory::finalize();
        return result;
    } catch (z3_exception& ex) {
        std::cerr << "ERROR: " << ex.what() << "\n";
        return ex.has_error_code() ? ex.error_code() : ERR_INTERNAL_FATAL;
    }
}
