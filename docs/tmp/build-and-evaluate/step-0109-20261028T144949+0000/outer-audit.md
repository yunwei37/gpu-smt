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

Source4283acbnow passes actual engine40710734996/native job122894986422,
Rust job122894987113and smoke40710735308/job122894988281. Complete archived
logs show70workspace/5explicit native/35Python controls. The added real
mask case executes within the existing import-parent differential. No measured
latency reduction,whole-population parity or generic fork-safety claim is made.
Current13d4606binary/host are not rebuilt or replaced. No new local acquisition,
research matrix,observer,limit or Agent. Four RQs/paper unchanged;full matched
resource evidence and next original42cohort retain priority.
