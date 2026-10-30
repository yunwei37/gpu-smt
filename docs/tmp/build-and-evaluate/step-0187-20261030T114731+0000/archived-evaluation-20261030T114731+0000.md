<!-- Archive of docs/evaluation.md at 796ae174ff6f49777aa6f7a6c828ef20514852c3; original dates/statuses retained.
Only relative Markdown destinations are rebased for this location.
Current evidence: ../../../evaluation.md
Original file: https://github.com/yunwei37/proofserve/blob/796ae174ff6f49777aa6f7a6c828ef20514852c3/docs/evaluation.md
-->

# Evaluation: current evidence and open work

Updated2026-10-30UTC. Root only;reviews are self-review,not independent audits.
The [original four RQs](../../../idea-story.md),Lean/SMT scope and OSDI objective remain
open. Tests,a compiled draft and selected timings do not establish novelty.
All raw,failed,partial and superseded evidence remains;detailed history is below.

<a id="current-decision-frozen-oracle-and-three-continuing-directions"></a>

## Current directions

Root currently integrates paper/evidence while W owns workloads, M owns
mechanism measurements and O owns engine/open-source changes. The user-approved
existing Workspace now runs on phobos-vt with the same 128 GiB PVC. Total lane
budgets are 40 GiB (W16/M16/O4/root4), each at most 8 cores. Root uses 0–1 for small
analysis/builds. Current signal controls still return errno 13; no functioning
signal watchdog is claimed. Owners retain natural-exit bounded native methods.
Mainline selection awaits W/M and the user's decision; no extra Agent is started.

The matched four-warm Kimina versus repaired-engine full7808resource pair
is complete with equal basic outcomes and19.28%less elapsed on this one point. Repair/measure resource performance before stacking
task-memory,ranking,failure or LRAT gains. An earlier user decision stops interval_cases parallel development and
requests complete-state expensive tactic reuse measurements, especially native
strategy failures. Current W/M work broadens workload and mechanism evidence. The corrected42capture has completed;the earlier selected-population
native input/cost capture was interrupted; its historical recovery is prepared,
not running. Its interruption/recovery records are retained below. Timeout and memory
failures are not interchangeable with tactic exceptions.
The four continuing directions remain:
the layered Rust engine,reliable early failure,multi-candidate inference and
public Lean code verification. There is no project deadline or closure rule.
Resource/COW/cache/ordinary compilation/cancellation primitives are prior work;
prospective novelty needs workload-level evidence. CPU oracle stays frozen.
No additional competitor reproduction,Agent,Workspace or checkout.
Exact authority remains [the user log](../../../user-instruction.md).

| RQ | Frozen question | Current status |
|---|---|---|
| RQ1 | How much expensive native preparation can real verification candidate streams share across independent jobs? | unanswered:complete preparation-cost/context coverage remains missing |
| RQ2 | Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation? | unanswered:full native artifacts,history,cancellation and supported scopes remain incomplete |
| RQ3 | How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse? | unanswered:one full warm-resource pair is complete with limits;scaling/repetition promises remain open |
| RQ4 | After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path? | unanswered:no useful extra full-flow GPU gain has been demonstrated |

<a id="current-resource-point"></a>
<a id="resource-point-and-workloads"></a>

## Resource point

Current placement and lane limits are described above. The48GiB/CPU8–11
four-worker service measurements below are the historical matched lab point,
not current phobos-vt limits or a new allocation. Their1s sampled watchdog,
dynamic admission, solo retries and no fixed process AS belong to that point.
Sampling overshoots are not a kernel quota. Earlier2worker/24GiB-AS and later
G10/phobos-vt records remain separate; no clock is rescaled across them.

## Complete native/Mathlib-derived pair

[Own fresh/prepared7808 pair](../../../../artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/result-review.md)
has equal3013accepted/4665rejected/87timeout/41resource/2backend statuses.
Whole28391.98/22891.51s=1.24028x is an own-component comparison,not strongest
warm-service benefit or novelty. Empty ast differs in7660prepared replies;
86operational strings differ. Fourteen preparations/62fallback rows are charged;
sampled peaks48.77/48.93GiB overshoot. Both engine cells omitted the ordinary
native Mathlib library that historical warm loaded,an additional code-context
confound. Two EOF/deep-simplex faults have unknown exact cause.
[Earlier ENOSPC pair](../../../../artifacts/engine-resource-pair-2026-10-25/full7808-20261026T004621Z/README.md)
retains prepared partial data. Historical accepted3086became timeout;new
own-pair equality does not erase that change.

## Resource-layer diagnosis and missing warm comparison

Historical warm21693.76s is2worker/24GiB-AS/HTTP versus new4worker/no-AS/retry
points;the six status differences and native-library confound forbid a matched
claim. [Old FIFO closure](../../../../artifacts/engine-resource-profile-2026-10-25/policy7808-20261028T034248Z/README.md)
returns all7808with the earlier prepared raw outcomes. Its22716.04s internal
clock has no complete external counterpart after the old controller pause.

[Disjoint singleton analysis](../step-0088-20261028T053756+0000/experiment-001/result-review.md):
10375.98s has one child(45.33%of its own cell);8924.78s/86.01%is actual exclusive
retry,1232.45s/11.88%retry-pending proxy,and218.33s/2.10%final timeout tail.
Occupancy is not CPU/removable time. Failure/timeout lifecycle unions overlap;
42of62fallback rows are the same exclusive checks,not extra additive work.
[Growth analysis](../step-0096-20261028T103651+0000/experiment-001/result-review.md)
finds41solo peaks>47.5GiB lower bounds;4658/7389exclusive samples have16GiB
headroom. These are not time shares,future memory caps or safe-backfill proof.

Retired-PID history scanning and stale queued global forecasts are repaired.
[Retry-frontier source/controls](../step-0094-20261028T102232+0000/step-report.md)
remove the mid-frontier drain barrier;no speculative backfill is enabled.
[First corrected24pair](../../../../artifacts/engine-resource-profile-2026-10-25/warm-resource-qualification-20261028T044624Z/README.md)
loads the same ordinary native Mathlib library on both sides. Warm1430.68s
returns14accepted/7error/1timeout/2resource;oldengine1540.71s returns14/5/3/2.
[Frontier24](../../../../artifacts/engine-resource-profile-2026-10-25/gpu-smt-resource-retry-frontier24-20261028T110236Z/README.md)
takes1347.58s with unchanged engine outcomes.
[Reply-retirement24](../../../../artifacts/engine-resource-profile-2026-10-25/gpu-smt-resource-timely-reply24-20261028T115820Z/README.md)
takes1349.55s(5.67%less than retained warm);14accepted IDs agree,but2507/7230
still time out only in engine. It changes no raw frontier outcome. The protocol
repair is real but did not explain those differences;selection/order/shared
host prevent a full gain claim. All registered native births retire.

