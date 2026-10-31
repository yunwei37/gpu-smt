# Startup results — instrumented first matrix
All 39 original-module builds, 39 import-only controls and three Mathlib controls
returned zero. Each of 13 selected modules has three adjacent build/import pairs.
The 13 were selected because their *historical* A-batch standard build was under
5 seconds. This is a conditional small-module cohort, not a probability estimate
of the complete repository.
Direct-import wall medians range 0.712–3.195 s, median 1.355 s. Median per-module
import/build ratio is 0.682; sum of import medians / sum of build medians is 0.678.
This is an observational fixed-cost control, not a proven removable speedup.
Import-only median native user CPU is 1.001s, system CPU
0.422s, peak RSS 3.113 GiB.
The Mathlib-only wall median is 3.002s.
All source-native C/ilean/olean output options remain enabled in both sides.

## Instrumentation qualification
The serial runner's waited-child CPU after this phase was 259.99 s; native
wait4 user+system sums to 205.945162 s. Their difference, about 54.045 s, is
observer and small phase-preparation CPU (tick precision 0.01 s), while measured
native wall sums to 194.168 s. This cost is non-negligible and is not subtracted
from wall time or hidden. A narrower min/median/max-module calibration using
own-task descendants instead of scanning the whole proc tree is queued behind
native replay/perf controls. Do not use these preliminary absolute timings as
unobserved production costs.

## Extrapolation, explicitly hypothetical
Multiplying each measured import-only median by 163,000 modules gives 32.23 to
144.68 serial hours; multiplying the cohort median gives 61.34 hours.
This is a scale illustration only, **not a total-build estimate**: short-module
selection, different dependency closures, filesystem/cache state, parallelism,
amortization and observation costs prevent population inference.
RSS/PSS are per-process occupancy and cannot be multiplied into required RAM.
Full smaps samples and raw commands are on the PVC path in README.

## State
Kernel replay and perf are not yet complete at this checkpoint. Only startup
columns are populated. The first package-shadowing attempt remains separate
and is not treated as measurement success. Review: self-review.
