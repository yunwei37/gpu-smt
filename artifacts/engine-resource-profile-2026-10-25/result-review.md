# Existing native-worker CPU demand — root self-review

Read-only15-second observation of the healthy original full7808capture.
30 noninitial per-REPL intervals; median 0.999153
CPU cores, maximum 1.009294, one observed OS thread per REPL.
The~1.01 maximum reflects one-second/jiffy accounting, not two active threads.
All eligible CPUs are8–11. No native work was started/restarted or reconfigured.

This supports initially assigning one core per worker, at most four workers
on the next four-core point, subject to actual48GiB aggregate admission.
This is workload-local demand observation, not proof that every Lean version,
code-verification tactic or backend needs one core. Re-measure those workloads.
Legacy full7808retains two workers/24GiB AS; next-group memory/throughput and
accepted sets must be reported separately. No throughput result follows.

Rust build/test activity overlaps part of the historical capture; build
interval receipts are retained. Shared-host/CPU contention prevents treating
that pair as a pristine isolated performance experiment.