[Full7808 plan and actual start](../step-0102-20261028T122519+0000/step-report.md):
one finite serial warm→engine pair started12:25:19UTC,source13d4606.
Four warm workers actually mapped the matched library. No full terminal or
speedup is claimed;inspect actual PID/birth and terminal before continuation.
Later [exact-median maintenance](../step-0103-20261028T123153+0000/step-report.md)
preserves forecasts with no repeated sort;66workspace+5native CI controls pass.
Later [IO deadline correction](../step-0104-20261028T124447+0000/step-report.md)
has a deterministic old-selection overrun control and68workspace+5native CI.
Neither change replaces frozen13d4606 or has a measured whole-flow benefit.

[Historical42solo](../../../../artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z/README.md)
is41budget failures/1timeout,no accepted,and48.23GiB sampled peak;it lacked
explicit matched native-library selection. The corrected fixed42 cohort is
prepared/rebound to13d4606. After actual full-pair retirement/review,it
[started separately](../../../../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/README.md)
at2026-10-29T05:35:59UTC,one four-core-eligible fresh native request at a time.
The ordinary native library and unlimited-AS point has now completed;its own
[complete raw results](../../../../artifacts/engine-resource-profile-2026-10-25/solo42-native-library-20261029/result.json)
are retained separately. The earlier41/1record is not substituted for this run.

[Complete four-warm full7808 leg](../../../../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/README.md)
now returns3014valid/4668lean_error/85timeouts/41budget failures in25176.487277s
external wall. The [complete engine cell](../../../../artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md)
ends20323.007642s,1.238817x/19.2778%less elapsed,with exact7808status/3014accepted
ID parity. Warm7860attempts/52retries versus engine7850/42are fully retained.
The engine has one prepared-ready event,42solo and18import-different fallbacks.
Raw native payloads differ on7682IDs;even removing only env/empty ast leaves
23rejected-source diagnostic/optional-field differences. All126operational
strings differ. Peaks48.768776/48.805775GiB include sampled overshoot.
Immediate-warm versus frontier-engine retry order,affinity,single order and
shared support work prevent a COW-only or general strongest-service claim.

[Response-origin analysis](../../../../artifacts/engine-resource-profile-2026-10-25/native-response-origin-20261029/README.md)
reproduces16optional-field differences through the installed model serializer
and relates22embedded coordinates in7sources to the3removed header lines.
All23also match historical fresh responses in the same two-field view,but
its library/executable context differs;this is not a new matched native proof.
Original raw differences remain,no response normalization or engine patch.

## Own load-aware methods

[TaskMemory32](../../../../artifacts/engine-resource-profile-2026-10-25/task-memory32-20261027T193536Z/README.md):
2832.46/2169.74s,23.40%less elapsed,exact16accepted/7rejected/9resource outcomes;
attempts41→37,retries9→5. Tail/outcome-informed selection,single order/sharedhost,
CPU11support and sampled overshoot prevent population/novelty claims.
The prepared full policy queue ran only its FIFO cell;three policy cells remain
deferred. Predictions never reject;lower-bound sibling peaks can misreserve.
[Held-out memory fit](../../../../artifacts/engine-resource-profile-2026-10-25/source-memory-crossfit-20261027/README.md)
is worse than a median predictor and underestimates all41resource sources>2x;
it is not deployed. [Duplicates](../../../../artifacts/engine-resource-profile-2026-10-25/exact-duplicates/result-review.md)
are only18literalNone failures,no substantive repeated proofs.
[Preemption occupancy](../../../../artifacts/engine-resource-profile-2026-10-25/preemption-occupancy-20261027/result-review.md)
is overlapping work,not an Amdahl ceiling.

## Failure and scheduling

[Completed480profile](../../../../artifacts/lean-failure-profile-2026-10-25/full480-analysis/result-review.md):
83timeouts/355errors/42resource failures. interval_cases55.19%and simp_all28.21%
are observed timeout-thread CPU shares,not all-candidate wall fractions.
[Simp23](../../../../artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z/simp23-analysis/README.md)
has20timeouts/3observer recursion faults,eight outer/six inner short-call cases
and nine long calls;no certified full-state cycle/failure witness.
[Interval48](../../../../artifacts/hotspot-mechanisms-2026-10-25/interval48-import-repair-20261026T162128Z/README.md)
times out on both48-source conditions;0/48reliable failure coverage.
Closed-tail remains frozen0/71;branch counts/hashes are not failure proofs.

[Known-statement controls](../../../../artifacts/hotspot-mechanisms-2026-10-25/known-statement-controls-20261029/README.md)
prepare two unexecuted Lean negation certificates for publicly known defects,
not new discoveries or a deployed rejection rule. Exact retained theorem text
matches32log/31Nat-subtraction sources;one literalNone remains unmatched.
The true four-digit-cardinality task still has29resource failures. Its9596.64s
admitted-envelope sum is overlapping cost,not workflow time or predicted gain.
Finite arithmetic sanity/primary-source inspection do not certify native
acceptance equivalence;those Lean certificate controls remain unexecuted and
deferred behind the current tactic-input measurement,without an automatic queue.

[Recovery-boundary reuse](../../../../artifacts/hotspot-mechanisms-2026-10-25/recovery-boundary-20261028T131753Z/README.md)
recomputes the existing six native controls:an explicitly recovery-sensitive
custom tactic changes accepted→rejected under generic recovery disabling.
Ordinary first/backtracking stays accepted;failed-have stays rejected. This
synthetic counterexample excludes universal transparency,not a natural failure
rate. All71source-native parser rows have one final theorem;an after-theorem
command hook cannot skip later proof declarations there. That static fact is
not measured early-failure coverage. No generic wrapper is enabled or rerun.

[Full scheduling matrix](../../../../artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730/full-result-review.md)
at old2worker/24GiB-AS takes21746.81s all,15385.39s first-original,15112.12s
first-short(1.41347x/1.43903x),same142solvedtasks. This is pass@k,not RL rewards;
single-order comparison is not scheduling novelty. Task-held-out rank fit was
negative and is not deployed.

