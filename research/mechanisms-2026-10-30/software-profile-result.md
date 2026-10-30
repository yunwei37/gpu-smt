# Software CPU residence: observer IR is not candidate IR

M branch;2026-10-30UTC;self-review. PMU remains unavailable. No host or
security setting changed. These are process-local2ms CPU-timer instruction
samples,not cycles/IPC/LLC/dTLB measurements. Raw PCs,maps,stdout/stderr and
receipts remain outside Git on PVC. All native processes naturally retired.

## Native qualification and median diagnostic sample

Four short controls xstock/library-off/on return12/12 with identical flags,
diagnostics,InfoTrees and rawHB; sampler actually engages. Next31 units
(three frozen median inputs repeated10times,one manual true closed list
fold) xthree cells return93/93. Sampler-on matches stock for all31 flags,
diagnostics,InfoTrees and rawHB. Library-off's first source differs by2 raw
HB(964274 vs stock/on964276); all flags/diagnostics/InfoTrees still match.
The strict all-three-cells qualifier is false,and remains explicitly false
in pc-native-representatives.json. Do not hide that difference.

|Body kind|Samples|IR residence %|Cold RC lower bound %|Alloc/free lower bound %|Named table lower bound %|
|---|---:|---:|---:|---:|---:|
|Ordinary no-error median x10|499|5.21|14.03|13.63|5.81|
|Ordinary error median x10|328|3.96|9.76|10.67|9.45|
|Budget-interrupted median x10|1558|2.25|10.08|10.14|9.76|
|Manual List.range4000 fold,prefix only|146|0.00|8.22|7.53|10.96|

The last row fails at whnf heartbeat3000. It is not a successful closed
computation or a kernel-check profile. The failed control is retained; no
silent replacement or accepted-proof claim. A separate actually verified
closed computation below covers that missing case.

Body CPU totals stock5.041618s,off5.047695s,on5.067284s. Whole-process wall
36.119517s,36.252681s,37.254657s. One ordered pass does not identify causal
tracing overhead. Peak sampled own RSS3.806568448GB,within M16GiB.

Of16649 samples,2531 belong to candidate bodies and14118 to phase0(outside
bodies). Phase0 includes11903 IR-interpreter-related samples,mostly lookup
and collector/InfoTree export. Whole-process IR would therefore mostly
profile our measurement program. It cannot be credited to Mathlib strategy
execution or used as a precompilation opportunity.

The explicit-only scenario of deleting all observed body IR residence while
freezing every other cost yields about1.055/1.041/1.023x for the three median
classes. This is neither a practical AOT forecast nor a general upper bound:
compilation can also change boxing,allocation and helper-call work. Per-PC
samples do not attribute those effects causally. Median diagnostic repeats
are not weighted full7808 demand. The SDK import point also lacks the native
Mathlib closure loaded by the historical prepared strong backend.

## Actual ordinary-kernel digits recheck

The mathematical declarations of DigitsCertificate.lean are unchanged.
PCDigitsCertificate.lean adds only IO measurement around the existing warm
Environment.addDeclCore recheck; the computed_count theorem remains axiom-free.
The equivalence/bridge retain only their original standard axioms. No
native_decide,new proof axiom or trusted external arithmetic result.

|Cell|Whole wall seconds|Reported recheck interval seconds*|Recheck rawHB|Native kernel peak RSS bytes|
|---|---:|---:|---:|---:|
|Stock|30.729935|8.657968|57844572|2369527808|
|Sampler loaded/off|30.679967|8.633309|57844572|2369593344|
|Sampler on|30.781255|8.700093|57844572|2375897088|

*Self-review found this initial NS field stops after sampler shutdown/msync
and HB logging,so it includes post-kernel measurement work. It is not a pure
kernel duration. The4334 PC samples are limited to the kernel phase and
remain usable as residence observations. The previous uninstrumented8.5572s
kernel recheck remains separate valid evidence. Timing correction is pending
a forward validation,not silently applied to these three raw results.

All3 exit0; non-timing stdout and axiom lists identical; all retired.
Maximum1s sampled whole own-tree RSS2,402,959,360bytes (~2.24GiB),distinct
from per-native kernel high-water RSS. No sampled budget failure.

Kernel phase has4334 samples:0 IR-interpreter;727 cold RC(16.77%);479
allocation/free(11.05%);819 named hash/table functions(18.90%);113 unresolved
(2.61%). Leading symbols:lean_dec_ref_cold727,replace_rec_fn::apply554,
expression-hash-table find461,lean_alloc_small318,replace_cache::insert279,
hash(expr)181. All4334 belong to the known kernel recheck interval; the
small direct type_checker-name bucket is NOT the total kernel share.
Structural replacement,cache operations,RC and allocation are kernel work
even when helpers have generic symbol names.

## Interpretation and limits

Reference-count/allocator/table percentages count explicit helper residence,
not inlined operations or complete algorithmic costs. Categories are
disjoint naming buckets; no stack attribution or memory-bandwidth inference.
Periodic sampling can alias and is not an IID confidence-interval experiment.
The closed kernel phase runs compiled C++ expression processing already;
compiling more Mathlib tactics does not remove its structural reduction work.
This supports investigating certificate representation/term construction and
checking allocation,not a claimed new generic AOT mechanism. Reflection and
external-proof reconstruction are established prior art.

Current small digits inputs fit machine words; no demonstrated GMP-specific
speedup. The previously measured grid rechecks/4million-cell extrapolation
remain separate evidence,not a new executed full-grid certificate.

## Forward pure-timing correction

The first window above remains raw historical evidence. A new explicit point
(pc-digits-pure-timing) moves the stop clock immediately after addDeclCore,
before diagnostics,sampler stop or msync. Results:8.645868s stock,8.679851s
loaded/off,8.516725s on;all3exit0,identical proof/axiom output,rawHB57844573
in each cell. HB scope differs by the relocated clock call and is not
borrowed from the earlier window. Whole source still includes an explicit
second kernel check; this is not an optimized proofserve end-to-end result.

Corrected point4258kernel-phase samples:0IR,699coldRC(16.42%),462alloc/free
(10.85%),777namedtable(18.25%),124unresolved(2.91%). This agrees qualitatively
with the earlier kernel residence observation. Runtime variations in one
ordered pass do not prove sampling is free or produces acceleration.
