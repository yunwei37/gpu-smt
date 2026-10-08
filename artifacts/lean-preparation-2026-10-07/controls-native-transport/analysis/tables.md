# Raw Lean preparation capture analysis

These are whole-call/corpus observations; no kernel-stage timing or equivalence claim.

| Run | Inputs | Terminal complete | Makespan (s) | Integrity issues |
|---|---:|---|---:|---:|
| fresh | 4 | True | 8.519543552 | 0 |
| warm | 4 | True | 4.699767063 | 0 |

| Response comparison | Count |
|---|---:|
| equal | 4 |

| Run | Outcome | Records | Invocation p50 (ms) | Invocation p95 (ms) |
|---|---|---:|---:|---:|
| fresh | incomplete | 2 | 2110.7159165 | 2122.39721675 |
| fresh | rejected | 2 | 2089.300302 | 2131.4280285 |
| warm | incomplete | 2 | 20.821769 | 29.102651899999998 |
| warm | rejected | 2 | 19.0335125 | 26.512875649999998 |

Per-input source/native JSON and differences: `per_input.jsonl`. Full timing strata, system outcomes, provenance and reconciliation issues: `summary.json`.

Primary scope is run→shutdown makespan, including setup and capture overhead. Invocation distributions include all retained outcomes; missing durations remain missing. Warm fallbacks create fresh native environments within a warm process.