## Public Lean code verification

[Verina189](../../../../artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/result-review.md):
46no-explicit-admission native exits,139admitted stubs,four API errors.
[Original lean-mlir module](../../../../artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z/README.md):
file/stdin/profile40.47/40.21/94.04s,equal successes. LRAT trace slices overlap
and cannot become an Amdahl fraction of40s native wall;one module is not all.
[Closed-CNF module](../../../../artifacts/lean-code-verification-2026-10-25/shared-cnf-original-20261027T192501Z/result-review.md)
native/import/core/public40.15/40.34/57.98/56.91s,all accepted but proposed paths
slower. [Fused LRAT qualification](../step-0085-20261028T035549+0000/experiment-001/result-review.md)
proves stock-checker equality and executes seven certificate boundaries plus
native controls/first original theorem. Complete-module performance is pending;
ordinary fusion is not novelty. Its prepared pair waits behind resource work.

## Frozen evidence and full history

[GPU screening7808](../../../../artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/result-review.md)
has exact statuses/3014accepted but8.86%more elapsed;34refuted intermediate goals
in29ordinary-error candidates remove no timeout. The old25/0.2%estimate came
from invalid wrapper data;do not reuse it as final coverage. No expansion.
[Frozen Goedel oracle](../../../../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/full-result-review.md)
is1.10627x aggregate with2rejection-to-completion changes,not our contribution.
[Selected1000CPU/GPU](../../../../artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/full-result-review.md)
has no useful extra GPU gain;overlapping fallback totals are not strict ceilings.
E038,defeq/metadata/declaration,SMT-prefix and retained SHRED/ProofNet results stay
frozen. The [complete previous frontier](../step-0105-20261028T131753+0000/evaluation-history-through-1274950.md.gz) is losslessly archived;its
relative links were authored from docs/evaluation.md. A [readable pinned parent](https://github.com/yunwei37/gpu-smt/blob/1274950dfc2307b178d07a6d75165c780916036e/docs/evaluation.md)
retains those links and earlier archives. The current37-page
[paper](../../../paper/main.tex) includes the complete corrected resource table,with
[actual targeted compile/layout evidence](../step-0120-20261029T053959+0000/paper-check.json).
Four-RQ final evidence,novelty and independent audit remain unfulfilled.
No acceptance or project-completion claim.

## Complete retry-tail engagement — 2026-10-29

[Step0124](../step-0124-20261029T065342+0000/step-report.md) reuses all7850engine attempts from the complete7808pair. Four native candidate-process envelopes cover95.3%of ordinary time;42exclusive envelopes take9145.23s,97.5%of single-candidate time and45.0%of whole time. This confirms the existing queue-tail fix engages;it is not CPU utilization,a safe memory-overlap bound or isolated speedup. The41solo resource failures/1timeout remain. No new native collection or workload policy is introduced.

## Elastic branches and complete-state tactic caching — initial opportunity

[Step0126](../step-0126-20261029T071858+0000/step-report.md) reuses the full process/Syntax populations and distinct historical480profile. The18.38%rooted count is ProofNet;miniF2Fis13.44%. Four named expensive outer tactics make461/3987and82/3957rooted repeats;complete-state hits/time remain unknown. Current42tail IDs have older CPUdominated73.04%byeqRefl,not the83timeoutgroup. Missing same-run dependencies/state/cost require the user-authorized profile after42. No parallel/cache mechanism or gain is enabled/claimed.


## Native input matching and completed error cost — actual measurement

[Step0131](../step-0131-20261029T091211+0000/step-report.md)
qualifies the native boundary,not a cache:24real sources x3modesmatch statuses/
raw diagnostics,4originalnativeREPLsourcesagree,and safe low-threshold injection
actually kills/requeues/retires4workers. Sourcepositions/info trees/message/terminal
handling follow the pinned native procedure. Exact tactic text is compared;
fresh goal generation is a separate replay qualifier,not target-expression identity.

The [frozen selected-population capture](../../../../artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/populations/README.md)
was launched fromae59c77:2045miniF2F+632ProofNetsources x3modes=8031
elaborations,one48GiB/noAScollection;the later interruptions below supersede
that startup observation. This is not all7808or13760sources,nor a
four-workerwarm-service comparison. SDK--rundriver overhead and opaque/hidden/
posterror/HB/diagnostic replay limits remain explicit. No failurecache,early reject,
novelty or end-to-endgain is claimed before complete data and implementation.
Keep raw failures and analyze completed ordinary-error repeats,unreached and
operational cases separately;no old proxy/cross-run time denominator is substituted.

[Step0133](../step-0133-20261029T102319+0000/step-report.md)
recomputes the retained native positive control: the intentional ordinary-failure
pair matches after the existing environment-comparison repair. This is not a
population hit rate. Offline result analysis now separates original resource
attempts/final retries, timeout/late returns, memory/heartbeat/recursion/interrupt
diagnostics and explicit watchdog events. Completed ordinary-error costs require
a prior completed producer in the same process; unstable outcomes and operational
sources get no such credit. [Step0134](../step-0134-20261029T113605+0000/step-report.md)
adds per-kind cost/eligibility and source-level reachability denominators,
and corrects an old preflight reachability description from its raw calls;
no source verdict or later positive-control match changes.
The launch used its frozen qualified observation source,without an enabled
cache or second collection;this records source provenance,not current liveness.

## Actual population interruption — 2026-10-29

[Step0135](../step-0135-20261029T123554+0000/step-report.md)
preserves a [failed partial capture](../../../../artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/populations/partial-20261029T1233/README.md):
2640original-mode rows,5RSSpreemptions/14timeouts among them,and no observe/import
phase yet. An additional original proofnet-5879attempt exits1 with native
Nat.pow panic before a result row;the old controller stops and allworkers retire.
This supersedes the earlier running observation,not the raw launch metadata.
Match rate and saved time remain unknown;repair and continue unfinished cells
without discarding the healthy prefix or five deferred resource retries.

[Step0136](../step-0136-20261029T124312+0000/step-report.md)
repairs this operational failure and qualifies original5879/minif2f7 across
three modes:3explicit native-process failures,3subsequent native completions,
allworkersretired. Continuation preserves the prefix and5deferred resource
retries;one old unreported panic is explicitly derived with unknown elapsed.
Phased diagnostic completion cannot claim an uninterrupted end-to-end speedup.

The [actual continuation](../../../../artifacts/hotspot-mechanisms-2026-10-25/state-reuse-native-20261029/populations/continuation-20261029T125316/README.md)
started12:53:16UTCfrom aee0932with unchanged native modules and resourcepoint.
Before the later eviction,its frozen pipeline returned new rows beyond the
preserved prefix.5390unfinished cells/5deferred resource retries were restored.
Fullselected match/cost results remain pending;no uninterrupted-performance claim.


## Current recovery status — after the storage eviction

[Step0140](../step-0140-20261029T170259+0000/step-report.md)
records the16:05:43UTC ephemeral-storage eviction and automatic replacement of
the same Workspace onG10. Only2640rows are archived;one old panic row can be
derived from retained evidence,while at least1273newly observed entries are
currently unavailable. Final eviction-time count/outcomes are unknown.
No formal collection is running. The8031input and5390pending/5retry plan are
preserved on the existing PVC. The user now directs staying onG10 and
cancels the lab-placement proposal. A future G10 capture is a fresh hardware
point,not an elapsed-time continuation using lab's original-mode denominator.
[Step0142](../step-0142-20261029T182504+0000/step-report.md)
adds the requested early PVC-output check;the next collector snapshot is5e563f9.
[G10 semantic controls](../step-0143-20261029T183313+0000/experiment-001/result-review.md)
validate one custom failed-state example,not the formal workload/resource point.

[Offline input control](../step-0145-20261029T191343+0000/experiment-001/result-review.md)
finds2677distinct complete source strings in each mode,including2045miniF2F
and632ProofNet;exact-source duplicate groups are zero. Intentional repetition
across the three measurement modes is not a workload cache opportunity. This
does not determine full-state matches,cost,coverage or speedup.


## G10 continuation — user-directed separate hardware point
The user directs staying on the present Workspace/node and no scheduling change
or further lab question. Actual G10 eligibility isCPU0–7,total RAM about27.8GiB;
the selected prospective collector point is12GiB total owned sampled RSS,
no fixed per-process AS limit,one native frontend,eligible CPUs0–7. This leaves
about15.8GiB physical RAM outside the research budget;availability remains shared
and must be observed at launch. Output stays on the existing PVC.

No formal capture has started. Two-second same-UID controls show TERM/KILL
returning PermissionDenied;the children retire naturally. The mandatory watchdog
cannot currently guarantee interruption,so no long/large Lean collection is
admitted on that execution path. No permission/security change is requested or
made. Continue G10 Rust development and simulated tests;this is not a negative
cache-opportunity result or a reason to return tolab.

The collector now accepts an explicit budget/CPU selection and records actual
hardware/boot identity in lifecycle/terminal output. It rejects a budget exceeding
host RAM and refuses a continuation lacking matching resource/hardware records.
Historical source/data remain frozen. Any eventual G10 three-mode comparison
must execute its own selected2677sources in all3modes rather than borrowing
the2640retained lab original rows.12GiB resource censorship is separately reported;
no cross-hardware speedup or strict globalAmdahl bound follows.

The user subsequently approves this12GiB/serial/PVC point and requires an
immediate whole-collection stop on API unreachability or hostMemAvailable below
about6GiB. The node hosts control-plane/etcd. The resource-option patch alone did not implement those guards.
The later guarded source below implements their operational paths,but no
capture can start on the signal-denied path;healthy unit-test activity is not
under-load native qualification. A1s sampled threshold cannot be called a hard kernel RSS limit.


## Shared-node guard implementation — step0150
Current finite collector source defaults/caps sampledRSS at12GiB. It checks
hostMemAvailable>=6GiB,owned PID/group signal retirement before native startup,
and existing-account API readiness. Background probing preserves independent
RSS sampling;API failure/stall or low available memory aborts the whole
collection,never fabricating a source rejection or hiding a pending API failure
at successful termination. No CronJob or cluster runtime setting changes.

81Python tests pass. An actual G10 guarded-entry qualification,CPU6–7/PVC,
stops at denied PID signalling:the2s Python control naturally retires,zero Lean
processes launch,zero candidate results and no complete terminal are written.
No native workload result,API pressure test or hardRSS quota follows from it.
G10 still requires working interruption and readiness observability before
native capture can run. No permission or lab-placement request is made.

## 2026-10-30 — resource-tail and exact first-success opportunity

The full41resource cohort and two7808point cost-selection matrices are complete
in step0163/1d5e990 and step0164/952cae6. Source/whitespace/last-line groups are
proxies,not complete native failure keys;41RSS-watchdog outcomes do not certify
cross-budget deterministic failures. Exact entry-state match remains unknown.
At the matched four-worker point,short-source frozen work is only1.018423x
the minimum first-success work that still exhausts all102unsolved tasks.
A task-heldout p/c predictor reduces work0.3874%but lacks end-to-end evidence;
sibling history and charged one-probe restart do worse. The restart row is
not full Gittins and has unknown original-budget eligibility. No unsafe resource
cache or unvalidated runtime scheduler is enabled. Primary literature and
paper now distinguish algorithm-selection/search/restart precedents from a
prospective native-semantics contribution. Four directions/RQs remain active.

## Latest correction — runtime-only and cross-proof call granularity

Source-feature success/cost ranking is frozen,no retraining. Step0166/4741ad8
uses retained native Syntax and proof-relative mapping for all41resource failures:
19narrow have/rw/rfl templates,5different proofs with the same explicit finite
filter target template. Four later current envelopes889.82s;separate historical
rfl CPU442.05s across5. These are not complete native state/resource witnesses.
Steps0167/1772b1a and0168/77ea9f9complete elapsed-only LAS/completion-index
resume/restart models on both7808points,including the immutable previously
measured short-order control. No source features are recomputed for it.
Mean task latency improves in the CPU proxy,but consumed work/batch timing
worsen and RSS/original-budget parity is unqualified. No runtime feature is
enabled;exact finite bounds/exhaustive unsolved groups remain explicit.


## 2026-10-30 — root paper integration after authorized parallelization

User assigns workloads/ to W, engineering/onboarding to O and
research/mechanisms-2026-10-30/ to M. Root owns manuscript/evidence integration,
not those implementation paths. The title, abstract, introduction, design,
implementation and all four RQ texts remain byte-identical in this paper update.
No cross-proof reuse thesis or new novelty claim is adopted before W/M evidence
and the user's decision. Root uses only two eligible CPUs and its4GiB share of
the new40GiB aggregate;this does not rerun historical48GiB experiments.

The existing Workspace/PVC is restored onphobos-vt. Root's short same-UID
Kubernetes-exec controls still observe errno13 for TERM and KILL. Both2-second
Python children naturally exit0 and are confirmed retired. Their birth identity
and return codes are archived in step0174. This entry-path observation does not
establish whether an untested Coder SSH execution path can signal its children.
No security adjustment or native long capture follows.

Step0170/f41c3f0 provides all21396retained AutoVerus timing cells. Three direct
passes cover3566sources each;reportedRust+VIR+nonSMT-AIR is75.33–75.68% of
reported native time. SMTinit+run is9.77–9.87% of summed external candidate
process time,not whole-service wall.17missing timingJSON and341missingSMT
fields per pass remain explicit. Paper now includes these per-pass costs.

Step0174 reproduces the earlier read-only196-log accounting directly from the
retained compressed archive without extraction. Logger endpoints sum84267s;
1652inference labels sum80835.416549206s(95.9277%). Residual3431.583450794s
contains verification and other work;exactgeneration/verification ratio stays
unknown. Two negative per-log residuals remain at one-second resolution;
archived Python does not reconstruct the historical inference timer. API waits/
retries are included. No2026native or cross-hardware denominator is substituted.

Step0173/eefd07f audits96sources in the three largest observed-unsolved tasks:
19451.516132460/52992.124105687 physical-attempt seconds(36.7064%). Coverage
is95nativeSyntax sources and79independent historical profiles. The same
five-source closed-target projection is found,all with resource failures.
Actualreads,ordinary-failure producers and replay saving stayunknown. The
manuscript records this scope without making it a new central mechanism.
Salsa/Adapton and the existingSHRED citation delimit read-set reuse precedent.

At the frozen W03d8f95/M573c3d8snapshot,W enumerates163097Lean source files,
not verified candidates or per-proof native times. M's G10PMU probes are denied;
the392shared-library-file census is not a native-execution fraction or evidence
about PMU permissions onphobos. These initial artifacts do not settle the
paper's mechanism. Root reads them but makes no edits to the branch-owned paths.


## 2026-10-30 — root audit of completed M1149a59 evidence

The root reads but does not edit M's1149a59mechanism results. The200-source
stratification actually has50accepted/60rejected/50timeout/40resource-exhausted,
200uniqueIDs,94priorprofiles and0freshLeanexecutions.290have/106<;>/5all_goals
are structural top-level Syntax counts. Missing aligned mctx edges and node
durations leave work/critical-path/average available parallelismunknown.
The two usable completed-request atomic bounds do not settle parallelism.
Paper records this coverage rather than a positive/negative1.3x conclusion.

All12memory-model cells complete under M's frozen-demand assumptions.
Budget-fit sizes7718/7766/7766/7808vary across the8/16/32/48GiB scenario budgets.
These are offline model parameters,not new native budget acquisitions or a
change to the current40GiBfour-lane allocation. All3014frozen accepted IDs
survive in the selected subsets,which is not same-budget native verdict parity.
Fixed-pool overcommit in every row invalidates its apparent compliant-baseline
speed. Immediate/zero-cost kills omit10/49/38/48originalterminal labels;
those are operational omissions,not reusable Lean rejections.
Admission retains all selected frozen labels while conservatively reserving
observed peaks. Censored/time-varying demand,shared-parent accounting and native
retirement are not resolved;no COWdiscount orphysicalfrontier is inferred.
Root numeric/status invariants pass. No M script is rerun or modified.

The main thesis and four RQs are unchanged. These feasibility findings motivate
continued native evidence,not adoption of a cross-proof mechanism or a new
contribution before W/M evidence and the user's scientific decision.


## 2026-10-30 — root cross-check of W002 and native reuse baseline

Root checks the derived CSV tables at W commit daffefc without editing or
rerunning W's source scanner. All 163,097 unique file paths, 1,785,499,363
source bytes, and tactic totals match. Reconstructing the internal graph gives
370,864 edges, a longest unit-weight chain of 451 modules, a largest same-depth
layer of 9,225 modules, and 130,834 modules reachable from the OAI root.
The largest 2,610 files (the ceiling of 1.6%) contain 40.1099% of source bytes.
This is an internal-consistency self-review of derived tables, not an
independent full source scan or acquisition of native costs. It takes 2.36 s,
with a process peak of 140,664 KiB and zero native verification executions.

The publisher's pinned README, toolchain, and Lake sources describe a release
with mixed verification status, one large Lean library, Lean 4.34.1, and a fixed
Mathlib revision. The lexical count of 1,354,379 decide +kernel forms in
5,848 files is not a count of repeated reductions. Lean 4.34.1's actual Decide
and AuxLemma implementations include a branch-local type-indexed cache with
privacy/defeq flags and universe-parameter matching. Its lookup table is not
serialized in .olean files. These source facts establish neither a corpus hit
rate nor cross-request reuse. The decide +native form is also an entry to native
evaluation, so absence of literal native_decide names cannot prove absence of
that route. Transitive axiom closure requires separate evidence.

The paper records this static workload and the existing native cache baseline.
It adds no mechanism, measured native time, acceptance claim, or global speedup
bound. The title, abstract, introduction, design, implementation, and all four RQ
descriptions remain unchanged. W and M continue their candidate, native-cost,
and representativeness work in their owned paths; the scientific mainline still
awaits that evidence and the user's decision.

## 2026-10-30 — integrate W003 and M003 without selecting a new thesis

Root checks completed commits W 3c6546b and M f387566. It does not edit or rerun
their implementations. A separate script recalculates the three AutoVerus
direct tails from all retained source receipts: the slowest 58 of 3,566 consume
3.39888%, 3.33824%, and 3.31490% of their respective process-wall sums.
Each pass has 190 exit-zero, 3,359 exit-one, 17 exit-101, and no capture timeout.
This is a concrete counterexample to transferring the large Lean failure tail
to this source-replay point, not a CPU hardware comparison or whole-service
speedup bound. No cause is assigned to exit 101.

The six EPFL derived groups conserve all 68,932 labels: 28,145 valid and
40,787 invalid, including 1,314 wrong declarations. Publisher policy excludes
timeouts and infrastructure/precheck failures and does not release native
costs. This cannot measure an uncensored expensive-failure tail. APRIL's
1,835 test mutations and 20 budget-text records are diagnostic coverage, not
natural arrival or causal-cost observations. LNSym's 196 files contain 62
bv_decide, 153 native_decide and one direct ofReduceBool token; native timing
and transitive trust closure remain unmeasured. Exact pinned cards and the
LNSym README are checked. EPFL/APRIL web-tool fetches fail; bounded CLI reads
of the same primary revisions succeed.

M's final finite-count certificate is actually checked by stock Lean
4.9.0-rc1. Its computation theorem has no axioms; the predicate/cardinality
bridge uses only propext, Quot.sound and Classical.choice in printed closure.
The completed process takes 30.5811 s and 30.5467 CPU s, with 2,369,380,352-byte
leader high water and a 2,382,487,552-byte sampled own-tree peak. The 8.5572 s
extra warm declaration recheck is already inside the full process clock.
Root's independent integer enumeration confirms count 100 and sum 544,000;
this numeric agreement is not a second native proof check. All three earlier
unsuccessful versions remain in M's commit. This is a checked alternative proof
representation, not transparent acceptance of unchanged generated proofs,
automatic certified extraction, engine throughput, or a GPU improvement.

Root also verifies 684 direct ELF dependencies of the historical loaded
Linarith library. Its dependency closure includes NormNum and Linarith code;
the separate plain-CLI import maps only SDK shared libraries. The backends
must not be conflated or converted into an interpreted CPU fraction.
A check of M's 7,808 prepared-leader rows gives 7,682 accepted/rejected physical
attempts with median 470,599,680 bytes and recorded p99 977,809,408 bytes.
The separately observed parent peak is 3,614,543,872 bytes. Asynchronous peaks
and leader-only accounting do not supply a marginal memory reservation or
isolated COW gain.

The root calculation takes 0.952 s, peaks at 414,832 KiB, and launches no native
verifier. It is self-review of derived tables and retained receipts, not a new
full EPFL or LNSym source scan. Root uses CPUs 0–1 under its 4 GiB allocation.
Only Evaluation, citations, this evidence index and the root step records
change. The entire pre-Evaluation manuscript and all four RQs are preserved;
the scientific-mainline decision remains with the user after W/M evidence.


## 2026-10-30 — retained grid checks and fixed-trace memory envelopes (step0178)

Root resumes the existing pending step after the user's planned maintenance.
The original on-PVC crosscheck survives unchanged: zero native verifier runs,
0.421 s, 20,536 KiB process high water, CPUs 0–1. M e259a49's raw trace samples
are independently integrated using integer timestamps. Warm/engine covered spans
are 25,174.736735515/20,321.999420 s, sample counts 25,167/20,323, and maximum
sample gaps 1.031698211/1.003564 s. At 48 GiB, left-held exceedance durations
are 92.937076033/83.008805 s; the engine's fraction is larger (0.40847% versus
0.36917%) despite fewer absolute seconds. At 8/16/32 GiB the plotted fractions
are descriptive queries of these same traces, not changed-budget throughput,
acceptance, or a physical COW frontier. All original clocks remain separate.

