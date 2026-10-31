# M systime003 — frozen finite attribution/ablation matrix actually queued

EXPERIMENT: user explicitly requested freezing/queuing remaining tasks while
the W batch owns P cores. matrix.csv has90unique native cells; every
(module,configuration,instrumentation)cell has3repetitions:
baseline plain/stat/record/trace for3modules;4single-factor plain variants
(no-M,one worker,mmap threshold only,trim threshold only); no-M stat/trace
triplets for the direct getrusage/systemCPU comparison.

The existing UMoments9 plain producer is retained. Its completed cells are reused;
only missing repetitions after that actual PID/birth retires can be filled.
An existing partial capture is preserved and stops the queue for inspection.
No duplicate native process or automatic outcome-changing retry.

Matrix controller11027/birth747568388 is actually live and queued behind
the existing M7507/O7536on the common FLOCK, with no valid native matrix
result yet. Its frozen runner/inputs/task list are on PVC matrix-v3.
Each native child self-alarms<=1200s; outer group watchdog and same-Pod
native15GiB cgroup apply to all configurations, plus16GiB M tree sampling.
Queue waiting is separately recorded; no claim that the whole90-cell matrix
takes<30minutes. Each independently captured task is bounded; full queue can
take many hours. No scheduling mutation or whole-matrix lock monopoly.

WRITE: runnable finite matrix.py, matrix.csv, queue evidence and run cleanup.
The observer cannot release its slot with a live native cgroup: owned leftovers
are killed/scoped and retirement checked before another cell starts.
No parent cgroup limit, other Pod, sysctl or module is modified.

REVIEW — 自审: all30module/config/mode groups have3planned repetitions.
Frozen runner/list bytes match owning Git paths; this is launch qualification,
not completion or a measured attribution. No perf/plain pooling. Native source,
acceptance,diagnostic and .olean comparisons remain required actual outputs.
Root owns paper; only M systime paths touched. Goal active.
