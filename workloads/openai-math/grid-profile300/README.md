# Own-denominator Grid diagnostic, censored at300s

Original pinned1,815,532-byte Grid source,4.34.1/Mathlibd13f,100000HB,
M8192,j1,CLI--profile/--stats,self-wall300s,CPU0-7.
Native returnSIGALRM after300.100s;user176.164s/system196.607s,
peak6,575,484KiB. Combined old/new sampledpeak11,688,361,984bytes(10.89GiB).
The foreground native/controller retired;old censored EPFL remains charged.

Native profiler emitted491completed over-threshold type-checking events and
1import event. These are partial,possibly overlapping durations,not complete
phase coverage or a disjoint fraction of the300s denominator. Final--stats
summary did not print after forced self-exit. No kernel/LP/global Amdahl bound
or proof of dominant tactic follows from event-duration sums.

690504minor/0major faults,24778976voluntary/127174involuntary context switches.
These process-level counters do not identify a specific syscall/algorithmic
cause. CPU may exceed wall because wait4 accounts multiple threads/children.
No single-core guarantee is inferred from requested-j1.
The previous unprofiled120s point is retained and not reweighted/rescaled using
this diagnostic. The earlier seven-module profiler overhead is not borrowed.

A separate unprofiled-j8 point has been launched within CPU0-7,M8192,100000HB,
self-wall1200s and batch1400s. Worker setting,instrumentation and wallbudget
differ;no isolated causal j8 gain or matched profiler overhead is claimed.
Its actual terminal is not asserted here. Full source+failed+partial profile/
memory/counters stay on PVC in openai4341-grid-profile300 and grid-j8-1200.
