# Real32 FIFO/task-memory development comparison — running

Release8045cca builds successfully after all prior native owners retire:
12.010628s,336,310,272B sampled build-group peak,no guard kill.
The run copies/fixes this executable outside Cargo target. Original prior
guard-killed release attempt remains preserved,not reused.

Real preflight on originals7328/7329accepts both under FIFO and task-memory,
with identical native outcomes and all4native births retired. This engagement
does not test heavy memory feedback or prove a speedup.

The full32input is the exact prepared outcome-informed heavy/ordinary cohort,
all/reusefalse/300s,pinned native4.9Mathlib,48GiB actualRSS/CPU8–11/fourone-core
dynamic leases,noAScap. FIFO starts,then task-memory starts after cell retirement.
Each policy history starts cold;no prior result or memory peak is injected.
Raw streams use existing/tmp location in launch.json;do not replace executable,
SDK or input mid-run. Existing measure/compare/archival,no new scheduler/AI.

No complete fullpair/accepted-set/throughput result yet. Selection bias,observed
peak censoring,conservative reservation,fixed-order shared host and1s watchdog
overshoot limit interpretation. Source policy is opt-in;no default enablement,
novelty or strongest-warm-service claim. Root execution/self-review only.