Five actual stock-kernel grid rechecks are retained at M e259a49. Their subtotal
is 2.894191661 s inside the complete 11.006749094 s process clock. The three
origin rectangles overlap and have no satisfying antecedent; two offset blocks
include (5,401)/(401,5). No full-grid certificate or coverage bridge executes.
Linear full-grid projections of 402–517 s are neither measurements nor certified
upper bounds. The optimized C loop only enumerates/counts product matches; it
does not check the complete Lean predicate or construct a proof. These timings
cannot establish verified-checking or GPU speedup.

Pinned 4.9.0-rc1 source inspection distinguishes the ordinary decide frontend
from the extra warm declaration checks; the former reduces a Decidable instance
before kernel checking. That control is not the 4.34.1 decide +kernel census.
The public maxHeartbeats wrapper multiplies by 1,000, but allocation and kernel
check counters differ. The direct addDeclCore raw parameter 100,000,000 does
not establish equal remaining allowance to an original tactic invocation.
This is source review, not a new binary/version performance comparison.

The paper figure uses byte/JSON-equal retained input copies. The complete batch
ratio stays 1.23882×, with its single ordered shared-host pair, affinity/retry
and raw-artifact limitations. Warm preparation/retry accounting is clarified;
all 7,808 status aliases and 3,014 accepted IDs match, not all wire artifacts.
The four actual crate names/roles are reflected in Implementation. All text
before Implementation, the section hierarchy, four RQs and Related-work-to-end
remain unchanged. The scientific mainline remains pending W/M and user judgment.

