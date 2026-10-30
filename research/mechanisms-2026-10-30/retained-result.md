# M2/M4 — existing-data coverage and memory stress simulation

All interpretation is self-review. No main-engine feature is changed.

## M2:200-source stratified census, not yet a dependency-DAG measurement
Select50accepted,60rejected,50timeout and40resource-exhausted sources spread
uniformly across each stratum's measured physical-attempt cost rank. All200are
original7,808-source candidates.94have the old detailed profiler data.
The native top-level Syntax census finds290have units,106units containing<;>
and5containing all_goals. These are structural opportunities, not independent
jobs: nested tactic text/aliases and execution reachability require InfoTree.
No aligned per-call mctx dependency graph survives in these existing summaries.
Critical-path lengths, shared-metavariable edges and average available
parallelism remain unknown. Do not claim an average above OR below1.3.
A single-completed-atomic-call bound attempt is preserved separately;only two
completed requests qualified and their bounds are extremely loose, so it is
not used as a parallelism result. Need the actual bounded native InfoTree run.

## M4:four-core, observed-peak reservation sensitivity
Replay frozen sums of physical-attempt times, not consumer queue latency.
At per-core2/4/8/12GiB,total budget is8/16/32/48GiB. The budget-fit cohort sizes
are7718/7766/7766/7808;90/42/42/0sources exceed the observed-peak budget or lack
usable demand. None of the excluded rows was historically accepted. Censored
timeout/resource rows remain labeled; recorded peaks are not true maxima.

|GiB/core|fixed4 proxy s|fixed over-budget s|kill proxy s/killed|admission proxy s|
|---:|---:|---:|---:|---:|
|2|6410.77|1706.33|5797.69 /10|7194.06|
|4|10062.13|5011.09|6438.16 /49|18543.67|
|8|10062.13|3374.17|7494.06 /38|11498.37|
|12|13449.45|4797.96|9759.43 /48|23163.71|

Within each row the three policies use the SAME budget-fit subset and all3014
frozen accepted IDs survive. But fixed-pool memory exceeds budget, so its
apparent speed is invalid as a compliant baseline. The kill model completes
10/49/38/48fewer original terminal labels; dropping hard failed work is not
verification acceleration. These are modeled operational failures, not native
logical rejections. Actual same-load verdict parity has NOT been established.

The demand model reserves the observed peak throughout each job. Kill pressure
is detected immediately at dispatch, with optimistic zero kill/cleanup cost.
Admission uses hindsight peaks, NOT a source predictor or production forecast.
Full recorded peaks are charged per job even when an import parent contributes;
there is NO invented COW/shared-page discount. This conservatively models joint
admission, but does not identify the extra gain attributable to a shared parent.
New lower budgets/memory trajectories and latent peaks cannot be reconstructed
from this one48GiBpoint. All outputs/initial terminology revision are retained.

## Direction decisions
- M2:inconclusive;do not implement speculative execution from source counts.
- M4:supports accounting/admission as a feasibility necessity,not a novel
  mechanism or a measured service speedup. Reject any comparison that calls
  fixed-pool overcommit or operational dropping a same-semantics acceleration.
- M1:phobos repeats same-UID TERM/groupKILL errno13;both short children naturally
  exit0. Keep heartbeat/internal-memory bounded Lean and never claim a restored
  watchdog. No security settings were changed.
