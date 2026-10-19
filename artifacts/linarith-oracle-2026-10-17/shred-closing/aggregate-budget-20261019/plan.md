# Aggregate-memory repair requested by the user

The previous two-source submission point did not bound the retained server
pool: three REPLs were still live. Stop the sole verified experiment owner
before its next method starts, retaining original partial outputs. The
recorded nine processes sum38047547392RSSbytes at stopping, zero survivors.
This is an explicitly new requested resource point, not a software speedup.

Use at most two live native REPLs, each24GiB address-space limit, in both
miniF2F conditions. Two times24GiB equals48GiB. Restrict the actual live pool,
including startup and asynchronous retirement, rather than only SDK request
concurrency. No Workspace/host/container quota, permission or other project
setting changes. Parent/process accounting includes the whole owned experiment
tree, including wrapper/server/REPL/backend, conservatively summing RSS.

A watchdog outside the service event loop samples that tree every second.
If total RSS exceeds48GiB, record process birth/PID, actual source ID/phase,
largest native REPL RSS and aggregate, then kill that owned process group.
Resource-limit failures and watchdog kills become explicit resource_failure
outcomes, with original error/exit/raw evidence, not accepted proofs or normal
Lean rejections. No global PID/name kill or foreign Workspace access.

First execute24original candidates in matched native/SHRED arms at this point.
Independently exercise the same watchdog kill/attribution path at a lowered
test-only threshold on real candidates from that cohort; do not allocate48GiB
just to trigger a safety test. Keep that injected-failure run separate from
the normal48GiB qualification and all performance data. Verify actual process
limits, maximum live native count, RSS samples, largest-victim choice, source
attribution and retirement before a fresh full7808-source comparison.
Only one full acquisition runs. Do not resume obsolete48GiB-per-worker queues.
Raw old partials and earlier clocks remain separate and are never spliced.

One-second monitoring is a sampled response, not a kernel-enforced hard RSS
cap: brief overshoot is observable and must not be claimed impossible.
The24GiB address-space bounds and live-worker ceiling provide the proactive
constraint; the whole-tree RSS monitor includes non-REPL overhead. Root-only
implementation and self-review; no Agent/new scheduler/service is introduced.
