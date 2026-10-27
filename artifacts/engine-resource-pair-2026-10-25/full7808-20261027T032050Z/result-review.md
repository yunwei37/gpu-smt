# Completed native/Mathlib-derived population pair

Root self-review,2026-10-27. Original admitted plan/preflight:step0069.
Frozen source1f38be7,unchanged pinned Lean4.9rc1/Mathlib/native/prepared host,
canonical7,808 candidates/all/no reuse/300s,CPU8–11,four one-core leases,
48GiB sampled aggregate budget,no fixed AS cap. Native first,prepared second.
This is an own-engine component comparison.

| Metric | Fresh native | Mathlib-derived |
|---|---:|---:|
| Original candidate results |7,808|7,808|
| Accepted / rejected |3,013 /4,665|3,013 /4,665|
| Timeout / resource exhausted / backend error |87 /41 /2|87 /41 /2|
| Whole cell seconds |28,391.984735|22,891.507755|
| Engine lifecycle seconds |28,390.654880|22,890.193560|
| Physical attempts |7,852|7,850|
| Exclusive retries |44|42|
| Watchdog-marked attempts,including solo terminal failures |85|83|
| Full-monitor sampled peak RSS,GiB |48.774902|48.927013|

Whole-cell ratio1.240284609x;19.373344%less elapsed. This charges input decoding,
runtime,shutdown,capture serialization,gzip and compressor retirement.
It is one fixed-order/shared-host observation; bounded development builds and
unit proofs used CPU11 during the group. No counterbalanced causal estimate,
strongest-warm-service superiority,GPU gain or novelty follows. All operational
failures stay charged. Do not pool with old24GiB-AS/two-worker clocks or splice
the prior ENOSPC prepared prefix into this pair.

## Decisions, output and failures

Exact batch/source/order,7,808unique IDs per cell,zero cache/coalescing,one
consumer result per index and final Complete(7808) are checked. All statuses
and3,013accepted IDs match;142solved problems,102unsolved. New native statuses
also exactly match the preceding uncapped dynamic native population. The
historical accepted-to-timeout regression against an earlier baseline still
exists;this does not prove universal equivalence across resource points.

7,660responses differ solely because prepared omits empty ast:[]. Removing
only that field for this audit leaves zero other response differences,including
messages/positions. Originals remain unmodified.86operational error strings
differ;87timeout IDs match. Status equality is not raw-byte/AST/artifact
compatibility or universal isolation proof.

All41terminal resource failures per side are watchdog preemptions during
exclusive retry,not semantic rejection or newly attributed bad_alloc. Two
backend faults per side,IDs2325and3209,retain native EOF and deep simplex
recursion stderr tails. Exact native crash cause remains unknown. No exclusion
or classifier change converts them into rejected proofs. Full error strings
are in each cell's operational-failures.json.gz and raw captures.

Prepared execution records14actual single-thread parent preparations,each
loading5,545modules,13evictions and62fresh-fallback event rows. Thus Mathlib is
not loaded literally once over the full population;one preparation serves
disposable children until resource eviction. Fallback rows are not62distinct
failed candidates.

## Resources, tails and retirement

The1s sampled policy overshoots48GiB:full-monitor peaks are52,371,652,608B and
52,534,980,608B. Thinned journals have lower maxima52,207,243,264B and
52,265,881,600B,with45/33over-budget samples. Do not claim a hard quota or use
retained maxima to contradict the full-monitor peak. At most4registered leaders
are observed;this is not proof of4busy cores.

The fresh-native slowest1% cohort sums overlapping attempt walls26,204.199384s
versus25,242.089170s prepared. Slowest10% sums56,518.293556s versus54,771.211589s.
These exclude queue and are not lifecycle,removable wall time,Amdahl shares or
statistical significance. All cohort IDs remain in comparison.json.

15,736recorded PID/birth pairs have zero currently matching live non-zombie
processes;controller457460retired. This is not independent authentication of
unregistered descendants. Consumer Complete alone was not shutdown proof.
Physical journals and final histories agree on ID/exclusive multiplicities.
85/83raw-native status records differ from wrapper statuses at watchdog
classification after journaling;raw native outcomes remain unnormalized.

## Recompute and interpretation

Run python3 analyze.py from this artifact directory. audit.json recomputes
membership,decisions,fields,multiplicity,resources,preparation and retirement.
comparison.json,terminals and both compressed physical/consumer/RSS journals
retain complete evidence. ingestion.json records byte-for-byte copies and
original locations. Original/tmp files remain. No new collection ran.

Run status:complete for this declared support pair.
Tested hypothesis:supported for population decision equality and descriptive
component benefit;raw-output compatibility is limited.
Research value:supporting;paper impact:local RQ2/RQ3 evidence.
Next:advance own load-aware method and closed-CNF native checking.
No RQ closed,no milestone/acceptance claim,no independent audit.
