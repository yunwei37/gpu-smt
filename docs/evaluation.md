# Evaluation

Current phase: BOOTSTRAP, step0009 REVIEW_GATE after complete E030 acquisition
and full12serial root writing rounds. All four RQs and the scientific
contract remain open. Step0008 source/raw/paper/root audit were committed and
pushed to main as a476e6da8298e04e699b4e02726b53ea1a2a439e; publication does
not satisfy independent review or final-paper completeness.
[Current step](tmp/bootstrap/step-0009-20261014T114438+0000/step-report.md) holds gate records.
[Prior detailed evaluation](tmp/bootstrap/step-0007-20261010T000125+0000/archived-evaluation-before-direct-mini-20261014.md)
is retained byte-for-byte.

## Objective and questions

Lean-first complete verification acceleration, using RTX5090 and real ordered
public proof/program attempts. Preserve every accepted, rejected, incomplete,
failed and partial result. OSDI is a research target, not acceptance.

1. RQ1: How much expensive native preparation can real verification candidate
   streams share across independent jobs?
2. RQ2: Does branching from prepared native state preserve verifier responses
   and requested artifacts while isolating candidates and cancellation?
3. RQ3: How does prepared-state branching change end-to-end latency, throughput
   and memory at equal resources compared with established warm-session reuse?
4. RQ4: After preparation reuse, when does heterogeneous execution improve
   complete verification over the strongest measured CPU path?

## RQ4: complete native6 ProofNet comparison

All16conditions, each5952original source attempts, complete/valid;95232
outcomes. Three rotated primary repetitions plus four separate profiles.
Each matched primary preserves identical basic outcomes and CPU0–3/width4.
Warm native and native snapshot/cache are strong main competitors; the packed
CPU version is a component control. GPU integrates a narrow native Meta
beta/zeta reducer with readback, ordinary fallback and final native checking.
It is neither full GPU kernel checking nor metadata-only verification.

| Method, whole seconds | Rep0 | Rep1 | Rep2 |
|---|---:|---:|---:|
| native warm |310.478180|311.544205|318.571668|
| native snapshot/cache |319.523948|320.058833|331.711916|
| packed CPU control |319.509904|326.852216|321.050247|
| GPU native6 |315.870382|322.890819|323.607358|

GPU loses to strongest native CPU by1.736741%,3.642056%,1.580709%;
mean2.319835%, observed range1.580709–3.642056%, not a confidence interval.
This rejects a speedup claim for this mechanism/cohort. Component CPU/GPU
timing is not a hardware-only comparison: GPU has earlier negative head
refusal. The headline comparison therefore uses strongest native CPU.

One profile per method: warm328.046342/snapshot348.389767/CPU338.670063/
GPU342.948856s. Sampled tree PSS maxima5289626/9268751/5161250/6315211KiB.
Non-atomic one-second sampling misses short-lived/unsampled peaks; observer
CPU is included, GPUcontext/driver and other owners are excluded. Profiles
do not replace primary repetition uncertainty.

Raw/recomputation:
- artifacts/lean-gpu-checking-2026-10-13/experiment022/full4-proofnet/
- native6-three-primary-blocks-analysis.json, per-cell source/terminal/basic
  analysis and original complete ZIPs.
- runtime-native6-full-20261014032048Z/terminal-{job,pod}-api.json,
  terminal-container.log, full-proofnet-terminal-summary.json and outcome.json.

Actual finite Job/container succeed/exit0. Only owning Job/Pod deleted after
terminal API/log collection; canonical results restored to normal directory.
Both original Workspaces remain Running1/1/restart0.

## RQ4: complete miniF2F continuation

The full native6 miniF2F Job failed in a lab global OOM at 05:28:38 UTC
on 2026-10-14. Its native warm baseline returned663 candidates and launched
source663 without a result; GPU conditions had not run. Kernel victim RSS was
99,353,352 KiB. Scheduled Pod UID matches the kernel cgroup. This is failed
acquisition, not miniF2F latency or a GPU-memory result. Original7808sources,
16conditions/124928outcomes and complete32condition two-cohort scope remain
required. Raw failure/API/events/kernel records are retained under the runtime.

The owning Workspace Pod was subsequently replaced by its existing ReplicaSet;
same Workspace/PVC, deletion actor unknown. Old E015/R11/E008/SMT captures are
interrupted, not active. Complete original cells survive. Available-memory
snapshots did not bound this candidate. No memory cap/source exclusion or blind
retry has been applied. E018 resumed after restoring its dependency alias, then was stopped after
complete first-primary reanalysis found a slower path and five outcome mismatches. RTX5090 remains shared.

Plan: tmp/bootstrap/step-0007-20261010T000125+0000/experiment-022/plan.md.
Raw: runtime-native6-mini-20261014045320Z/output-root/full4-minif2f.
No extra small adapter version is admitted before completing both cohorts.

## RQ1/RQ3: deeper native preparation

