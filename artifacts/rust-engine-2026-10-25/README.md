# Rust engine implementation qualification — root self-review

Reusable source: crates/. Exact validation commands, exits and compressed logs
are in validation-20261025T084048/.20unit/integration/process/HTTP tests pass;
the native differential test is explicitly ignored locally while the existing
full research capture owns the slot. Pinned official Lean4.18/REPL CI passes
the accepted/rejected/sorry raw-JSON differential on exact head f016161.
Updated hardware/telemetry code receives a fresh exact-head CI below.

Actual low-threshold process RSS triggers watchdog preemption and exclusive
retry; native fixture outcomes distinguish acceptance/rejection/admission,
timeout and stderr draining. These are protocol/process fixtures, not Lean
proofs or whole-workload speedup measurements.1024queued-job checks ensure
process sampling does not multiply by queue length. Cancellation tests retain
RL duplicate subscribers and charge final-subscriber backend retirement.

Cargo fmt, Clippy with warnings denied, all-target tests, rustdoc with warnings
denied and executable/help pass. Earlier compiler/lint/format failures/logs
remain retained. The lookup microbenchmark is explicitly a data-structure
control, not native/service performance. Real native full-population parity,
42large-memory reruns and new-resource throughput remain pending.
