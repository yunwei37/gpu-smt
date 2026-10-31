# M systime002 — historical concentration and attribution hypotheses

EXPERIMENT: recomputed the actual completed W26-module standard-artifact rows
read-only. Two modules contribute84.113%of systemCPU (exact value in summary);
all peakRSS/native-M ratios below1. Thus proximity to the RSS cap and generic
high import occupancy do not alone identify the cause. EnvelopePsiB is a
memory-comparable low-systemCPU control. These are descriptive old-point
numbers, not new on-CPU profiles or population totals.

Actual SDK disassembly confirms the200-call getrusage fast path; installed
headers confirm mimalloc allocation. This makes the no-M comparison a
source-supported causal test and prevents assuming GLIBC tuning controls
all Lean allocations. Neither is a measured root-cause attribution yet.

WRITE: historical numeric tables and scope, exact-diagnostic comparison and
profiler-overhead analysis paths, syscall summary reader. Stack parsing is
still awaiting a real recorded native capture; not claimed qualified.

REVIEW — 自审: UMoments9 baseline controller7507 is genuinely queued behind
the W7216P-lock owner and its current native process; no parallel timing begun.
Only one M Lean may run, bounded own-Pod cgroup and self wall ready.
No parent limits or other-lane workload changed. Goal remains active.
