# Plan — source-only memory forecasts from the completed native population

2026-10-27; root thread only; concurrent supporting node of the ongoing
step0069 pair. RQ3 asks how prepared branching changes end-to-end latency,
throughput and memory at equal resources. The prior time/acceptance predictor
did not improve frozen first-success work; do not retune that predictor.

The separate question here is whether existing source features predict the
native attempt's observed memory occupancy better than the learned global
median. The completed original7,808 native cell already contains real attempt
peaks,preemptions and resource failures. Reuse it rather than start a new Lean
collection. The active same-version native/prepared pair stays unchanged.

Use the existing comment-stripping27source features from features.py and one
L2-regularized linear regression of log observed peak RSS,penalty1,unpenalized
intercept. Whole tasks stay together in five deterministic folds (sorted
task IDs modulo5). Standardization and coefficients use training folds only.
No hyperparameter search,task lookup,source-ID/outcome input or hindsight
ranking. Reuse the same folds for a training-only median constant. This
constant is a predictive comparison with more training observations than a
causal online median,not an exact replay of engine admission.

Target maximum reported observed peak over each candidate's actual attempts.
Zero/missing peaks remain unknown and are excluded from numeric fitting,
with explicit counts/IDs. Timeouts,resource failures and preemptions remain
in the records and are reported separately: their peaks are finite-resource
observations/lower bounds,not uncensored intrinsic demand. Include these
observations in fitting,not just successful proofs. Report MAE in GiB,median
absolute log error,underprediction by more than a factor2,and positive byte
shortfall/overreservation. Do not cap predictions at a worker limit or reject
a candidate from a forecast.

Also sum actual preempted-attempt elapsed/observed occupancy to quantify the
recorded discarded work. Concurrent attempt sums are not removable wall time
or an Amdahl ceiling. No admission replay,new preemption count,accepted-set
parity or performance advantage is inferred from these offline statistics.

A positive result motivates a future source-policy qualification after current
data finish; a negative/mixed result bounds this specific fixed model,without
parameter grids or research closure. Research role is supporting offline
evidence/dependency of admission work,not a standalone RQ answer or novelty.

Use the existing support-runner on CPU11,one BLAS thread and combined owned-tree
RSS sampling. Abort only new analysis work if combined pressure crosses48GiB;
do not disturb the healthy native capture. Record overlap as a performance
confound. No logger/parser framework or extra native group. Preserve input
provenance,all heldout predictions/models,script,raw execution and self-review.