Runtime11 shares imported search-index preparation once before native
body-free theorem-prefix owners. Same full12ProofNet conditions/71424inputs
and planned12mini/93696 remain in experiment024/shared-import-search.
First complete matched block: prefix1819.027655s, prepared496.784868s,
snapshot507.272168s, all basic/population valid. This implementation loses
in that block; remaining repetitions/profiles were interrupted by Workspace replacement. No whole RQ answer.

Superseded runtime9/10 matrices remain incomplete; original complete/partial
data and binaries are retained in verified lossless archives, never stitched
as new timing. Source/build/regression/cost are dependencies, not contributions.

E023 all30ProofNet/178560outcomes have prior independent raw review:
disposable branches lose to strong warm/snapshot under higher load.
Mini/full60 and scaling/placement/history/cancellation obligations remain.
E020 all24ProofNet complete; mini24 remains in the existing CPU queue.
Old finite retirement128/512 comparisons are explicit controls, not defaults.

## RQ3: real source-native SMT

E025 first full trio,3566sources/method, is reconstructed with identical
source/command/basic/native-status/requested-artifact records.
Stock1233.396666s, branch1539.323528s, logical1541.669126s:
branch24.803607%slower thanstock and only0.152147%better thanlogical,
one block, no superiority or confidence interval.2789earlier-source terminal
reuse sessions engage the mechanism; actual fork/translate counters absent.
Eight primary cells completed; the ninth was interrupted by Workspace Pod replacement.
The original12condition/42792outcome matrix is incomplete and no process remains active.
Plan/report: experiment-025/direct-result-first-trio-20261014T0328.md.
Raw: artifacts/autoverus-native-2026-10-09/experiment025/full1/.

## Supporting complete-source CPU checker

E018 original192context-cell matrix,14913source edits per condition, was stopped
after first-primary reanalysis found a slower path and outcome mismatches.
Its known prefix export failure in Mathlib context22 was repaired before disposition. Its failed attempt
remains intact. Direct acquisition repair falls back to unchanged native-full
only for a known unexportable prefix before any candidate; all original814
inputs complete, match stock, whole800.379800s includes failed prefix+fallback.
No external support/acceleration is claimed for that context. Both phase
CPU time files and continuous profile sampler require full accounting.
Original same-binary completed cells remain; full matrix is incomplete.
Raw/repair: artifacts/lean-cpu-checker-2026-10-13/experiment018/full1/.
E019 failed/partial/device startup history remains, not a complete baseline.

## Remaining evidence and publication

Complete mini cohorts; strongest source-compatible reuse/checker competitors;
native behavior/resource/cancellation/history; load/scaling/memory/placement;
causal mechanism coverage; closest-work novelty; full paper/compile/WRITE/
REVIEW/independent outer audit and completed-step main commit/push remain open.
Native5/4 and earlier GPU versions are complete historical negative evidence;
no cross-epoch causal tuning benefit or universal GPU impossibility is inferred.

Storage preserves complete original bytes/modes through verified lossless
inactive archives, with restoration receipts under experiment025. Active
datasets/SDK/CLI/credentials/native6/runtime11/runtime2 and other owners remain.
Future capacity is remeasured, not guaranteed by previous free-space values.

## Native hotspot selection and E018 first complete primary

All24contexts/14913original sources per E018 method: native32319.280591s,
external-prefix51050.157265s (57.9557%slower), five accepted-to-rejected differences.
One primary block/sums of context clocks at different times; no CI or final
repeated service-throughput result. The external integration is invalid for a
native-equivalent speedup claim. Further acquisition stopped through its own
cleanup path; completed and partial raw remain. The192cell plan is incomplete.
See experiment018/first-primary-result-disposition-20261014.md.

E026 uses built-in native diagnostics over all5952 original ProofNet sources.
It is supporting hotspot attribution after the completed E015 simp/typeclass
categories, not another GPU speedup experiment. Default report threshold censors
low-frequency counts; counts are not CPU costs/GPU eligibility. Build/preflight and complete5952source acquisition succeeded. Basic outcomes
match the complete native control.4898sources emit diagnostics; outParam recurs
in2970sources/2967distinct source strings, and Ring.toSemiring in1735/1732.
These are source-coverage observations, not actual-work counts or measured
projection costs; default threshold/name alias/snapshot replay are disclosed. Plan and raw under
artifacts/lean-parallel-verification-2026-10-12/experiment026/.

Reanalysis of original classified E015 counter snapshots pairs5951completed
sources, retains one censored operational source and finds369.605477s observed
exclusive native-miss CPU:97.576700s has none of the four recorded context flags;
272.028777s has at least one. This is a miss-scope subset, not a whole-time/GPU
ceiling. Joint masks/marginal overlap and zero-flag noneligibility are disclosed
in experiment026/classified-source-delta-review.md. No new timing run was needed.

## Exact projection cost and stronger CPU candidate

E027 completed5952original sources with zero basic differences;5951source
counter pairs and the original censored operational source. Observed exclusive
miss CPU232.678006s: seven named families16.910503s (7.2688%), generic projection
expressions44.087492s, other171.680011s. No whole-time/GPU ceiling follows.
Per-operation projection offload is rejected as the next implementation. Raw
standardZIP/parser/source/result review are under experiment027/.

