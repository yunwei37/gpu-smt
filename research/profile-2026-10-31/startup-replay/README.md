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

## Execution notes
First attempt exposed LEAN_PATH package-root shadowing: the 26-artifact directory
cannot precede an incomplete OAI dependency root. All failed rows and three
Mathlib controls remain in the original PVC directory and are excluded from
main timing statistics. The corrected v2 uses an OAI symlink union of retained
dependency artifacts, overridden only by the exact 26 A-batch compiler artifacts.
A real NearPinDeletion source preflight returned zero and emitted all outputs.
A pidfd readiness wait avoids rounding 1-second workloads to 100ms sample ticks.
Raw root: /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/v2 .
Existing perf 6.12.113 and its retained .deb are reused; no host package/sysctl change.

## Reproduction
The runner sets process affinity with sched_setaffinity(0, {0,...,7}) and takes
an exclusive POSIX flock on the shared pcore.lock before launching any timed
child (equivalent to the requested taskset/flock boundary). No waiting time is
included in per-child wall clocks. Child exit is detected with pidfd; sampled
RSS/PSS are separate from wait4 maximum RSS. Columns at_sampled_rss_peak_* use
one simultaneous sample; independently sampled field maxima must not be added.
Private_Clean file-backed mappings may be shareable even when Shared_Clean is
small in a single-process run. Full smaps_rollup samples retain Pss_File/Anon.
Run phases with python3 measure.py startup, replay, perf; each takes the same
lock. analyze.py RAW OUTPUT_DIRECTORY emits the small CSVs. The retained .deb
for perf is under sibling systime/linux-perf_6.12.113-1_amd64.deb. The toolchain
and dependency roots are explicit in measure.py and raw environment.txt.

## Finite exit-driven continuation
The actual serial sequence is startup -> replay -> four user-space import perf
runs -> thirteen no-declaration checker controls and one user+kernel Mathlib
profile -> min/median/max observer calibration -> result collection.
Every timed phase takes the existing shared P-core lock; other lines can acquire
it between phases. Exit waits use pidfds rather than per-minute polling.
There is no timer, new agent or persistent scheduler. The small finalize.py
reduces actual records, retains non-successes and instrumentation caveats, and
commits only this directory's generated CSV/report paths after the chain exits.
It first attempts pull --rebase --no-autostash; if the shared checkout is dirty,
it never stashes others' work and pushes only when origin/main is already an
ancestor. A divergent fetch stops publication. Finalization stdout and the
published commit receipt stay under raw v2/finalize.log and published-result.txt.
Absence of that receipt is not experiment completion.
