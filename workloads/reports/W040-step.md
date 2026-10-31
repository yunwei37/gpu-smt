# W040: conditional precision extension preregistration

## EXPERIMENT
Prepared/not launched six new random modules from largest observed variance
stratum45,251members, excluding two fixed original pilot observations.
Python seed20261031/SRSWOR6of45,249, no easy-dependency filtering.
One draw needs2,116fresh imports; retained. Sole active native remains batchB.

## WRITE
Explicit conditional cell estimator:sum pilotCPU+R*mean(newCPU),
variance R²(1-n/R)s²/n; nominaldf5t only after6complete.
Separate from original42/global CI. Wrong manually written pilot name caught
by actual-plan assertion before publication, then corrected from plan.
Targets/method small CSV+README; raw plan on PVC.

## REVIEW
Same-thread self-review. No execution/CPU/CI improvement claimed for plan.
No replacement or adaptive pooled n8coverage claim. Scope only workloads/.
