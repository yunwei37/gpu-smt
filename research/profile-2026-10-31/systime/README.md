# M: attribution of OS time in native Lean compilation

[Experiment plan](plan.md). Actual source inputs, raw counters, stack data,
syscall summaries, artifacts and memory records stay on the existing PVC:
 /workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime/

Current preflight is qualified; **no completed original-module measurement yet**.
UMoments9 baseline triplet is queued on the shared P-core lock; process identity
in preflight.json is a point-in-time observation, not a perpetual running claim.
No historical W timing is pooled with privileged/new-cgroup/perf measurements.

Installed perf6.12.113 and retained its .deb. Hardware user/kernel counters,
syscall trace and self-child signals actually work. Native cgroup control passed:
only the owned child moved into a temporary15GiB group under this same Workspace
Pod; parent limits/other pods untouched, group removed after natural return.
All timed controls use taskset0–7 and shared pcore.lock; preparation uses8–23.

Two invalid setup points remain outside the valid run directory: one wrong
affinity helper run, deliberately stopped; three imports failed under a15GiB
address-space limit. None completes the module or counts as a repetition.
The current runner asserts P affinity and uses a temporary cgroup, no fixed AS.

Source/SDK evidence changes the attribution hypotheses: this SDK uses **mimalloc**
for Lean objects, so GLIBC_TUNABLES need not affect the dominant allocator.
The stock memory-limit check calls getrusage at a default source threshold200
checks and falls back to /proc/self/statm near/above the peak threshold.
Actual SDK disassembly confirms compare0xc8 and a direct getrusage@plt call.
These are hypotheses to test with native stacks/syscalls and single-variable
experiments, not proofs of the observed kernel-time cause.

Primary source (pinned SDK tag):
- https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/memory.cpp
- https://github.com/leanprover/lean4/blob/v4.34.1/src/include/lean/lean.h
- https://github.com/leanprover/lean4/blob/v4.34.1/src/runtime/object.cpp

run.py records native wait4 user/system/wall/RSS separately from observer cost.
analyze.py produces per-run/median/range tables; analyze_stacks.py attributes
period-weighted on-CPU samples only, preserving unmatched frames. Stack parsing
still requires actual first-capture qualification. Missing work is pending,
not a negative result. No system-time attribution or acceleration claimed yet.
All review is 自审; root owns characterization-paper integration.
