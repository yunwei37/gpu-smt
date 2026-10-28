# Evaluation: current evidence and open work

Updated2026-10-28UTC. Root only;reviews are self-review,not independent audits.
The [original four RQs](idea-story.md),Lean/SMT scope and OSDI objective remain
open. Tests,a compiled draft and selected timings do not establish novelty.
All raw,failed,partial and superseded evidence remains;detailed history is below.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>

## Current directions

The sole new acquisition is the matched four-warm Kimina versus repaired-engine
full7808 resource pair. Repair/measure resource performance before stacking
task-memory,ranking,failure or LRAT gains. The four continuing directions remain:
the layered Rust engine,reliable early failure,multi-candidate inference and
public Lean code verification. There is no project deadline or closure rule.
Resource/COW/cache/ordinary compilation/cancellation primitives are prior work;
prospective novelty needs workload-level evidence. CPU oracle stays frozen.
No other competitor reproduction,AI delegation,new Workspace or checkout.
Exact authority remains [the user log](user-instruction.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:the corrected full warm-resource pair is running;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="current-resource-point"></a>
<a id="resource-point-and-workloads"></a>

## Resource point

One native collection at a time:48GiB summed own sampled RSS,CPUs8–11,up to
four one-core workers,dynamic admission,no fixed process AS cap. A1s watchdog
preempts/reaps the largest own attempt;retry follows the queued ordinary
frontier and runs alone. Later arrivals cannot starve it;solo excess remains
resource failure. Sampling overshoots and is not a kernel quota. No other
Workspace/quota/permission change. Historical2worker/24GiB-AS points stay separate.

## Complete native/Mathlib-derived pair

[Own fresh/prepared7808 pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/result-review.md)
has equal3013accepted/4665rejected/87timeout/41resource/2backend statuses.
Whole28391.98/22891.51s=1.24028x is an own-component comparison,not strongest
warm-service benefit or novelty. Empty ast differs in7660prepared replies;
86operational strings differ. Fourteen preparations/62fallback rows are charged;
sampled peaks48.77/48.93GiB overshoot. Both engine cells omitted the ordinary
native Mathlib library that historical warm loaded,an additional code-context
confound. Two EOF/deep-simplex faults have unknown exact cause.
[Earlier ENOSPC pair](../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z/README.md)
retains prepared partial data. Historical accepted3086became timeout;new
own-pair equality does not erase that change.

## Resource-layer diagnosis and missing warm comparison

Historical warm21693.76s is2worker/24GiB-AS/HTTP versus new4worker/no-AS/retry
points;the six status differences and native-library confound forbid a matched
claim. [Old FIFO closure](../artifacts/engine-resource-profile-2026-10-25/policy7808-20261028T034248Z/README.md)
returns all7808with the earlier prepared raw outcomes. Its22716.04s internal
clock has no complete external counterpart after the old controller pause.

[Disjoint singleton analysis](tmp/build-and-evaluate/step-0088-20261028T053756+0000/experiment-001/result-review.md):
10375.98s has one child(45.33%of its own cell);8924.78s/86.01%is actual exclusive
retry,1232.45s/11.88%retry-pending proxy,and218.33s/2.10%final timeout tail.
Occupancy is not CPU/removable time. Failure/timeout lifecycle unions overlap;
42of62fallback rows are the same exclusive checks,not extra additive work.
[Growth analysis](tmp/build-and-evaluate/step-0096-20261028T103651+0000/experiment-001/result-review.md)
finds41solo peaks>47.5GiB lower bounds;4658/7389exclusive samples have16GiB
headroom. These are not time shares,future memory caps or safe-backfill proof.

Retired-PID history scanning and stale queued global forecasts are repaired.
[Retry-frontier source/controls](tmp/build-and-evaluate/step-0094-20261028T102232+0000/step-report.md)
remove the mid-frontier drain barrier;no speculative backfill is enabled.
[First corrected24pair](../artifacts/engine-resource-profile-2026-10-25/warm-resource-qualification-20261028T044624Z/README.md)
loads the same ordinary native Mathlib library on both sides. Warm1430.68s
returns14accepted/7error/1timeout/2resource;oldengine1540.71s returns14/5/3/2.
[Frontier24](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-resource-retry-frontier24-20261028T110236Z/README.md)
takes1347.58s with unchanged engine outcomes.
[Reply-retirement24](../artifacts/engine-resource-profile-2026-10-25/gpu-smt-resource-timely-reply24-20261028T115820Z/README.md)
takes1349.55s(5.67%less than retained warm);14accepted IDs agree,but2507/7230
still time out only in engine. It changes no raw frontier outcome. The protocol
repair is real but did not explain those differences;selection/order/shared
host prevent a full gain claim. All registered native births retire.

[Full7808 plan and actual start](tmp/build-and-evaluate/step-0102-20261028T122519+0000/step-report.md):
one finite serial warm→engine pair started12:25:19UTC,source13d4606.
Four warm workers actually mapped the matched library. No full terminal or
speedup is claimed;inspect actual PID/birth and terminal before continuation.
Later [exact-median maintenance](tmp/build-and-evaluate/step-0103-20261028T123153+0000/step-report.md)
preserves forecasts with no repeated sort;66workspace+5native CI controls pass.
Later [IO deadline correction](tmp/build-and-evaluate/step-0104-20261028T124447+0000/step-report.md)
has a deterministic old-selection overrun control and68workspace+5native CI.
Neither change replaces frozen13d4606 or has a measured whole-flow benefit.

[Historical42solo](../artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z/README.md)
is41budget failures/1timeout,no accepted,and48.23GiB sampled peak;it lacked
explicit matched native-library selection. The corrected fixed42 cohort is
prepared/rebound to13d4606 and remains unstarted until the current pair retires
and is reviewed. Do not report old41/1as a new run.

## Own load-aware methods

[TaskMemory32](../artifacts/engine-resource-profile-2026-10-25/task-memory32-20261027T193536Z/README.md):
2832.46/2169.74s,23.40%less elapsed,exact16accepted/7rejected/9resource outcomes;
attempts41→37,retries9→5. Tail/outcome-informed selection,single order/sharedhost,
CPU11support and sampled overshoot prevent population/novelty claims.
The prepared full policy queue ran only its FIFO cell;three policy cells remain
deferred. Predictions never reject;lower-bound sibling peaks can misreserve.
[Held-out memory fit](../artifacts/engine-resource-profile-2026-10-25/source-memory-crossfit-20261027/README.md)
is worse than a median predictor and underestimates all41resource sources>2x;
it is not deployed. [Duplicates](../artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md)
are only18literalNone failures,no substantive repeated proofs.
[Preemption occupancy](../artifacts/engine-resource-profile-2026-10-25/preemption-occupancy-20261027/result-review.md)
is overlapping work,not an Amdahl ceiling.

## Failure and scheduling

[Completed480profile](../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md):
83timeouts/355errors/42resource failures. interval_cases55.19%and simp_all28.21%
are observed timeout-thread CPU shares,not all-candidate wall fractions.
[Simp23](../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/README.md)
has20timeouts/3observer recursion faults,eight outer/six inner short-call cases
and nine long calls;no certified full-state cycle/failure witness.
[Interval48](../artifacts/hotspot-mechanisms-2026-10-25/interval48-import-repair-20261026T162128Z/README.md)
times out on both48-source conditions;0/48reliable failure coverage.
Closed-tail remains frozen0/71;branch counts/hashes are not failure proofs.

[Recovery-boundary reuse](../artifacts/hotspot-mechanisms-2026-10-25/recovery-boundary-20261028T131753Z/README.md)
recomputes the existing six native controls:an explicitly recovery-sensitive
custom tactic changes accepted→rejected under generic recovery disabling.
Ordinary first/backtracking stays accepted;failed-have stays rejected. This
synthetic counterexample excludes universal transparency,not a natural failure
rate. All71source-native parser rows have one final theorem;an after-theorem
command hook cannot skip later proof declarations there. That static fact is
not measured early-failure coverage. No generic wrapper is enabled or rerun.

[Full scheduling matrix](../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
at old2worker/24GiB-AS takes21746.81s all,15385.39s first-original,15112.12s
first-short(1.41347x/1.43903x),same142solvedtasks. This is pass@k,not RL rewards;
single-order comparison is not scheduling novelty. Task-held-out rank fit was
negative and is not deployed.

## Public Lean code verification

[Verina189](../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md):
46no-explicit-admission native exits,139admitted stubs,four API errors.
[Original lean-mlir module](../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md):
file/stdin/profile40.47/40.21/94.04s,equal successes. LRAT trace slices overlap
and cannot become an Amdahl fraction of40s native wall;one module is not all.
[Closed-CNF module](../artifacts/lean-code-verification-2026-10-25/shared-cnf-original-20261027T192501Z/result-review.md)
native/import/core/public40.15/40.34/57.98/56.91s,all accepted but proposed paths
slower. [Fused LRAT qualification](tmp/build-and-evaluate/step-0085-20261028T035549+0000/experiment-001/result-review.md)
proves stock-checker equality and executes seven certificate boundaries plus
native controls/first original theorem. Complete-module performance is pending;
ordinary fusion is not novelty. Its prepared pair waits behind resource work.

## Frozen evidence and full history

[GPU screening7808](../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md)
has exact statuses/3014accepted but8.86%more elapsed;34refuted intermediate goals
in29ordinary-error candidates remove no timeout. The old25/0.2%estimate came
from invalid wrapper data;do not reuse it as final coverage. No expansion.
[Frozen Goedel oracle](../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full-result-review.md)
is1.10627x aggregate with2rejection-to-completion changes,not our contribution.
[Selected1000CPU/GPU](../artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/full-result-review.md)
has no useful extra GPU gain;overlapping fallback totals are not strict ceilings.
E038,defeq/metadata/declaration,SMT-prefix and retained SHRED/ProofNet results stay
frozen. The [complete previous frontier](tmp/build-and-evaluate/step-0105-20261028T131753+0000/evaluation-history-through-1274950.md.gz) is losslessly archived;its
relative links were authored from docs/evaluation.md. A [readable pinned parent](https://github.com/yunwei37/gpu-smt/blob/1274950dfc2307b178d07a6d75165c780916036e/docs/evaluation.md)
retains those links and earlier archives. The unchanged36-page
[paper](paper/main.tex) remains incomplete;four-RQ final evidence,novelty and
independent audit are unfulfilled. No acceptance or project-completion claim.
