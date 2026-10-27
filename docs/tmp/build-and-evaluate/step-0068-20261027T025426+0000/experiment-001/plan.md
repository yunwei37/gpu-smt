# Plan — unchanged original lean-mlir bitvector workload

RQ4 asks when heterogeneous execution improves complete verification after
preparation reuse. This supporting characterization measures whether a real
code-verification module spends a substantial amount in SAT/LRAT. Parent
step0063 prepared the exact source and execution plan; step0067 has now
ingested the preceding interval48 group. All prior groups are terminal.

Execute the existing leanmlir-engine-input/execute.py unchanged: original
b8c4a771 module, project and nightly2025-12-01 SDK. Three sequential cells:
original file, exact stdin, original file plus native trace profiler. Keep
the root's --tstack=400000 and all source bytes/options; no theorem splitting,
admission removal, heartbeat/solver/trust change or dependency update.

One exclusive4core lease on CPUs8–11,48GiB aggregate actual RSS,noAScap,
existing1s watchdog. Keep the existing300s engine timeout; this is not a
published workload deadline. File/stdin must be compared before treating
their outcomes as equivalent. A timeout/resource failure is censored, not
zero SAT/LRAT cost.89 source mentions do not imply89 executed calls.

The original-file cell is the real preflight; run the full declared matrix
without substituting smaller proofs or silently changing flags. Retain raw
exits,JSON,stderr,native profiler data if returned,queue/cleanup/resource
history and whole controller/build/archival clocks. Missing trace remains
unknown. A fresh Rust CLI is built only after prior native owners retire.
Closed streams reuse existing lossless archival,not a new observer.

Positive/negative data identify or bound actual expensive components; a
censored outcome leaves body attribution open. This setup does not itself
prove performance, novelty or complete RQ4. Root self-review only.
