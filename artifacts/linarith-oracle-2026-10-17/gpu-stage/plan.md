# GPU oracle stage: all-branch attribution and admission

Root executes implementation, capture, analysis, paper and self-review. No agent
delegation. CPU result remains 1.346679850013x; GPU is unfinished. The final
more-than1.5x rule uses the better CPU/GPU result against a matched strong native
warm baseline on the SAME frozen 1,000 enriched Goedel candidates.

## Measurement contract

Use Lean 4.27, pinned Mathlib, original ordered source bodies, width4 native batch,
CPUs12–15 and the existing whole-clock collector. All new captures inherit
48 GiB RLIMIT_AS; operational/resource failures stay in the population. Prefix
capture on CPUs20–23 remains untouched. Diagnostics use separate Lean namespaces,
shared library and Rust executables; no loaded prefix/primary file is rebuilt.

Record every direct and fallback numeric request, including cert:null and error
answers, not only checked successes. Record absolute CLOCK_MONOTONIC interval
boundaries and calling-thread CPU for LP scaling/build, floating simplex,
exact support repair, exact LP fallback, exact verifier, input parsing and
response packing/writing. Record polynomial expansion and matrix packing
separately. Lean logs client roundtrips (including mutex queuing), all direct
check attempts and timed fallback stages with exact source identity. LP
certificate-space rows include the strictness normalization row, columns are
hypothesis multipliers, nnz counts nonzero entries. Report all-input and actual
FP-matrix distributions, product pool sizes and generated products separately.

Pair Rust/Lean calls by explicit call_id, source and absolute time. Source bodies
map back to frozen candidate IDs; reject ambiguous/unmatched joins, never silently
discard them. Cover calls from candidates that ultimately fall back; classify
no-cert, failed Lean check and checked direct calls independently. Parent/child
timings are nested, not additive. Numeric protocol residual is measured CPU
minus disjoint solver/repair/etc stages; client interval minus in-service interval
is queuing/IPC/logging residual, not CPU. Logging overhead remains charged in
diagnostic whole clocks and is not subtracted from primaries.

## Amdahl and batching

Aggregate baseline/CPU-oracle primary times imply the GPU variant must remove
more than 10.22134% of CPU-oracle elapsed time to reach 1.5x if all other costs
stay fixed. This algebra is a target, NOT an empirical upper bound.

Measure all eligible multiplication and LP search intervals including fallback.
Report summed CPU, summed interval wall, interval union, and batch/candidate
placement separately. Overlapping sums cannot be called whole-wall fractions.
An optimistic upper bound may give all eligible work zero duration, including
all exact LP fallback search (more generous than a floating GPU can guarantee).
Any impossibility conclusion must survive the generous scheduling bound;
otherwise the data merely admit implementation, not prove GPU benefit.

Compute outstanding independent calls and same-wave candidate overlap as evidence
for batching; do not claim sequential branches in one candidate are simultaneously
ready. Report max/p50/p95 ready sets and the number of distinct candidates per
batch. Keep strong and oracle captures separate.

Heavy tails: identify slowest 1% and 10% using candidate native request clocks
when available; the current collector's four-source wave latency ties four
candidates, so report wave-based tails explicitly rather than inventing individual
latencies. Use original per-source Lean profile time only if it measures the
same boundary. Give component distributions in tails and unchanged outcome costs.

## Next conditional implementation

If data do not rule out >1.5x, implement RTX5090 batch LP (cuOpt/PDLP or a solver
chosen on measured shapes), floating support search only, CPU exact repair,
Lean certificate check, and strong fallback. Include export/pack/transfer,
queueing, repair, fallback and retirement in whole time. Real matched preflight
precedes same-1,000 paired execution; retain heavy tails and all failures.

A CPU miss alone never closes the project. Only completed GPU measurement or
a valid generous GPU upper bound can resolve the final criterion. Self-review
is not independent audit. No claim of OSDI acceptance.