After maintenance the same Workspace/PVC is readable and writable on phobos-vt;
root observes 61 GiB available at that time. Short self-owned TERM/KILL controls
both return errno 13 and naturally exit zero. No functioning signal watchdog,
security repair or native collection is claimed. Compiler/tool/output/cache
paths remain on the existing PVC outside the checkout. The actual complete
paper build and observed memory are recorded in this step's receipt, separately
from all earlier clocks. Reviews are same-thread self-review.


## 2026-10-30 — failure frequency versus tail concentration (step0179)

Root independently reaggregates the retained native-cell records for all three
direct AutoVerus passes, using fsum and the original per-pass process clocks.
Each pass has 3,566 unique complete candidates and no capture timeout. The
3,376 nonzero exits consume 607.419495/599.613263/600.950988 s out of
639.238028/631.214591/632.607252 s: 95.0224/94.9936/94.9959%.
Native JSON success=false occurs on 2,940 rows per pass and consumes
91.9664/91.9254/91.9163%. Each pass has 419 JSON-success/exit-one rows, costing
3.01568/3.02811/3.03927%, and 17 exit-101 rows without a JSON verdict. These
observations are not interchangeable acceptance classes or advance knowledge
of an inevitably failing candidate. The already reported 58-source upper tail
still contributes only 3.39888/3.33824/3.31490%.

