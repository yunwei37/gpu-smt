# Import startup and kernel replay characterization
## Plan and self-review
Requested 2026-10-31 O-line characterization experiment. Test whether fixed
imports dominate short native modules and whether kernel-only replay is cheaper
than construction. This supports the characterization paper; no acceleration
mechanism or novelty is claimed. Positive, negative and censored results are retained.
Source cohort: all 26 successful standard-artifacts-a modules plus Grid and
Amplitudes. Startup cohort: the 13 A modules whose historical standard build
wall time was under 5 seconds; repeat original builds and direct-import-only
controls three times, plus three import-Mathlib controls. Full artifacts
(olean/ilean/C) remain enabled. Historical durations select the cohort only.
Replay uses the exact bundled Lean 4.34.1 leanchecker, default import-relative
mode, not --fresh. Imports are trusted; unsafe/partial constants are skipped by
upstream replay. CLI total includes startup, path discovery, imports, replay
and cleanup; do not call it pure kernel CPU time. Historical build/replay ratios
are labelled historical, not causal matched ratios. A new build comparison for
the 13 short modules is paired on this hardware/protocol.
All measured work uses taskset 0-7 and the shared pcore.lock, one job at a time.
Preparation runs on 8-15. O budget: 12 GiB observed tree RSS; Lean -M9216 when
supported; bounded process-group timeout and memory sampling. smaps sampling
100ms is instrumentation and can miss peaks. No page-cache drop or host changes;
these are warm OS-cache sequential repetitions. Raw stdout, exact commands,
resource samples and perf.data live on PVC outside Git. Perf-record runs are
separate from unprofiled timing runs. Self-review only, no independent review.
Upstream: https://github.com/leanprover/lean4/blob/v4.34.1/src/LeanChecker.lean
and https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Replay.lean .
