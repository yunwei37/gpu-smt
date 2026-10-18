# Nat/Int adapter coverage: functional, slower in the real preflight

This is root self-review of the declared ten previously unsupported sources.
No other Agent performed implementation or review.

## Mechanism and actual execution

The candidate reuses Mathlib's filterComparisons,removeNegations,natToInt and
strengthenStrictInt proof transformations before the existing coefficient
oracle. Naturals are lifted with proofs into integers. Integer division is
kept as an atom in both HDiv and normalized Div syntax; it is not field
division. Exact repair,Lean checking and native fallback remain active.

The build succeeds. Source and generated BatchOracle are retained. The same
eight-queue protocol,max eight candidates,CPUs8–11,48GiB and native timing
REPL are used throughout. Diagnostic logging is enabled on the ten-source
qualification,so these are qualification clocks rather than a final
uninstrumented1,000-source result.

| Condition | Whole seconds |
| --- | ---: |
| Fresh native reference | 144.555359582 |
| Current CPU oracle | 143.750716129 |
| Lifted Nat/Int CPU oracle | 158.015169893 |

Every condition completes all ten sources with identical native verdicts and
non-message payloads. The new adapter is9.92%slower than the current oracle.
The actual original24Real/Rat qualification also completes: native30.132526730
and candidate22.912470440seconds,all24verdict/non-message fields agree.
That small qualification is not a full-cohort or replicated speedup claim.

## What worked and what did not

The old adapter records2,348unsupported-carrier fallbacks on these ten
sources. The candidate eliminates that error and records1,778direct success
events plus618no-certificate fallbacks. These events include recursive
equality branches; they are not distinct candidate or whole-tactic counts.

On observed successful branches,the candidate sums0.188seconds of export,
1.878seconds of numerical round trip and88.451seconds of Lean certificate
construction/checking. The oracle's successful-branch numeric LP counter
sums0.348seconds and product generation0.090seconds. These are overlapping
cumulative walls,not a partition of158.015seconds. Failed numerical branches
lack these uninstrumented-adapter timing counters; they are not treated as
zero or used to prove a GPU impossibility bound.

The adapter genuinely engages but doesnot improve the measured end-to-end
preflight. Removing the unsupported-type gate alone is insufficient. These
observations reject this implementation as a performance replacement; they
do not prove Nat/Int acceleration or all GPU designs impossible.

## Disposition and reproduction

No full candidate performance matrix is admitted. The maintained Oracle.lean
remains the earlier qualified Real/Rat adapter with native fallback for other
types. The full attempted adapter is retained in source/Oracle.lean and can
be rebuilt with the canonical builder:

    python3 bench/lean-native/linarith-oracle/build-race.py \
      --out /tmp/gpu-smt-reproduce-nat-int \
      --oracle-source artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/nat-int-oracle/source/Oracle.lean

The builder now reads the maintained adapter by default instead of a stale
OS-temp copy; explicit source selection is for reproducibility,not solver
tuning. Use the declared input-unsupported10.jsonl,launch metadata and row11
for execution. The original build source snapshot predates this source-path
CLI and remains historical provenance.

All raw old/new/Real qualification records,build logs,source snapshots and
machine summaries remain adjacent. The active primary profiler used its
previously compiled adapter and is unaffected by this source experiment.
The original fourRQs,systems novelty target and GPU continuation condition
remain open. Reviews are self-review,not independent audits.
