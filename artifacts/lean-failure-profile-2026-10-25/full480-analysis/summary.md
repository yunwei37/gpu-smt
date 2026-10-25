# Native failure-hotspot measurement — root self-review

Completed diagnostic: 480 selected sources; actual body-profile data for 480.
Baseline-fixed groups retain the original timeout/error/resource classifications, even if profiled outcomes differ.
This is a diagnostic, not a performance improvement or independent audit.

Counter CPU below includes completed child-subtracted runtime-boundary CPU and the last observed open-frame CPU.
Inclusive wall/CPU spans overlap. One-second endpoint CPU attribution to active tactics is an estimate, not exact per-tactic time.
Cumulative HTTP envelopes overlap across concurrent candidates and are not whole elapsed fractions.
Resource-failure body clocks are missing, never zero-cost. Gzip termination/clock/table/sampling limits remain in result.json.

| Baseline group | Sources | Baseline cumulative HTTP (s) | Profile statuses | Missing baseline body clocks |
|---|---:|---:|---|---:|
| all_selected | 480 | 34602.439200 | {"lean_error": 355, "resource_failure": 42, "timeout_error": 83} | 42 |
| baseline_timeout_error | 83 | 24966.405942 | {"timeout_error": 83} | 0 |
| baseline_lean_error | 355 | 5639.602457 | {"lean_error": 355} | 0 |
| baseline_resource_failure | 42 | 3996.430801 | {"resource_failure": 42} | 42 |

## all_selected: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| tactic execution | 18215.515622 |
| simp | 9235.109871 |
| typeclass inference | 4845.609979 |
| elaboration | 1128.671248 |
| norm_num | 296.768056 |
| import | 275.651740 |
| type checking | 169.701005 |
| ring | 11.878487 |
| parsing | 0.500111 |
| aesop | 0.355656 |
| linting | 0.138305 |
| attribute application | 0.001502 |

### all_selected: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Mathlib.Tactic.intervalCases | 14097.721872 |
| tactic execution / Lean.Parser.Tactic.simpAll | 9464.257900 |
| tactic execution / Lean.Parser.Tactic.eqRefl | 3677.206527 |
| outside active tactic boundary | 1475.967465 |
| tactic execution / nlinarith | 1070.085041 |
| tactic execution / Lean.Parser.Tactic.refine | 1028.903524 |
| tactic execution / Lean.Parser.Tactic.simp | 685.993011 |
| tactic execution / Mathlib.Tactic.normNum | 581.917672 |
| tactic execution / linarith | 376.598949 |
| tactic execution / Lean.Parser.Tactic.omega | 373.974510 |
| tactic execution / Lean.Parser.Tactic.simpa | 302.021018 |
| tactic execution / Lean.Parser.Tactic.apply | 205.008504 |
| tactic execution / Lean.Parser.Tactic.allGoals | 140.993596 |
| tactic execution / Mathlib.Tactic.FieldSimp.fieldSimp | 41.005172 |
| tactic execution / Mathlib.Tactic.RingNF.ringNF | 35.003586 |
| tactic execution / Lean.Parser.Tactic.tacticSeq1Indented | 27.001996 |
| tactic execution / Mathlib.Tactic.Ring.ring1 | 23.996670 |
| tactic execution / Lean.Parser.Tactic.tacticSeq | 18.997922 |
| tactic execution / Aesop.Frontend.Parser.aesopTactic | 15.003184 |
| tactic execution / Lean.Parser.Tactic.decide | 11.000796 |

## baseline_timeout_error: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| tactic execution | 13210.515270 |
| simp | 7070.735290 |
| typeclass inference | 4046.522202 |
| elaboration | 268.970485 |
| norm_num | 149.648062 |
| import | 66.867234 |
| type checking | 15.910674 |
| ring | 4.037026 |
| parsing | 0.073911 |
| linting | 0.013826 |
| attribute application | 0.000139 |

