# Mechanism feasibility measurements — M branch

Owner: this M chat; all review is self-review. Only this directory is modified.
Shared original Workspace/check-out,main; now phobos-vt with local PVC.
M uses at most16GiB and8cores within the four-line40GiB allocation. One M
Lean process at a time; bounded native cells under30minutes. External child
signals remain denied; no security or host PMU setting changed. Raw captures
and generated binaries live outside Git on the existing PVC:
/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/.
No main-engine change or inferred speedup. Historical G10 points stay separate.

## Current evidence

- [Profiler perturbation](profiler-heartbeat-methodology.md):400 diagnostic
  returns; trace.profiler changes7 error flags. Its lower runtime is not speedup.
- [C timing qualification](step-007-report.md):fresh small controls match
  stock flags,diagnostics,InfoTrees and heartbeats on short controls.
  [Full200 result](native-cohort-result.md):600 returns with observed flag/
  diagnostic/InfoTree parity;rawHB differs,production DAG remains unknown.
- [Genuine timeout prefix](genuine-timeout-prefix-result.md):30returns with
  exact differential parity;separate from clipped-pass prefix and full timeout.
- [Software residence](software-profile-result.md):native sampling actually
  checked;observer IR separated,successful kernel4258sample pure-timing profile retained.
- [Original-budget pass cohort](accepted-original-result.md):150returns,
  all50no-errors;4/8core local latency models1.276/1.340x,not engine speedup.
  This prevents applying the clipped diagnostic ceiling to original inputs.
- [Local dependency model](step-009-report.md):independent/coupled controls
  separated; complete DAG and merge semantics still unknown.
- [Ordinary-kernel certificate](step-003-report.md):digits answer100 passes;
  [grid samples](step-004-report.md) are partial; the new
  [reflected grid](step-019-report.md) proves the complete grid by a row-division
  certificate. It does not execute4million Boolean reductions inside the kernel.
- [Memory/core conclusions](memory-budget-conclusion.md):four budgets;full
  result coverage changes retry-model costs; no calibrated COW speedup claim.
- [Hot tactics](hot-tactics.md) and [prior work](prior-work.md):actual loader
  context matters; reflection/futures/compilation are established techniques.

Native guard/sampler scope:[exact resource semantics](native-resource-semantics.md).

Execution-budget correction:[whole matrix overrun and forward fix](collection-budget-erratum.md).
The former six-cell collection exceeded30minutes overall; per-cell bounds
did not make it compliant. Current native points have completed and retired.

## Questions and measurement sequence

1. Hardware counters and actual native-module loading: read-only PMU probe and
module census, then short naturally exiting controls. If counters are denied,
IPC/LLC/dTLB/cycle fractions stay unavailable; do not replace them with wall time.
2. Approximately200 stratified candidates: recover existing profiler/InfoTree
evidence first; preserve incomplete goal/dependency traces and distinguish
structural opportunities from an executable dependency DAG and parallel speedup.
3. Kernel-checked arithmetic extraction: structural decimal digits, an actual
equivalence theorem and decide checks; no native_decide/trust bypass. Report
compile/kernel costs and RSS separately. Earlier4000000-cell linear projections stay estimates. The new complete
row-certificate theorem uses an algorithmically compressed checker, not that
projected dense computation.
4. Per-core2/4/8/12GiB memory simulations reuse recorded candidate attempts and
memory observations; missing latent peak/threshold response is censored, never
an invented outcome. Compare fixed pool, destructive OOM and shared admission.
5. Primary-source prior-work audit includes STM/PIDE/futures, Prolog/TLS,
Lean.Elab.Parallel/LeanTree, reflection/vm_compute/decide, lean-egg,
LeanGraphSearch and SHRED. Naming/repackaging alone is not novelty.

Heavy whole-project precompilation is not started. The module census cannot
replace a profile-weighted native-code opportunity estimate; PMU remains denied.

## phobos-vt continuation

Migration approval preserves the Workspace/PVC. M uses at most 8 cores and 16 GiB within the four-line 40 GiB total. External child signals still fail with EACCES. See step-003-report.md for the full-import deadline failure; do not duplicate that live Lean process. Native-qualified software sampling points are now complete;see the current evidence above. See prior-work.md for the claim map.

Step 003 completion: the maps process has retired; final digits certificate passes stock-kernel checking. See native/phobos-digits-certificate-v4 and hot-tactics.md. The previous whole-import run remains noncompliant with the 30-minute limit. Current finite runner loads a self-wall-exit library before imports; no signal-based watchdog is claimed.

## Computation extraction extension

[Individual coverage review](coverage/README.md): all126miniF2F operational failures
and17returned EPFL budget observations reviewed. Two checked target families
cover49source opportunities. [Whole-source pair](step-023-report.md) now recovers31/49 complete proofs (16digits/15grid),14retain tactic errors and4remain budget-limited.
The31 accepted sources solve two previously unsolved tasks in the retained historical corpus.
This changes operational acceptance; it is not a result-preserving engine-speedup claim.
[Automatic dispatch](automation/README.md) completes both64-source task frames, with unchanged31 passes and rejected adversarial targets/prefixes. False auxiliary assertions are separate proof-repair cases.
See [step020](step-020-report.md) and the original-source obligation table.

[Full reflected grid](ReflectedGridCertificate.lean) checks row-completeness and
proves the original mathd_numbertheory_541 theorem. Independent chunk kernel
recheck timings and total pipeline cost are separate measurements; see step021.

[openai/math seven-type check](openai-kernel-sample/README.md): both original and certificate plain sources7/7 accepted; the split-row certificate is slower (13.318s vs23.937s summed whole-source wall;2.328s vs5.758s additional kernel work).
This is a negative generalization result for the tested Int/list family, not a global1.35m-call estimate. Raw heartbeat unit mistakes and the later60s typed-census censoring are retained separately.
[Remaining37 bridge effort](coverage/remaining37-bridge-estimate.md) is an estimate, not completed proof coverage.

[Third checked bridge and full32-source pair](power-family-result/README.md):
128point cube/fourth checker with proved sharp bounds;2whole-source repairs,
1/8selected historical timeout recovered. Latest corpus acceptance overlay145/244
tasks (59.4262%),33new accepted candidates total. Shape coverage57/126must not be
confused with actual32/126source recovery.
