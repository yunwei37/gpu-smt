# Mechanism feasibility measurements — M branch

Owner: this M chat; all review is self-review. Only this directory is modified.
Shared original Workspace/check-out on G10, main. No additional agent, no
placement/security/CronJob changes. Per user: M at most5GiB, one Lean process,
finite heartbeat-bounded runs under30minutes; aggregate four-branch budget12GiB.
Outputs remain on the existingPVC. No main-engine change or inferred speedup.

## Questions and measurement sequence

1. Hardware counters and actual native-module loading: read-only PMU probe and
module census, then short naturally exiting controls. If counters are denied,
IPC/LLC/dTLB/cycle fractions stay unavailable; do not replace them with wall time.
2. Approximately200 stratified candidates: recover existing profiler/InfoTree
evidence first; preserve incomplete goal/dependency traces and distinguish
structural opportunities from an executable dependency DAG and parallel speedup.
3. Kernel-checked arithmetic extraction: structural decimal digits, an actual
equivalence theorem and decide checks; no native_decide/trust bypass. Report
compile/kernel costs and RSS separately. 4000000-grid estimates stay estimates.
4. Per-core2/4/8/12GiB memory simulations reuse recorded candidate attempts and
memory observations; missing latent peak/threshold response is censored, never
an invented outcome. Compare fixed pool, destructive OOM and shared admission.
5. Primary-source prior-work audit includes STM/PIDE/futures, Prolog/TLS,
Lean.Elab.Parallel/LeanTree, reflection/vm_compute/decide, lean-egg,
LeanGraphSearch and SHRED. Naming/repackaging alone is not novelty.

Heavy whole-project precompilation is not started: it requires module count,
disk/CPU/memory estimates and the user's later machine-placement decision.

## phobos-vt continuation

Migration approval preserves the Workspace/PVC. M uses at most 8 cores and 16 GiB within the four-line 40 GiB total. External child signals still fail with EACCES. See step-003-report.md for the full-import deadline failure; do not duplicate that live Lean process. Software CPU sampling control is qualified, Lean sampling is not. See prior-work.md for the claim map.

Step 003 completion: the maps process has retired; final digits certificate passes stock-kernel checking. See native/phobos-digits-certificate-v4 and hot-tactics.md. The previous whole-import run remains noncompliant with the 30-minute limit. Current finite runner loads a self-wall-exit library before imports; no signal-based watchdog is claimed.
