# Evaluation: current evidence and open requirements

Updated2026-10-19. BOOTSTRAP remains unfrozen. All four RQs and the
Lean-first/SMT/RTX5090/OSDI-quality objective remain open. Source/code
qualification and publication are not new scientific contributions or
submission readiness.

The complete preceding chronological ledger is preserved
[verbatim as gzip](tmp/bootstrap/step-0010-20261014T133154+0000/evaluation-history-through-20261018-http-admission.md.gz)
and [readable at its original commit](https://github.com/yunwei37/gpu-smt/blob/ad01e18/docs/evaluation.md).
Decompress once for the original bytes; its relative links were authored
relative to docs/evaluation.md. Historical live-status and closure statements
retain their dates and do not override current evidence.
[Step record](tmp/bootstrap/step-0010-20261014T133154+0000/step-report.md)
and [outer self-audit](tmp/bootstrap/step-0010-20261014T133154+0000/outer-audit-report.md)
link original raw, failed, partial and superseded results.

## Current resource point

The latest user instruction replaces the earlier48GiB-per-worker policy
for new runs: [aggregate budget and qualification](../artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/README.md).
The sole old full collector is stopped. New acquisition uses total owned
RSS48GiB, at most2actual live REPLs and24GiB each, with one-second parent RSS
watchdog and explicit candidate-attributed resource failures. Real lowered-
threshold fault injection succeeds;24normal real-source paired qualification
is still running. One full acquisition follows only after qualification.
This changes the experiment resource point, not earlier raw data/clocks.
No Workspace/host/other-project configuration changes.

## Fixed research questions

| RQ, unchanged from the Initial Narrative | Evidence and unresolved promise |
|---|---|
|RQ1: How much expensive native preparation can real verification candidate streams share across independent jobs?|Real header/context associations and paid-preparation profiles exist. Competent warm reuse already removes most import work in measured cohorts. Multiple contexts/projects and consequential reusable cost in both Lean/SMT remain required.|
|RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?|Scoped native/kernel/artifact controls and closed constructor failures remain. Complete supported history/cancellation/resource/artifact equivalence and an effective mechanism remain required.|
|RQ3: How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?|Complete negative service/SMT comparisons and native runtime controls exist. The final equal-resource service frontier, causal ablations, complete resource coverage and repetitions remain open.|
|RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?|The selected CPU arithmetic composition improves one complete protocol; GPU constructors have scoped negative/mixed results. Strongest-service applicability, useful device supply/costs and generalization remain open.|

The [Initial Narrative](idea-story.md), user instructions and complete
Lean/SMT/service scope are preserved. Fork/COW, caching, native compilation,
ordinary solver portfolios and snapshots individually are established work.

## Original workloads and protocol boundaries

| Workload | Original population | Native producer/environment |
|---|---|---|
|GoedelWorkbook|29,750source files, distinct problem IDs|Migrated3c2afe6b;Lean4.27/db93fe16,Mathliba3a10db0|
|miniF2F|244tasks ×32candidates =7,808|Lean4.9.0-rc1/be6c4894|
|ProofNet|186tasks ×32candidates =5,952|Original4.9producer|
|AutoVerus|3,566original Rust attempts|Version-aligned Verus33269/Z34.12.5|

Released sources and four serial generator-output segments are not measured
verifier arrivals. Original bytes/order/options and all outcomes are retained.
Different SDKs, headers, collection epochs, algorithms, CPU eligibility,
observers and submission interfaces keep their own clocks.
Historical12GiB service captures remain separate; current user-required
captures/native children retain48GiB and record resource failures.
CPU affinity permits co-tenancy and does not establish exclusive resources.

## Current arithmetic result

The [complete reduced-diagnostic original1000pair](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/full1000-result-review.md)
takes810.713059s for adapted compiled Fast/hybrid+officialomega and
476.725600s for direct literal-power export with the CPU numerical portfolio:
1.700586x. Both return992complete/8rejected/0operational with matching
per-source verdicts and non-message fields;108message differences remain.
Eightqueues/fourCPU8--11/48GiB; optional process observer off in both.
Remaining candidate/RPC/omega/backend records are charged.
This is one shared-host fixed-order pair, not a global CPU optimum or GPU gain.
The control is an adapted frontend with common product reuse.

Direct source service spans regress for169sources, including63of70IDs that
regress in every earlier instrumented observation. Current medians are
2.729/1.559s and p99 44.212/31.821s. All sources remain; spans include waiting
and overlap. Whole gain does not establish a per-candidate latency guarantee,
isolated CPU savings or the cause of regressions.

[Source-joined regression costs](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-without-diagnostics/regression-cost-result-review.md)
show82of169current regressions, including20of63persistent ones, have no
recorded large numeric race. Completed HiGHS solver time in the169is1.622s;
native/cancelled/small paths and Lean stages are outside that counter.
This does not establish all-LP cost or fallback causality. It provides no
evidence for attributing every regression to a pathological external LP.

[Three earlier instrumented observations](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-whole-repetitions/result-review.md)
have native/direct629.48/350.68,615.33/348.91,637.27/356.54s; ratio of sums1.78205x.
They retain diagnostic construction and sampling on CPU4--7.
They are not pooled with the corrected pair.
[Component controls](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export/full1000-result-review.md)
separate numerical backend, direct proof path and literal-power coverage;
the total gain is not ordinary compilation or power support alone.

The criterion uses the better valid CPU/GPU result on the original1000.
The corrected CPU observation exceeds1.5x and justifies continuation;
it does not complete the research goal or establish OSDI-level novelty.
[Current whole-Goedel matrix](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-full29750/plan.md)
uses the frozen corrected implementation on all29,750originals.
Its actual process/terminals determine progress. The
[older29,750capture](../artifacts/linarith-oracle-2026-10-17/gpu-stage/full29750-generalization/)
uses another implementation and cannot generalize the current method.

## Formal populations and standard service comparison

The [4.9adapter qualification](../artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/result-review.md)
matches all64native responses,44complete/20reject, with88direct certificates.
Its [full ProofNet component comparison](../artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9/full-populations/proofnet-result-review.md)
returns all5,952: stock1151.883s, native1160.922s, direct1178.934s.
Every condition has413complete/5523reject/12operational/4incomplete,
with exact verdict/non-message parity. Direct is2.35%slower.
The module-loaded stock path elaborates explicit arguments before fallback;
it is not pristine Mathlib. The native mode is not the full4.27Fast frontend.
miniF2F remains acquiring under the same declared protocol.

The [official Kimina HTTP plan](../artifacts/linarith-oracle-2026-10-17/kimina-http/plan.md)
tests transfer beyond native-array collection. Unchanged upstream application/
SDK fb2393de, same declared4.27kernel/GC/native-loader REPL, compiled stock,
strong Fast/hybrid+omega and current Power at8source concurrency/fourCPU20--23.
The repaired first64preflight closes stock216.998s/native82.459s/Power40.417s
complete lifecycles, each63valid/1Leanerror with matching status/non-message
responses. Two failed dependency attempts remain; Power's valid run replaces
only its zero-input startup failure. This is one selected preflight, not a
population result. The completed3rotated1000source blocks are reported below.
[Preflight and repair scopes](../artifacts/linarith-oracle-2026-10-17/kimina-http/preflight-result-review.md).
This is not a new prepared-state mechanism or a GPU result.

The [complete default-tiered Goedel control](../artifacts/linarith-oracle-2026-10-17/kimina-http/reference-engine/full1000-result-review.md)
now returns all 1,000 originals: 1018.229 s native versus 492.981 s Power,
2.065455× whole; 1004.574/479.541 s warm, 2.094865×. Both return
992 valid/eight rejected, zero operational failures, matching per-source
statuses/non-message fields and 112 message-only differences. All descendants
retire. This single shared-host four-CPU16–19 epoch closes the default-engine
omission. It does not replace the faster measured hybrid comparison to
inflate the headline, pool epochs or establish global CPU optimality.

[The complete official DSV2/Farkas reference-corpus comparison](../artifacts/linarith-oracle-2026-10-17/kimina-dsv2/result-review.md)
contains all 438 different-prover proof outputs in three alternating pairs.
Both methods use the same retained Lean 4.27 environment; the adapted
compiled reference selects upstream default tiered exact search.
Aggregate whole time is 1264.966/1194.906 s native/Power, **1.058632×**;
warm time is 1223.849/1153.172 s, **1.061289×**. Each cell returns
263 valid, 175 Lean errors and zero operational failures. Source statuses
and non-message fields agree across all six cells, with one warning-only
difference between methods. Individual whole ratios span 1.049900–1.064890,
an observed range rather than a confidence interval.
All sources appear in the HTTP/body projection and latency figure, including
Lean errors. Completed HTTP attempt latency excludes pre-dispatch SDK waiting;
SDK body wall includes GC/IPC and concurrent sums overlap. These are not
pure-LP CPU or removable whole-wall fractions. This is producer-output
transfer on overlapping miniF2F tasks, not upstream 4.31 replication or
evidence that all proofs inherit the selected Goedel gain.
The historical 2234.69 s run still lacks complete matched phase stamps.

The [complete original Goedel HTTP matrix](../artifacts/linarith-oracle-2026-10-17/kimina-http/full-matrix-result-review.md)
now contains all nine1000-source cells. Strong-native/Power whole times are
857.111/534.483s and812.073/456.819s for the first two intact pairs:
1.603628× and1.777670×; ratio of sums1.683831×, warm1.702017×.
Every cell has992genuinecomplete/eight rejected/zero operational, with exact
per-source verdict/non-message parity and108message differences per pair.
Third-pair Power491.129s precedes container interruption, while stock2564.311s
and native773.372s are recovered; expose its descriptive1.574682ratio
without an uninterrupted three-repeat aggregate or new confidence interval.
PublicCSVcontains9000source observations; the CDFincludes all6000strong-native/
Power observations. Power body spans regress for208/152/245sources.
Native-ranked slowest1%body sums are993.892/650.805,949.659/562.366 and
901.897/595.935s, native/Power, overlapping spans rather than whole-wall
savings. All48GiB/CPU/retirement receipts and raw messages remain.
The [first-block checkpoint](../artifacts/linarith-oracle-2026-10-17/kimina-http/first-block-result-review.md)
remains historical. This closes acquisition, not GPU/novelty/all-RQ evidence.


The [official SHRED closing-certificate executor](../artifacts/linarith-oracle-2026-10-17/shred-closing/README.md)
is now actually qualified: first original miniF2F32, 28 complete/four
rejected in both modes, four hits and zero timeouts/process errors.
The matched service integration additionally preserves all statuses on
miniF2F50 and a positive-control ProofNet68 cohort. These are functional
subsets; opaque env handles/cache messages differ. Native parsing costs
roughly7s and makes SHRED slower in those tiny batches when charged.
The [complete ProofNet official-HTTP pair](../artifacts/linarith-oracle-2026-10-17/shred-closing/proofnet-full-result-review.md)
returns all5952originals in each method: native356.367363s, SHRED373.219730s,
including preprocessing and retirement,4.7289%more elapsed.
Both genuinely complete413same sources; outcomes are5534/5514rejected,
4/24incomplete and1/1operational. Twenty rejected-to-incomplete changes
all carry cache-hit messages. Raw SDK valid417/437 is not a complete-proof
count. Both source5879failures preserve three HTTP500JSON-decode attempts.
All owned descendants retire;5743opaque-env and5946raw-reply differences remain.
This as-integrated prior-method control is not protocol-transparent reuse,
a global CPU optimum or a whole-family negative conclusion.

Cost-weighted recorded generation sums801.745555s wall across overlapping
requests, not removable CPU/whole wall;1333of1653captures come from ultimately
noncomplete sources. Hash-bucket repeated-generation proxy64.676644s
shrinks to6.031379s when restricted to sources complete in both methods.
Both views remain; hashes, missing failed-generator timings and overlap
preclude a scheduling/Amdahl bound. Counts alone do not admit a new cache.
A [457-source existing-error pilot](../artifacts/linarith-oracle-2026-10-17/error-work-control/preflight-result-review.md)
closes119.999495/63.221143s native/guard. Eleven actual prior-error skips,
413samecomplete/4sameincomplete; one operational-to-rejected change remains.
This selected diagnostic is not representative population speed or novelty.

On2026-10-19the Workspace Pod was replaced, interrupting all original
collectors. Node/SSH/k3s-agent/5090 remain healthy; the retained PVC and
completed cells survive. Lost temporary aliases are restored to their
existing retained dependency trees. Original unfinished cells remain
interrupted partials, never spliced into complete wall clocks. The miniF2F
HTTP pair recovery uses fresh outputs; completed ProofNet is not rerun.
A second container OOMKilled at01:20Z interrupts the first recovery; Goedel
also exposes a missing Farkas alias. Both faults and invalid all-operational
startup captures remain. The alias is repaired and real24-source native/
oracle qualification passes22complete/2same rejects. Recover unfinished
collectors sequentially with unchanged within-cell resources, not another
simultaneous restart or a new quota.
[Recovery evidence](../artifacts/linarith-oracle-2026-10-17/workspace-interruption-20261019/README.md).
No full speed or new contribution is inferred from hit counts or partial data.

The miniF2F eight-source HTTP capture suffers a further verified global OOM
at 2026-10-19T03:13:19Z. Kernel records eight substantial REPLs totaling
120,538,700 KiB (114.95 GiB) anonymous RSS; every recorded individual
process remains below the required 48 GiB address-space ceiling.
Existing container OOM-group behavior kills the whole experiment group.
The incomplete attempt retains 2,428 distinct requested IDs, 2,420 IDs
with responses and eight pending sources, including warm preparation.
These are partial observations, not a completed corpus result.

The [recovery plan and kernel evidence](../artifacts/linarith-oracle-2026-10-17/shred-closing/memory-recovery-20261019/plan.md)
restart the same original native/SHRED comparison at **two outstanding
sources in both methods**, four CPUs 4–7 and 48 GiB per process.
This is a new resource point; no eight-source or pre/post-OOM timings are
pooled. The official service, native code, source order and timeout stay the
same. Only the finite capture's request/warm width changes; default width
eight and all server/host settings remain. Matched real-source preflight
precedes the full 7,808-source pair. Full results remain pending.
The infrastructure incident is recorded in server-manage commit03bd8433.


The subsequent two-source service capture is interrupted by an observed
Rich regex-highlighting stall on the Python event-loop thread, not another
inferred global OOM. Its raw log separately records214LimitOverrunError
occurrences from default asyncio.readline limits. The
[declared transport/logging repair](../artifacts/linarith-oracle-2026-10-17/shred-closing/stream-recovery-20261019/README.md)
changes only long-line framing and heuristic highlighting in the retained
Kimina application. Exact before/after sources, patch, license, real stack,
retired owner processes and closed partial bytes remain. The protocol test
preserves a200050-byte reply and following frames at the unchanged64KiB
default limit; that is dependency qualification, not a verification speedup.
The [closed54-source paired qualification](../artifacts/linarith-oracle-2026-10-17/shred-closing/stream-recovery-20261019/result-review.md)
includes previous HTTP failures and source2518. Both return28complete/
23rejected/3operational, zero status/outcome differences;16opaque-env and32raw
reply differences remain. The same three failed IDs each retain threeHTTP500
attempts; causes remain unassigned, not relabeled ordinary Lean rejection.
Each has62HTTPrequests/62responses, observed overlap2and no line-limit error,
with all owned descendants retired. Largest real replies906/1267bytes do
not themselves test the >64KiB frame. The whole7808-source pair starts once
at06:40Zin fresh outputs using the same repaired application in both arms;
old/new epochs are not pooled. Its acquisition remains incomplete. The finite
sequence joins actual qualification via pidfd without goal polling, then
continues admitted unfinished methods; no new Agent or scheduler is used.

## Prefix/preparation evidence and previous controls

Complete [miniF2F exact](../artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/exact-result-review.md)
and [unit](../artifacts/linarith-oracle-2026-10-17/formal-default/minif2f/unit-result-review.md)
captures take41738.63/40943.77s versus28673.00s nativebatch.
All2992native-complete IDs survive; operational outcomes differ319vs326.
Parsed unit-prefix potential13.44%of edges is not time saved.
Complete [ProofNet prefix](../artifacts/linarith-oracle-2026-10-17/formal-default/proofnet/result-review.md)
takes1127.28s batch versus2502.01/2479.03s exact/unit.
All413native-complete survive; incomplete/operational changes preclude a
validated transparent speed ratio. Its18.38%edge potential is not CPU saving.
These source-native executors use SHRED's parser, not its complete published
workflow. At the pinned revision SHRED exposes CLI profiling and paired
closing-certificate execution; a standalone HTTP replacement service is not
its declared interface. Earlier prefix timings do not characterize that
separate certificate executor or the official Kimina HTTP service.

[Paid preparation](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-039/result-review.md)
is modest after competent warm reuse at the measured boundaries:
ProofNet import-preparation CPU is about0.81--0.85%of observed native lifetime,
and SMT paid parent readiness is only seconds per complete condition.
These scoped CPU counters are not full-wall bounds or zero initialization cost.
One Goedel import header and many header hits cannot establish multi-context
placement novelty. Complete CPU/native compilation controls and their remaining
profile scopes stay in the archived ledger; ordinary compilation gains do not
supply the proposed systems contribution.

## GPU evidence and opportunity limits

No useful additional full-verification GPU gain over the strongest current CPU
composition is demonstrated. [The corrected additive portfolio](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio/result-review.md)
retains native hybrid plus HiGHS: CPU38.022s versus CPU+GPU39.327s on64originals,
3.43%more elapsed, matching full responses. Extra processes/repair/contention
are charged; racing does not provide a strict no-slowdown guarantee.
[Ready-goal GPU qualification](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/additive-device/result-review.md)
on15originals gives79.931s CPU/79.593s GPU, but zero GPU answers win.
Twoactual groups/three device models include cross-candidate work;
the0.42%clock difference does not demonstrate device benefit.

Earlier complete1000GPU trials remain version-specific:
3374.15s phase-I with8operational failures; a later pooled composition
1020.12s warm/1036.25s cold versus its own1237.37s native reference.
They are not the current Power/strongest-CPU comparison.
The5090is shared using time slicing; sharing itself is not established as
the cause of any slowdown. No unprofitable kernel/allocator/thread grid runs.

[Complete current component cost accounting](../artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-omega-cost/full1000-result-review.md)
retains all successful/failed numerical branches, cancelled-childCPU,
actual matrix shapes, request overlap and matched1%/10%tails.
The historical2234.69s primary lacks those phase stamps and cannot be recovered
by rescaling later measurements. Conditional ideal-capacity ratios1.46068,
1.53960 and1.51182 use an already-oracle-containing component reference
and hold workload/path/rate assumptions fixed. They are not universal bounds.
Wall unions and overlapped leaf CPU cannot be inserted blindly into1/(1-f).
The user's broad negative-GPU closure condition is not proven.

Earlier20.9xresident metadata and14.6xwarmREPL results are scoped proxies.
Defeq1.067--1.090x is conditional sensitivity, not measured whole acceleration.
The arena/reclamation constructor reaches higher prospective coverage but
takes1052s and remains closed; body CPU coverage is not removable wall time.
All original failed and partial results remain in the archive and raw folders.

## Closed constructors, current artifact and review

The user-closed native runtime branch(E038) remains stopped, preserving
known-slow v1 partials. No full runtime matrix restarts without beneficial
matching preflight. The slow reclamation interpreter(E040), old shared-process
placement and unsupported narrow GPU constructors remain closed.
[Disposition](tmp/bootstrap/step-0010-20261014T133154+0000/route-closure-20261017T0127/result.md)
and [earlier negative routes](tmp/bootstrap/step-0010-20261014T133154+0000/negative-routes-disposition-20261015.md)
retain their exact evidence; closing constructors does not answer every RQ.

Complete repaired SMT stock/branch/logical comparisons retain42,792executions;
branch is28.84--37.91%slower, with no stock-relative memory saving.
[Original source/artifact comparisons](../artifacts/autoverus-native-2026-10-09/experiment025/full-registry-repaired1-result-review.md)
remain separate from the older31status-change epoch. No generic prefix
reconstruction transparency or universal state-isolation win is claimed.

[Buildable arithmetic source](../bench/lean-native/linarith-oracle/reproduction/README.md)
includes exact measured Rust/Lean bodies, locked dependencies and provenance.
Fresh source build and real64source CLI qualification return63complete/1same
rejection with actual LP engagement. It is functional reproduction, not
a new performance score or a clean-machine dependency installer.
The [paper](paper/main.tex), manuscript PDF, scope limitations and current
step remain unfinished at the complete scientific objective.
All current implementation/review is by this thread. Self-review does not
substitute for independent audit or establish venue acceptance.
