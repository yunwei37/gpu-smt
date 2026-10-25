# Complete original Verina characterization — root self-review

All 189 official original task files at commit
66b3ce5014edafb20cb26b87c681e7f31847249f execute on pinned Lean4.18/Mathlib
aa936c36e8484abd300577139faf8e945850831a, with unchanged sources.
Native and diagnostic statuses exactly match: 46 exit0 with no explicit
admission, 139 incomplete references containing sorry, 4 actual Lean errors.
The four errors are advanced_28/55/74 and basic_22: upstream files reference
Std.HashSet/HashMap.emptyWithCapacity, absent at the pinned toolchain.
Their warnings/admissions and full diagnostics remain retained.
No source has been patched to turn a stub or version error into a proof.

Whole native/diagnostic lifecycles are 48.841915097/53.948885378 seconds, each
includes all process creation, file imports, frontend work and reaping.
This one native-then-profile block on a shared host is not a speed comparison.

The 46 no-explicit-admission files contain 47.583772333 accumulated traced
elapsed-slice seconds. Nearest traced simp/simp_all accounts for 8.909486395 s;
35.444889589 s has no traced tactic ancestor (including uninstrumented or
subthreshold work). No bv_decide, omega, decide or grind tactic span above the
default trace thresholds is present in this completed-reference subgroup.
The admitted-stub group has 0.288924762 s of traced omega, which is not proof
of completed specifications. The source corpus therefore does not currently
supply a large measured SAT/LRAT workload. This does not close the code-verification
direction: the real SLLVM references with bv_decide remain the next source target.

Exclusive tracing weights come from Lean's actual Firefox exporter, whose source
is retained compressed. It builds positive weights from elapsed intervals between
child traces and synthesizes threadCPUDelta from those same intervals.
These are wall slices, never real CPU samples. Threads/files accumulate, and
10ms default trace filtering can hide shorter tactics. No zero-cost or overall
Amdahl bound follows. All per-source statuses/times and traces are retained.

Peak sampled owned RSS 10,299,805,696 bytes, max two native Lean processes,
zero watchdog errors/kills, no timeout/resource failure, full retirement.
24 GiB AS per Lean and 48 GiB aggregate sampled RSS respected.
120s per-file point is the published Verina synchronous-checker default,
distinct from the 300s miniF2F service point. No cross-point timing comparison.
This thread reran trace attribution, checked all189 IDs/status pairs, inspected
all4 errors, and checked terminal/memory records. Root self-review only.