Thus the valid lack of a highly concentrated timeout/resource tail does not
eliminate a large aggregate failed-candidate cost. No early rejection, budget
failure reuse, source-cost predictor or end-to-end speedup is established.
These clocks cannot be joined to publisher generation spans, other conditions
or hardware points. The paper adds this local interpretation; all scientific
framing, RQs, implementation and existing related work remain unchanged.

W ea41025's phase-A plan has 53 targets (42 probability targets), 12,785 internal
closure modules and 1,285 external import names. Time/RSS coefficients and
native peaks are uncalibrated; planning is not a completed native workload.
M 949622a's two tiny dependency controls succeed, but tactic Info/trace counts
are 18/28 and 6/9. Root separately counts all kinds and tactic-only nodes;
terms and punctuation must not be mislabeled tactic observations. No one-to-one
trace join, global critical path, parallel speedup or replay eligibility follows.
Their full 0.86654 s clock, leader high-water and sparse sample peak differ in
scope. The planned bounded 200-source point is not silently treated as executed.

Root runs zero native verifiers. Raw reanalysis output, initial all-kind counts,
refined tactic-only counts, exact frozen commits, root elapsed time and memory
are retained in step0179. Other lanes' sources and active captures remain
untouched. This is same-thread self-review, not independent audit.


