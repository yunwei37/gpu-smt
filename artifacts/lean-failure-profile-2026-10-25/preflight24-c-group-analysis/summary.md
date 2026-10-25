# Native failure-hotspot measurement — root self-review

Completed diagnostic: 24 selected sources; actual body-profile data for 24.
Baseline-fixed groups retain the original timeout/error/resource classifications, even if profiled outcomes differ.
This is a diagnostic, not a performance improvement or independent audit.

Counter CPU below includes completed child-subtracted runtime-boundary CPU and the last observed open-frame CPU.
Inclusive wall/CPU spans overlap. One-second endpoint CPU attribution to active tactics is an estimate, not exact per-tactic time.
Cumulative HTTP envelopes overlap across concurrent candidates and are not whole elapsed fractions.
Resource-failure body clocks are missing, never zero-cost. Gzip termination/clock/table/sampling limits remain in result.json.

| Baseline group | Sources | Baseline cumulative HTTP (s) | Profile statuses | Missing baseline body clocks |
|---|---:|---:|---|---:|
| all_selected | 24 | 444.836940 | {"lean_error": 18, "resource_failure": 1, "timeout_error": 1, "valid": 4} | 1 |
| baseline_timeout_error | 1 | 300.073289 | {"timeout_error": 1} | 0 |
| baseline_lean_error | 18 | 61.633974 | {"lean_error": 18} | 0 |
| baseline_resource_failure | 1 | 80.564811 | {"resource_failure": 1} | 1 |
| baseline_valid | 4 | 2.564867 | {"valid": 4} | 0 |

## all_selected: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| simp | 323.052740 |
| elaboration | 76.300798 |
| tactic execution | 16.231094 |
| typeclass inference | 6.965283 |
| norm_num | 0.244716 |
| type checking | 0.232740 |
| ring | 0.118950 |
| parsing | 0.020826 |
| linting | 0.018002 |
| attribute application | 0.000075 |

### all_selected: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Lean.Parser.Tactic.simpAll | 314.975448 |
| outside active tactic boundary | 76.979899 |
| tactic execution / nlinarith | 13.001964 |
| tactic execution / Lean.Parser.Tactic.simp | 2.000391 |
| tactic execution / Mathlib.Tactic.normNum | 1.000182 |

## baseline_timeout_error: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| simp | 298.570266 |
| tactic execution | 1.094275 |
| typeclass inference | 0.006809 |
| elaboration | 0.004717 |
| parsing | 0.000546 |
| linting | 0.000125 |
| attribute application | 0.000002 |

### baseline_timeout_error: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Lean.Parser.Tactic.simpAll | 298.965708 |

## baseline_lean_error: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| simp | 23.795525 |
| tactic execution | 13.636298 |
| typeclass inference | 6.422794 |
| elaboration | 0.289554 |
| norm_num | 0.232973 |
| type checking | 0.164714 |
| ring | 0.081587 |
| parsing | 0.016711 |
| linting | 0.004672 |
| attribute application | 0.000058 |

### baseline_lean_error: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Lean.Parser.Tactic.simpAll | 16.009740 |
| tactic execution / nlinarith | 13.001964 |
| tactic execution / Lean.Parser.Tactic.simp | 2.000391 |
| tactic execution / Mathlib.Tactic.normNum | 1.000182 |
| outside active tactic boundary | 0.977866 |

## baseline_resource_failure: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| elaboration | 75.938883 |
| simp | 0.686950 |
| typeclass inference | 0.037503 |
| tactic execution | 0.003271 |
| parsing | 0.000743 |
| linting | 0.000097 |
| attribute application | 0.000002 |

### baseline_resource_failure: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| outside active tactic boundary | 76.002033 |

## baseline_valid: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| tactic execution | 1.497250 |
| typeclass inference | 0.498177 |
| type checking | 0.068026 |
| elaboration | 0.067643 |
| ring | 0.037363 |
| linting | 0.013108 |
| norm_num | 0.011743 |
| parsing | 0.002826 |
| attribute application | 0.000014 |

### baseline_valid: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|

## Scope and remaining decisions

Original-status changes: 0; all changed IDs remain in result.json.
Diagnostic capacity/clock flags: {"clock_errors": 0, "dropped_keys": 0, "frame_overflows": 0, "sampler_error": 0, "truncated_keys": 0}.
Sampling transition/gap counts: {"source_transition_intervals": 18}.
Per-source.csv lists every selected attempt, original/profile outcome, observed cost, missing clock and top measured boundary.
Per-source.json retains full named component and sampled tactic data; result.json retains open frames and stream completeness.
Named tactic boundaries do not automatically expose nlinarith preprocessing, product generation, LP and certificate subphases.
Any unmeasured internal subdivision remains unknown; do not borrow fractions from another corpus/version/run.
Select the next own-method experiment from this completed distribution only after raw-result review.
A small preflight may validate the analysis path but cannot select a whole-cohort dominant tactic.
