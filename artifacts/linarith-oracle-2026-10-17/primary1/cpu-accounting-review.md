# External-process CPU accounting — root self-review

Existing immutable streams, not a new experiment. Per-process cumulative self
user+system maxima are deduplicated by(pid,creationtime). The native collector
samples itself first; its exact cell rusage replaces that sampled lifetime CPU.
Each cell starts fresh native workers. Summing descendant self counters
excludeschildren_user/system and does not count the same ancestry twice.

Reference sample maxima: wrapper0.38s, native-repl process2074.03s,
additional child981.41s. Exact collector312.537590s yields at least
3368.357590sprocess-tree CPU, above recorded collector+waited2387.679575s.
Prototype wrapper0.39s, native-repl1714.21s, two further children253.62and
385.36s. Exact collector224.174179s yields at least2577.754179s,
above recorded collector+waited1941.895012s.
These are sampled lower bounds: unseen processes, incomplete reads and final
CPU tails remain. Ratios of lower bounds are not exact CPU reduction estimates.
Take the maximum of overlapping counter bounds, not their sum.

The first prototype's native/arith-oracle/farkas process names were observed
live in the root tool transcript. Those past names are not freshly verified
after exit. First-reference raw samples do not record executable names, so
this report does not invent a directly observed past identity for its extra
child. The ongoing second pair now has an actual live executable/parent/start
snapshot, to avoid relying on reconstructed identities later.

The gap proves the existing waited-child counter is not exhaustive on these
closed captures. It does not assign all missing work to an LP algorithm,
derive a device ceiling, correct whole wall time or change the measured
1.347247first-pair ratio. Strong-stage analysis now exposes the same accounting
scope and both lower-bound/recorded counters, without calling their ratios
complete-verification time shares. Old raw fields remain unchanged.

Original sources/outcomes, all88unused-variable-warning differences, whole
clocks, threepairs and1.5xrule are untouched. This is one root's source-grounded
self-review, not independent audit or a new research contribution.


The updated paper compiles with Tectonic exit0 to19pages. The changed CPU
accounting region on page12is rendered and visually inspected, without
clipping/overlap. Full phase populations, repetitions and finalgates remain
pending; this is a finite interpretation/analysis repair from existing data.