## 2026-10-30 — profiler changes diagnostic execution (step0180)

Root independently streams M6f6f896's actual19,087,720-byte stdout, verifies all
400 unique source/mode units,200paired IDs, control-first order, raw flags,
durations, published CSV and completed native receipt. Current retained input
pairs contain equal source strings and matching IDs; historical assurance stays
the existing producer provenance. No new integrity/qualification protocol is added.

Control has31 no-error flags/19other errors/150budget interruptions; observe
has24/16/160. Seven flags become budget errors.80raw error-string arrays differ
before normalization, including those seven; these are not80semantic changes
or a full-service acceptance difference. hasErrors is only a frontend flag.
Body sums779.387741001s/80.075228226s give0.1027411954ratio, with different
curtailed execution. Body timers exclude subsequent extraction/serialization
and are already inside the complete1170.882824374s capture. CPU1142.78795s,
sampled own-tree peak8643375104bytes, native exit0 and retirement are distinct.
No clock joins the interrupted WAN attempt or supplies an invented phase cost.

The first root classifier misses '(kernel) deterministic timeout'; its failure
is retained. The refined analysis recognizes that actual native budget form
without altering native data or published labels. Literal marker counts can
overlap: kernel timeout68/68, public heartbeat144/157, recursion limit4/3.
These are not CPU fractions. Unrecorded raw heartbeat deltas stay unknown;
order/cache history is unbalanced. No multiplier, native work/span, production
pass-set loss or equal-work speedup follows.

The separate C prototype's raw tactics.jsonl contains16source markers and zero
tactic enter/exit callbacks. Completion is not engagement. Root launches no
native verifier, repairs no M hook and edits no W/M/O path. Scientific framing,
four RQs and citations stay fixed. Detailed evidence and self-review:step0180.


## 2026-10-30 — first released-module native costs and engaged timing hook (step0181)

Root independently reads W127ddc4's actual14 JSONL compiler records and logs,
checks all seven module/mode pairs against the CSV, exact resource fields and
zero source budget edits. Native Lean4.34.1/Mathlibd13f23b7 prerequisites are
prepared separately; these are olean-only module compiles, not full project
coverage, cold cache setup or original unlimited-budget costs.

Baseline/profile-only process sums are44.002840860/44.498820008s, CPU sums
44.044105/44.530084s. Difference0.495979148s (1.12715%) is descriptive for the
single baseline-first, cache-warm shared-node pair. All14exit0 and no sorry
warnings; no full service acceptance or transitive axiom audit follows.
The whole two-mode capture takes89.077571430s. Root checks all90 memory samples
and the7,982,608,384-byte sampled aggregate peak against the terminal record.
Compiler wait4 peaks reach8,013,123,584bytes, above the sampled aggregate peak:
short transients can be missed. Native memory8192MiB is not a hard RSS quota.
This4-of53target pilot cannot calibrate a full-source cost model or safe
eight-worker admission. Cumulative phase values overlap. The --profile point
cannot correct a different-version/cohort/option/budget trace.profiler run.

M3837eca supersedes the inactive dynamic hook with actual link-time callbacks.
Root directly parses stock/linked-off/linked-on cold stdout and receipts, verifies
identical source snapshots, all eight stock/comparator flag/error/InfoTree/raw-HB
comparisons, and reads the raw event file. The1,050entry/exit IDs match, their
per-thread parent stacks close correctly and durations are nonnegative.
Return tags0/1 are callback values, not counts of successful/failed candidates.
Four raw-HB deltas match13000/23351/4461/114090 across all paths; this is only
small-control qualification, not general transparency, full200 or production
parity, timing overhead, or a speculative-execution speedup.

The paper adds the qualified native pilot and replaces the inactive-hook-only
paragraph with this later limited result. All prior failure data stay in M
artifacts, step0180 and Git history. No historical run is relabeled or deleted.
Root launches no native verifier or other Agent, changes no W/M/O path, and
preserves all scientific framing/RQs and existing citations. Same-thread review.


## 2026-10-30 — native failure/dependency cache precedents (step0182)

[Detailed primary-source
audit](../step-0182-20261030T111939+0000/literature-20261030T111939+0000/report.md)
verifies that Lean4.9.0-rc1 and4.34.1 already cache negative typeclass queries. Native
full-state reuse also charges saved heartbeats approximately. Separately pinned current
upstream 0f852cc822d5 records observed query dependencies, normalizes eligible contexts
and persists eligible entries across commands; selected official changes date to
September/October2026. These current features are not silently attributed to either
measured release. Generic failure/read-set caching is therefore prior mechanism.
Arbitrary tactic failure replay, complete native semantics, workload opportunity and
incremental service benefit remain unresolved. No native benchmark or production feature
is run, and the paper mainline stays unchanged. Source-only details remain in the root
node because canonical background-related-work.md has foreign dirty work; it is not
overwritten or staged.


## 2026-10-30 — full-coverage memory retries and native outcome transitions (step0183)

Root independently reopens the full original warm/engine records: 7,808 unique
sources each, 7,860/7,850 physical attempts, and the warm sampled memory trace.
All 52 warm retry sources begin nonexclusive and finish exclusive. Of these,
41 remain resource_failure and 11 become timeout_error. Engine transitions are
41 preempted-to-resource_exhausted and one preempted-to-timeout. No accepted
proof is recovered by these retry sets. These are observed operational
classifications at one total48GiB point, not equivalent failures of a complete
goal/strategy state or a monotone per-call work certificate.

Root also recomputes all12 M retry sensitivity cells from the original engine
records and the read-only M function; fit-subset coverage, accepted-label
assumptions, preemption counts and clocks agree. No M source/output is changed.
At48GiB the zero-cleanup, full-coverage proxy is24832.4775s, rather than the
9759.43s drop-result proxy; hindsight admission is23163.71s. At8/16/32GiB,
full-coverage retry proxies are8681.98294/21156.68190/18423.31459s for the
respective7718/7766/7766fit subsets. All3014 frozen accepted labels remain by
assumption. Peak demand is flat/hindsight, physical work already includes
historical retries, and cleanup0/1/5s is assumed. These are not native throughput
or same-semantics results under changed budgets.

