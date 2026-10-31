# Observed artifact expansion, not a full-build forecast

Existing pinned public-source4.34.1 compiler records only; no new native run.
All .olean/.ilean/.c bytes come from completed compile_ok rows at M9216/j8/
authored options. Partial/failed/interrupted output is excluded from these
success-only ratios but remains on PVC. Population weighting is not applied.

| Observed point | Modules | Source bytes | Artifact bytes | Aggregate ratio |
|---|---:|---:|---:|---:|
| A original probability endpoints |26|1,418,376|77,581,124|54.697x|
| B selected completed dependencies |61|9,780,494|420,157,676|42.959x|

Individual module ratios reach230.725x in A and314.668x in B.
B's Shortening source9,339B produces2,938,688B:2,893,832olean,
36,814ilean,8,042C. This suggests inspecting serialized output, but does
not prove that all expansion is proof-term duplication or that export
dominates CPU. No source-line symbols, native phases or time fractions
are inferred from bytes.

The earlier static disk plan's2x/10x/40xrows were assumptions, not bounds.
Both observed aggregate ratios exceed40x; do not use40xas a safe upper
bound for later sampling or full-library storage.
These are incomplete/selected observations, not an estimate that every
source file has54.7xgrowth. No new full-build GB/CPU/RSS forecast or CI.
Default-root and all-source populations also remain separate.

Only requested compiler facets are counted, not source copies, cached
dependency duplicates, toolchains, raw perf data or external package caches.
The W capture retains private outputs and complete cache artifacts, so disk
use can exceed one artifact copy. Source size alone also cannot bound memory.
modules.csv and summary.csv support exact recomputation from each row.