E028 implements conservative closed-term memoization in native reducible/instances
modes, which the pinned4.9 native cache does not cache. Exact native
configuration/environment/options scope, unchanged native mctx/environment and
closed result guard; all other inputs use original native computation. It is a
strongerCPUcandidate, not novelty. Build0/0/0/0; original0reject/257complete and
actual cache hits observed. Intended warm-pool/fourworker readiness completed on the original8cases;
all8full comparison cells completed. Final results and disposition follow below.
No memory budget/cap/model/Workspace/scheduler change.

E028 first complete5952source pair: original320.210026s, cached296.560437s,
7.3856%whole wall reduction/1.0797x. All original outcomes match; two auxiliary
proof value hashes differ with matching types/main theorem hashes. The complete
3repetition/2resource-profile result is recorded below; no OSDI/RQ
completion/GPUcomparison is claimed. Cache terminal observations show actual
engagement; failed-process censoring/peak-entry nonpeak semantics disclosed.

E028 all3primary pairs now complete: wall reductions7.3856%,-0.0617%,
-1.0334%, zero basic differences on all5952sources. The first-pair improvement
did not stably replicate; no proven end-to-end speedup. Two resource profiles
also completed, with no mid-run implementation/baseline change. Current officialWHNF
already caches eligible modes with configuration keys. Do not present this
older-version CPUprototype as novel/current-release superiority. Details and
uncertainty:experiment028/complete-primary-result-review.md.

E028 complete8cell/47616outcome experiment returned: no stable paired wall
acceleration; resource profiles PSS7864846original/7798128cachedKiB differ0.8483%
in one sampled comparison. No replicated memory improvement established.
Candidate closed with code/raw retained; official current unifiedWHNF cache
already covers this mechanism. AllRQs open; expression/reflection next.

## Step0008 / RQ3 shared-process placement

Experiment029 is admitted as a decisive complete native parallel/resource comparison,
not a GPU metadata proxy. All5952original sources against strongest warm4process pool;
three alternating primary pairs plus2profiles. Same native boundaries/defaults/300s
allowance andCPU0–3. [Plan](../artifacts/lean-parallel-verification-2026-10-12/experiment029/plan.md)
and direct-only self-review are saved. Implementation/build/preflight pending; no run
or performance outcome yet. Original full Lean/SMT/5090/four-RQ goal remains.

Experiment029 complete3primary pairs now contradict faster shared-process verification:
warm303.028963/303.825857/303.671271s, shared371.637252/360.690135/349.614219s,
slowdowns22.6408/18.7161/15.1292percent. All5952per-input basics match in everypair.
Shared panic retains13/14/13native fallback inputs/costs. Requested diagnostic hints
have internal metavariable-number differences for2913 and some2928; no normalization
or universal artifact transparency. Resource profiles still completing. Actual
analysis reconstructs fallback admission-to-response from original shared admission,
rather than reporting only the later fallback phase. Whole clocks were alreadycomplete.

E029 all8cells/47616outcomes complete, root direct result review saved. No faster
shared-process result:22.64/18.72/15.13percent slower. Single PSSprofile5.52percent
lower is unreplicated and private memory is not comparable as COW mutation.
All per-input basics match; native diagnostic metavariable IDs differ, preserved.
Candidate closed; complete source/failed/fallback/observer/raw and analysis under
experiment029. Driver terminal. Return to WRITE, all four RQs still open.

## E030 complete response-path comparison (running)

Root directly implements a necessary sorry-kind header precheck followed by the
original complete Syntax predicate, preserving native traversal/goals/feedback.
Same original5952ProofNet candidates and warm-pool host/runtime. First complete
primary pair:303.124060s original,297.519943s gated (1.8488percent wall reduction).
All basics and requested responses match. This one pair does not establish stable
acceleration; opposite-order repetitions and separate profiles are still running.
Plan, source, real preflight, failed build and first result preserved in
artifacts/lean-parallel-verification-2026-10-12/experiment030/.
Current official Lean4.35.0 remains unmeasured here; old4.9cohort results are
same-version evidence, not current ecosystem superiority or systems novelty.

E030all8cells/47616outcomes now complete with zero per-input basic differences
across all8versus original native warm control. Three paired wall reductions
1.848787%,2.312629%,0.724019% have descriptive mean1.628478%, not a CI.
Complete matched timer subset5791sources: sorry CPU8.476280494original/
0.663863863gated; response extraction20.169632959/12.296172330seconds.
Calling-thread scopes exclude async frontend/serialization/auxiliary construction;
interleaved or incomplete records remain censored, not reconstructed. Single
PSSprofile7860678original/7728536gatedKiB is not replicated savings.
Keep the small CPU precheck as an available stronger measured comparator; no GPU
benefit, systems novelty or closed RQ follows. Complete result-review/analysis/raw
are under experiment030. All12writing rounds compile to10pages and all10pages
were inspected. Root review/outer self-audit are direct-only; independent audit
remains unmet under the explicit no-delegation instruction.
