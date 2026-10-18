# ProofNet complete component comparison

Root self-review, 2026-10-18. All original5,952candidates returned in the
three admitted conditions. No filtered successful-only timing.

| Condition | Whole seconds | stock/condition |
|---|---:|---:|
| Module-loaded stock fallback |1151.883128794|1.000000|
| Native-preprocessing oracle component |1160.922449882|0.992214|
| Direct certificate oracle component |1178.934375398|0.977054|

Each returns413complete,5,523rejected,12operational and4incomplete.
Per-source verdicts and non-message response fields match exactly. Four
native and five direct message differences are retained. All12operational
indices and all4incomplete indices coincide. Three failed REPL requests
require native retirement in every condition; they remain charged, not
dropped or counted as proved theorems. Parent normal exit does not turn
those failures into successes. All413completed sources are preserved.

The direct condition is2.35%slower than the module-loaded stock condition
in this one fixed-order, shared-host observation. Thus the selected-Goedel
1,000-source improvement has not generalized to this4.9ProofNet component.
No confidence interval, global CPU optimum, GPU result or entire Kimina
service speedup follows.

## Baseline and implementation scope

All modes import the same extra adapter module. In its actual elab_rules,
explicit argument elaboration precedes the GPU_SMT_FORMAL_MODE test in run.
Therefore the stock fallback is not a pristine unmodified Mathlib frontend.
The native-only mode ports the certificate-search component; it is not the
full4.27Fast frontend. This limitation cannot be repaired retrospectively
by relabeling these clocks. A future positive strongest-baseline claim
would require its actual matching control.

Each uses four CPUs12--15, four-command warm batches, upstream48GiB and
300srequest boundary; original headers with source-native fallback when
they do not match the standard header. No device computation. Collected
self+waited-child CPU is not exhaustive descendant CPU, especially at
forced retirements. Request latency groups include headers and commands,
not isolated candidate or LP duration. Operational stderr is not guaranteed
complete for generic ReplError; recorded failures are retained as observed.

The closed raw source-indexed results, requests, resources and terminals
are under proofnet/{stock,native,direct}. proofnet-result.json is a stable
closed-dataset extraction from analyze.py; miniF2F remains independently
active, not a completed six-cell matrix. No new measurement was launched
from this result and no active writer or frozen library was changed.
