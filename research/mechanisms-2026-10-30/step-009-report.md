# Step009 — local C-call model and late sampling preparation

2026-10-30UTC;M branch;self-review. No second Lean collection.

## EXPERIMENT
Analyzed existing four qualified native-control captures only. The C-call
reader validates source boundaries,unique IDs,parent lifetime,monotone clocks,
retirement and nonoverlap. It does not globally join InfoTree and C event
positions: failed speculative calls can appear only in the C tree.

The independent constructor/allGoals control has one unique aligned split,
two disjoint live-metavariable components and branch CPU0.317141/0.295423ms.
An optimistic local model removes0.295423ms from its own2.097613ms body CPU:
1.163924x,not measured parallel execution. The existential control shares a
live witness before its later goal and has no eligible allGoals split.
Its unmodeled opportunity is unknown,not zero true parallelism. Ordinary
error and budget controls retain separate classifications.

The C success tag is1 in these qualified controls (error0),verified against
the successful independent branch. No earlier assumption of the reverse
mapping is used. An initial parser expecting a thread field on exit failed;
exit records only carry IDs/clocks/tag. Parent source lifetime and optional
thread consistency are checked instead. Failed parser execution preserved
in the task transcript; no measurement data altered.

Prepared a late-start SIGPROF software PC sampler because early constructor
handlers can be overwritten during Lean initialization. A standalone200ms C
control compiled and naturally exited with100 samples at2ms CPU intervals.
No Lean sampler run during the active cohort; no native/software category
fraction yet. This needs independent native differential qualification.
No IPC/cache/TLB counter or complete allocation/reference-count cost claim.

## WRITE
Data:c-local-model-controls.json and late-pc-control.json;raw outside Git:
/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/.
Full DAG span remains null. Local models do not prove shared-state merge,
name generation,diagnostic ordering,cache or heartbeat semantics.

## REVIEW
Actual four-control reader checks passed. Independent live components=2;
coupled control not incorrectly assigned independent branch timing.
No application engine method enabled. Current matrix remains frozen.
