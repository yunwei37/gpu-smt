# Raw Lean preparation capture analysis

These are whole-call/corpus observations; no kernel-stage timing or equivalence claim.

| Run | Inputs | Terminal complete | Makespan (s) | Integrity issues |
|---|---:|---|---:|---:|
| fresh | 4 | True | 5.513557022 | 0 |
| warm | 4 | True | 7.498355922 | 0 |

| Response comparison | Count |
|---|---:|
| equal | 4 |

| Run | Outcome | Records | Invocation p50 (ms) | Invocation p95 (ms) |
|---|---|---:|---:|---:|
| fresh | incomplete | 1 | 2405.169716 | 2405.169716 |
| fresh | rejected | 3 | 308.260913 | 2171.5115926999997 |
| warm | incomplete | 1 | 2097.62667 | 2097.62667 |
| warm | rejected | 3 | 495.098824 | 4160.8867333 |

Per-input source/native JSON and differences: `per_input.jsonl`. Full timing strata, system outcomes, provenance and reconciliation issues: `summary.json`.

Primary scope is run→shutdown makespan, including setup and capture overhead. Invocation distributions include all retained outcomes; missing durations remain missing. Warm fallbacks create fresh native environments within a warm process.
