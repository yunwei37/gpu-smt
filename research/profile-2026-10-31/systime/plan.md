# System-time attribution — admitted characterization experiment

Self-review, 2026-10-31. Latest user characterizes rather than requires a new
acceleration mechanism. M owns only this directory; root owns paper integration.

Question: why do large original certificate modules spend39–52%CPU in the OS
and underuse8workers? Counterexample/control EnvelopePsiB has~4%systemCPU.
Process-scoped hardware counters, on-CPU native/kernel stacks and syscall
summaries distinguish memory/VM work, allocator traffic, memory-limit checks,
reference counting and task-pool synchronization. Syscall elapsed time can
overlap across threads and includes waiting; it is not exclusive kernelCPU.

Inputs: pinned OpenAI/math4eaee875/Lean4.34.1 commit5045d005/Mathlibd13f.
Grid original source and historical HB100k/-M8192/.olean;
UMoments9 and EnvelopePsiB original source/authored or native-default HB/
-M9216/.olean+.ilean+.c. Dependencies reused, setup excluded from native time.
Sources copied byte-exact to a fixed persistent source path before measurements.

All timed/profiled subprocesses taskset0–7 under the shared pcore.lock.
Preparation/analysis CPUs8–23. One M Lean process; <=16GiB own sampled tree,
finite native1200s self alarm, group1700s excludes no results and may censor
later repeats. Additional outer watchdog terminates only owned process groups.
New test-local native cgroup15GiB, constant across all valid cells, is created
under THIS Workspace Pod cgroup and removed after retirement. No parent limits,
other pods, host sysctls or modules changed. Cgroup charges include more than
RSS; sampling is not a hard RSS cap. No native AS cap.

First attribute UMoments9, then Grid and EnvelopePsiB:
three repetitions each for plain, perf stat, perf record dwarf8192 at99Hz,
and perf trace summaries. User/kernel cycles/instructions/cache/LLC/dTLB
separate on cpu_core PMU; faults/switches/migrations also recorded.
Multiplex running ratios and unsupported events remain explicit.
Full perf.data remains PVC; only small CSV/top20 stacks and method/results here.

After attribution, single-variable native configurations: baseline; only
glibc.malloc.mmap_threshold=128MiB; only trim_threshold=128MiB;
one worker (both CLI-j1 and matching LEAN_NUM_THREADS1 to avoid ignored env);
no native-M with the same outer cgroup. Each configuration >=3repetitions.
No plain/profile times pooled. Overhead compares whole matched triplets.
Compile decision and byte equality of .olean must be reported; no semantic
equivalence claim substitutes for byte mismatch. Preserve any nonresponse.

Preflight failures preserved: native helper accidentally reset P affinity once,
stopped and excluded; then RLIMIT_AS15GiB caused thread creation failures
during import3times, excluded as incomplete-module diagnostics.
Corrected native helper asserts inherited0–7 and uses cgroup rather than AS.
No result claimed until native returns and actual artifact/diagnostic checks.