The first four-warm snapshot above3GiB per REPL has total15131496448bytes;
root reproduces all four resident values and its original timestamp. An8GiB
point cannot retain that snapshot, but a minimum warm footprint or marginal
COW saving does not follow. This is separate from leader wait4 or independent
peak subtraction.

The manuscript updates only the corresponding Evaluation method/limitations.
Scientific framing and all four RQs remain fixed. Detailed source checks and
actual build receipt are in tmp/build-and-evaluate/step-0183-20261030T112405+0000.


## 2026-10-30 — released kernel-checker fixture units (step0184)

Root independently verifies W6b95284's retained official pin and complete tree:
173files,12Lean sources/189413bytes,92JSON assets,90KIR fixtures/481125bytes.
All90raw JSON fixtures match published CSV size/role/parameter/tensor/grid
fields. Four retained implementation/README files equal the independently
retrieved official pinned source. No mirror supplies source evidence.

The67P0/23P1fixtures contain184/66concrete inputs. The emitter's five/one
specifications imply986positive property-wrapper obligations, not986executed
proofs or90native requests. Every native outcome remains not_run; no elapsed
time, acceptance or compiled axiom-closure claim is added.

The emitter generates positive KV.Holds wrappers using native_decide. Tool
FAIL means a certain modeled violation and can accompany a recognized Lean
refutation of that positive theorem; no accepted negation proof is implied.
The parser requires agreement among report, expected false-proposition errors
and compiler status; unrelated errors are tool failures. UNDECIDED may exit0.
Application verdict, compiler result and process exit must remain distinct.

The paper adds only the existing-scope workload/setup fact and pinned citation.
No competitor reproduction, runtime feature, new narrative or RQ change occurs.
Primary-source details and completed static checks/build follow in tmp/build-and-evaluate/step-0184-20261030T113046+0000.


## 2026-10-30 — completed prefixes do not qualify a full native comparison (step0185)

**Forward correction (step0186):** the partial analysis correctly checks
shard0, but its full200-pending assertion was stale. The complete matrix had
already finished at11:34:24UTC. Root observed that terminal at11:37:39UTC but
the chained publication still carried the earlier wording. The old receipt
and report are retained; the completed600-return reanalysis below replaces
that status assertion. Its hardcoded full200=false was not a live check.

Root directly parses M04aea15's three completed shard0 process outputs and
terminal receipts:100unique sources/300returns, equal source snapshots and
source order, all three process exits0/retired. For each linked-off and
linked-on comparator all100error flags, raw diagnostic arrays and InfoTrees
match stock, but33raw allocatedHeartbeatDelta values differ. Counter deltas
range from-24019597to41(off) and-48100884to66(on). These are raw-counter
differences, not33acceptance changes or proven budget flips. Their cause is
not established by this audit. Exact four-control heartbeat equality does
not qualify arbitrary cases; body-clock differences cannot be treated as
pure observation overhead or a production speedup.

Shard0 stock/off/on body wall sums729.881865/744.922177/742.865725s are inside
separate822.189537/836.245556/834.054916s complete process clocks. Full200/600
native comparison is pending, not inferred from this completed half. No
production candidate acceptance policy or whole dependency DAG follows.

Root also reparses W7e81ca8's frozen214record prefix:136EPFLreturns are53compiler
passes/71ordinary errors/12budget interruptions. Their623.799202s process-cost
sum is partitioned160.937229/303.183521/159.678453s. Budget cases account for
25.5977%of this returned-prefix cost only. Eight selected EPFL requests have
not returned, including the explicitly right-censored active invocation.
No censor-adjusted population weighting or conclusion that budgets dominate
or do not dominate full workloads is made. The seven wrong-declaration-labeled
sources that compile do not reproduce the publisher's complete judge and are
not counted as new false acceptances.

The manuscript is unchanged:these pending/intermediate diagnostics remain
provenance, rather than replacing complete evaluations. Three small earlier
untracked root-owned CI/client-control snapshots are preserved verbatim with
this step; their pending/historical fields are not relabeled as current proof.
Detailed checks:tmp/build-and-evaluate/step-0185-20261030T113532+0000.


## 2026-10-30 — complete200 native diagnostic differential (step0186)

Root now independently parses all six terminal cells and actual raw outputs:
600returns,200unique expected IDs, disjoint shards, equal within-shard captured
harness/order, all process exits0 and retired PID/birth identities. It checks
every recorded memory sample against each cell peak, and independently rebuilds
the two timing-on C event streams with per-thread parent stacks, source
ownership, clock monotonicity and exclusive CPU accounting.

All200flags/diagnostic arrays/InfoTrees match both comparators. Raw heartbeat
deltas differ63off/62on; exact budget semantics remains unqualified. The native
diagnostic classes are31no-error/19ordinary-error/150budget interruptions,
not the original service acceptance/sorry policy.

Stock/off/on body CPU827.301816/839.965435/838.669501s and body wall
827.525068/840.188200/838.914357s differ from full process wall sums
1023.378439/1029.925766/1028.648512s. One reversed order on disjoint shards
does not identify observer overhead or statistical variance. Maximum sampled
tree RSS8659439616bytes (~8.06GiB),largest sample gap1.014281s; no external
signal watchdog or hard RSS limit is claimed.

All200C trees close:7599entries/7599exits,400source boundary markers. Root
recomputes exclusive eqRefl CPU781.383626s (93.1694% of timing-on bodyCPU).
Per-source largest leaf sum812.899512s yields a conditional fixed-work,
indivisible-leaf upper bound1.03170132. It excludes new algorithms, splitting
inside native leaves, early termination and work removal; it is not a full
merge-safe DAG or production/global GPU Amdahl bound. The720.249942s leaf
and721.618421s body ofminif2f-4544 exceed its historical300s service cutoff,
so this diagnostic distribution cannot rescale the original7808point.

The paper updates only the corresponding Evaluation result/method paragraph.
All scientific framing, citations and four RQs remain fixed. Raw and failed
earlier observations, including step0185's status error, remain preserved.
Complete checks and build:tmp/build-and-evaluate/step-0186-20261030T114011+0000.
