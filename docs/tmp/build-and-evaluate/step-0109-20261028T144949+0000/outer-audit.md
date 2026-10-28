# Step0109 outer self-audit — parent wait and mask ownership

Executing root only,not independent review. The source-visible100msperiodic
poll is removed using standard atomic mask/wait behavior,not a smaller chosen
interval. Signals stay pending between child reap/check and waiting;SIGCHLD,
SIGTERM and SIGINT become deliverable inside ppoll. Stop with ready descriptors
is checked before accepting another connection. Setup failures cannot advertise
successful native readiness.

The forked child restores the original launcher mask after defaulting lifecycle
handlers and before service/task initialization. Its native SigBlk case must
read the real field and match raw fresh Lean without fallback. Existing native
concurrency,retirement,timeout and readiness controls remain. The mask change
belongs only to these owned native processes,not a Workspace or other service.

Compile/test/native CI is still pending at publication;no passing run,measured
latency reduction,whole-population parity or generic fork-safety claim is made.
Current13d4606binary/host are not rebuilt or replaced. No new local acquisition,
research matrix,observer,limit or Agent. Four RQs/paper unchanged;full matched
resource evidence and next original42cohort retain priority.