### baseline_timeout_error: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Mathlib.Tactic.intervalCases | 13692.704229 |
| tactic execution / Lean.Parser.Tactic.simpAll | 6998.012502 |
| tactic execution / Lean.Parser.Tactic.refine | 897.887089 |
| tactic execution / Lean.Parser.Tactic.eqRefl | 897.015727 |
| tactic execution / Lean.Parser.Tactic.simp | 597.980174 |
| outside active tactic boundary | 365.998969 |
| tactic execution / Lean.Parser.Tactic.simpa | 299.020578 |
| tactic execution / linarith | 286.582332 |
| tactic execution / Mathlib.Tactic.normNum | 223.914499 |
| tactic execution / Lean.Parser.Tactic.apply | 204.008630 |
| tactic execution / Lean.Parser.Tactic.omega | 171.998894 |
| tactic execution / Lean.Parser.Tactic.allGoals | 112.992708 |
| tactic execution / Lean.Parser.Tactic.tacticSeq1Indented | 23.001843 |
| tactic execution / Lean.Parser.Tactic.tacticSeq | 10.000621 |
| tactic execution / Mathlib.Tactic.Ring.ring1 | 7.995221 |
| tactic execution / nlinarith | 6.001381 |
| tactic execution / Lean.Parser.Tactic.withAnnotateState | 6.000665 |
| tactic execution / Lean.Parser.Tactic.skip | 3.000417 |
| tactic execution / Mathlib.Tactic.RingNF.ringNF | 2.000553 |
| tactic execution / Lean.Parser.Tactic.rcases | 2.000315 |

## baseline_lean_error: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| simp | 2151.173835 |
| tactic execution | 2060.065679 |
| typeclass inference | 794.224425 |
| norm_num | 146.655381 |
| import | 133.980915 |
| elaboration | 98.769957 |
| type checking | 57.151887 |
| ring | 7.841461 |
| parsing | 0.389005 |
| aesop | 0.355656 |
| linting | 0.115204 |
| attribute application | 0.001294 |

### baseline_lean_error: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Lean.Parser.Tactic.simpAll | 2466.245399 |
| tactic execution / nlinarith | 1064.083660 |
| tactic execution / Mathlib.Tactic.intervalCases | 405.017643 |
| tactic execution / Mathlib.Tactic.normNum | 349.003022 |
| outside active tactic boundary | 253.902032 |
| tactic execution / Lean.Parser.Tactic.refine | 131.016435 |
| tactic execution / linarith | 90.016618 |
| tactic execution / Lean.Parser.Tactic.simp | 88.012837 |
| tactic execution / Lean.Parser.Tactic.omega | 44.988837 |
| tactic execution / Mathlib.Tactic.FieldSimp.fieldSimp | 41.005172 |
| tactic execution / Mathlib.Tactic.RingNF.ringNF | 33.003033 |
| tactic execution / Lean.Parser.Tactic.allGoals | 28.000888 |
| tactic execution / Mathlib.Tactic.Ring.ring1 | 16.001449 |
| tactic execution / Aesop.Frontend.Parser.aesopTactic | 15.003184 |
| tactic execution / Lean.Parser.Tactic.eqRefl | 11.001752 |
| tactic execution / Lean.Parser.Tactic.decide | 11.000796 |
| tactic execution / Lean.Parser.Tactic.tacticSeq | 8.997301 |
| tactic execution / Lean.Parser.Tactic.tacticSeq1Indented | 4.000153 |
| tactic execution / Lean.Parser.Tactic.simpa | 3.000440 |
| tactic execution / Lean.Parser.Tactic.withAnnotateState | 3.000241 |

## baseline_resource_failure: actual component CPU

| Stock profiler category | Observed exclusive thread CPU (s) |
|---|---:|
| tactic execution | 2944.934673 |
| elaboration | 760.930805 |
| type checking | 96.638444 |
| import | 74.803591 |
| simp | 13.200746 |
| typeclass inference | 4.863352 |
| norm_num | 0.464613 |
| parsing | 0.037195 |
| linting | 0.009275 |
| attribute application | 0.000069 |

### baseline_resource_failure: sampled active tactic attribution

| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |
|---|---:|
| tactic execution / Lean.Parser.Tactic.eqRefl | 2769.189048 |
| outside active tactic boundary | 856.066463 |
| tactic execution / Lean.Parser.Tactic.omega | 156.986779 |
| tactic execution / Mathlib.Tactic.normNum | 9.000151 |

## Scope and remaining decisions

Original-status changes: 0; all changed IDs remain in result.json.
Diagnostic capacity/clock flags: {"clock_errors": 0, "dropped_keys": 0, "frame_overflows": 0, "sampler_error": 0, "truncated_keys": 0}.
Sampling transition/gap counts: {"source_transition_intervals": 457}.
Per-source.csv lists every selected attempt, original/profile outcome, observed cost, missing clock and top measured boundary.
Per-source.json retains full named component and sampled tactic data; result.json retains open frames and stream completeness.
Named tactic boundaries do not automatically expose nlinarith preprocessing, product generation, LP and certificate subphases.
Any unmeasured internal subdivision remains unknown; do not borrow fractions from another corpus/version/run.
Select the next own-method experiment from this completed distribution only after raw-result review.
A small preflight may validate the analysis path but cannot select a whole-cohort dominant tactic.
