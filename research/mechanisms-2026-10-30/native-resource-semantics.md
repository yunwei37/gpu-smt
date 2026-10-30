# Exact native guard and measurement scope

2026-10-30UTC;M;self-review. No runtime flag changed by this clarification.
All raw historical argv/receipts remain intact.

The recorded -M8192flag is **not an allocator-arena limit**. Matching pinned
Lean source runtime/memory.cpp:132–145 uses a periodic cooperative check:
first peak RSS as a fast path,then current RSS,then a memory exception if
above its limit. set_max_memory_megabyte multiplies by1024². It is neither
RLIMIT_AS nor a kernel hard RSS quota. Earlier M entry reports' wording
"allocator setting" was inaccurate;this is the forward correction. Sampling
and cooperative checks can overshoot. The16GiB M allocation and the native
8GiB guard are different quantities;this diagnostic point is not a no-guard
48GiB production-resource point.

The historical receipt field native_allocation_limit=50000000records the
CLI-T flag value. It must not be read as a global whole-source quota on
IO.getNumHeartbeats deltas. SDK --help calls it per-task allocation timeout;
Core source options,task/scoped counters and C++ kernel check heartbeats
are distinct ledgers. Raw whole-source counters can exceed the flag's
printed numeric value. Future receipts add exact flag/scope text without
changing execution flags. No unverified unit multiplier is asserted.

Source evidence:the retained matching be6c4894 SDK source has
Init/System/IO.lean:262defining the small-allocation observation and
runtime/interrupt.cpp:36–39incrementing the separate kernel check counter.
Metadata cannot collapse those into one physical-work budget.

run_finite's1s RSS sampler follows the declared controller PID/birth and
its descendants. Its sampled peak covers that capture tree,not all four
branches or unrelated analysis exec trees. Short peer analyses/builds were
kept within M's substantial headroom,but the capture-tree reading is not
a comprehensive all-branch hard quota. ru_maxrss is separately retained:
a subsecond control can naturally finish between RSS samples. For example
the auxiliary witness's14MBinitial sample missed its524MBnative highwater.

No security,workspace quota,other process,affinity permission or scheduler
was changed. All current M native captures have terminal receipts and
retired identities;future guard qualifications remain explicit.
