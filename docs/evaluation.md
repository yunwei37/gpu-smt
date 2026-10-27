# Evaluation: current evidence and open work

Updated2026-10-27UTC. Root thread alone;all reviews are self-review,not independent
audits. Four [original RQs](idea-story.md) and the Lean/SMT/OSDI objective remain
open. Engineering tests,activity and a compiled paper do not establish novelty
or venue acceptance. All original,negative,failed and partial data remain.

## Current directions

Prioritize the independent [Rust engine](architecture.md),then reliable failure
determination,same-task scheduling and public Lean code verification.
Resource preparation,ordinary COW/cache and first-success cancellation alone
are prior techniques;novelty needs evidence in the load-aware methods.
No CPU-oracle optimization/extension/new run,competitor reproduction,AI
delegation,new research stopping threshold,deadline or conditional closure.
See the exact [user instructions](user-instruction.md).

<a id="current-resource-point"></a>

## Resource point

One collection at a time. Own trees:48GiB aggregate actual sampledRSS,CPU8–11,
dynamic admission/up to4one-core workers,or one4core compiler lease;no fixed
per-process AS limit. The1s watchdog preempts/reaps the largest own native
attempt and queues an exclusive retry;solo excess remains a resource failure.
Sampling overshoots;it is not a hard quota. No otherWorkspace/quota change.
Historical2worker/24GiB-AS clocks retain their own point and are never pooled.

## Complete native/Mathlib-derived pair

[Full7808result](../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/result-review.md)
at frozen1f38be7retains canonical sources/order,all/reusefalse/300s.
Both cells:3013accepted/4665rejected/87timeout/41resource-exhausted/2backend-error,
exact same status/accepted IDs,142solvedtasks. Prepared omits empty ast:[]
in7660responses;other response fields match,86operational error strings differ.
Full raw artifact compatibility and universal isolation are not established.

Whole-cell28391.984735/22891.507755s=1.240284609x,19.373344%less elapsed,
including decoding/retirement/serialization/compression.14parent preparations
of5545modules,13evictions,62fallback event rows are charged. Single native-first
shared-host comparison with CPU11 support contention is descriptive component
evidence,not causal replication,strongest warm-service superiority or novelty.
Full-monitor sampled peaks48.774902/48.927013GiB overshoot48GiB. All15736recorded
births/controller retired. Two EOF/deep-simplex faults have unknown exact cause.

[Earlier dynamic pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z/README.md)
stays native-complete/prepared-ENOSPC-partial,without pair ratio. Its native
statuses match the new native,but historical accepted3086becomes timeout
relative to an older point. New pair equality does not erase that regression.
[Historical42solo reruns](../artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z/README.md)
give41budget failures/1timeout,no checked accepts/rejects,48.23GiB sampled peak.

## Own load-aware methods

[TaskMemory](tmp/build-and-evaluate/step-0071-20261027T035144+0000/step-report.md)
learns earlier physical sibling peaks by backend/resource/task/timeout context,
refreshing queued reservations without sharing verdicts. Native differential
CI and CLI/process controls pass. Lower-bound peaks can underestimate and
heterogeneous siblings can overreserve. Default FIFO remains unchanged.
[Real32development cohort](../artifacts/engine-resource-profile-2026-10-25/task-memory-preflight-20261027/README.md)
preserves16prioraccepted/7rejected/9resource-failed sources in original order.
Selection is outcome-informed,not final representative evidence. No throughput
benefit yet;the earlier release build was guard-killed and is not qualified.

[Whole-task lexical memory fit](../artifacts/engine-resource-profile-2026-10-25/source-memory-crossfit-20261027/README.md)
is negative:MAE0.606624GiB versus median0.352486;all41resource/44preempted sources
underestimated>2x. No fit deployment.
[Exact duplicate analysis](../artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md)
finds only18literalNone errors duplicated,no substantive repeated proof.

## Failure and scheduling

[480failure profile](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md):
83timeout/355error/42resource failures,unchanged labels. interval_cases55.19%
and simp_all28.21% are observed timeout-thread CPU shares,not corpus wall shares.
[Original23simp phases](../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/README.md):
20timeouts/3observer recursion faults;eight outer/six inner loops among14short
cases,nine long calls. No reliable cycle/failure witness or transparent observer.
[Original48interval mapping](../artifacts/hotspot-mechanisms-2026-10-25/interval48-import-repair-20261026T162128Z/README.md):
both48source variants timeout,0/48reliable failure coverage;11control pairs match.
Different preemptions/support load do not establish causal speedup.
Closed-tail stays frozen0/71;source spelling/branch count is not certain failure.

[Complete scheduling matrix](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
at old2worker/24GiB-AS:21746.81s all,15385.39s first-original,15112.12s
first-short(1.41347x/1.43903x),same142solvedtask IDs. Checked sibling wins permit
cancellation in pass@k;this does not supply every-candidate RL rewards.
Single-order difference is not causal replication or scheduling novelty.
Task-held-out lexical ranking was negative,not deployed;fixed-cost models are
not wall-clock bounds.

## Public Lean code verification

[Original Verina189](../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md):
46no-explicit-admission native exits,139admitted stubs,fourAPI errors;diagnostic
labels match. No above-threshold SAT/LRAT in completed subgroup;absence is notzero.
[Original lean-mlir module](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md):
file/stdin/profile40.466071/40.210064/94.042837s,equal successes,3.518GiB peak.
89BV stack contexts across42trace threads are not CPU utilization.
LRAT538.138403elapsed-slice seconds/38.814693s union overlap;not Amdahl inputs
or fractions transferable onto40s native wall. One module,not the fullproject.

[Closed-CNF original-module comparison](../artifacts/lean-code-verification-2026-10-25/shared-cnf-original-20261027T192501Z/result-review.md)
now completes native/import-only/core/public at40.146047/40.338398/57.984536/
56.912237s. All accepted with equal native responses,one attempt,no preemption,
and recorded retirement;core44.43%slower/public41.76%slower in this one ordered
observation.89active tactic-token edits preserve commented mentions and config;
inverse edits recover originalbytes. Small proof/preflight success did not
predict whole-time benefit. Single generated CNF does not prove physical reuse;
internal slowdown attribution is unmeasured. Keep opt-in research prototype,
not default enablement,GPU gain or novelty. Fourdirections continue.

## Frozen evidence and full history

[Corrected GPU counterexample pair](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md)
matches7808statuses/3014accepted,but is8.856321%slower.34exact refutations in
29ordinary-error candidates remove no timeout. Old25source/0.2%bounds arose
from invalid wrapper data,not final coverage. No screening-pair expansion.
[Frozen Goedel CPU oracle](../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full-result-review.md):
threepairs1.106271x aggregate,with2reject-to-complete changes.
[Selected1000CPU/GPU](../artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/full-result-review.md):
no useful extra GPU gain,cold GPU3.7044%longer than CPU. Exact fallback,not
floatingLP,is large in its own helper-clock profile;overlapping totals are not
a strict GPU ceiling. SHRED/ProofNet controls,E038,defeq/metadata/declaration/
SMT-prefix results remain frozen and linked in history.

[Full prior476line evaluation](tmp/build-and-evaluate/step-0080-20261027T192409+0000/evaluation-history-through-606a4b5.md.gz)
is preserved byte-for-byte;its links were authored from docs/evaluation.md.
[Readable pinned parent](https://github.com/yunwei37/gpu-smt/blob/606a4b5/docs/evaluation.md)
keeps that location and links earlier archives. Current [paper](paper/main.tex)
remains an incomplete35page research draft;all fourRQ evidence/novelty coverage
and independent audit remain open.
