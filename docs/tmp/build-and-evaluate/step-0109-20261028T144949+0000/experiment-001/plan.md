# E109 — native parent event waiting,not new proof execution

RQ2/RQ3resource maintenance,BUILD_AND_EVALUATE;root only,self-review.
Previous turn replayed6real simplifier traces and pushed368a5bd:progress.
The matched full resource cohort stays frozen13d4606;the next native42cohort
remains separately staged. No new local native group or timing matrix.

Actual prepared_host.c uses poll(...,100) to bound a SIGCHLD/stop signal
arriving between reap/loop-condition and blocking poll. A plain infinite poll
would lose this wake. Use the standard ppoll atomic signal-mask/wait interface
instead,removing periodic polling without selecting another interval.

Block SIGCHLD/SIGTERM/SIGINT while inspecting/reaping and processing events.
Atomically enable them in ppoll;pending signals interrupt that wait. After
audited native initialization reinstall this host's retirement/stop handlers.
Forked candidates reset handlers and restore the launcher's original mask
before runtime initialization;they must not inherit the blocked wait mask.
Existing EOF/control FD,waitid(WNOWAIT)/wait4,process group,PID/birth,CPU/RSS
and response/deadline/retirement paths remain. No logger,thread,daemon,setting
or new observer is introduced.

Validation:existing real pinned4.18native CI covers raw response equivalence,
two live children,timeout/cancellation,readiness/fallback/parent retirement.
Extend its existing native source cases with /proc/self/status SigBlk output,
comparing the actual candidate with raw fresh Lean;no timing assertion or
fabricated native response. Existing full Rust/clippy/fmt/docs and Python CI
remain required. No local compiler/native qualification beside the full run.
The ppoll manual is protocol evidence,not a native performance result.
This is removal of a concrete periodic-wake path,not established CPU fraction
or end-to-end gain. Current full13d4606data cannot measure this later change.
