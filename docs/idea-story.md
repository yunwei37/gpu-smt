# Idea story

## Initial Narrative — 2026-10-07

This section records the initial scientific disposition of the expanded research effort and remains intact. It is a hypothesis and evaluation contract under BOOTSTRAP, not a claim that the intended system already exists or achieves its performance goals.

**Problem and stakes.** Verification is increasingly performed on related candidate programs and proofs. Independent candidates require isolation, but preparing their verifier state repeatedly can consume CPU, memory and latency. The project studies real Lean proof checking and SMT-backed systems verification, preserving accepted, rejected, incomplete and resource-limited outcomes. The human requests acceleration, meaningful benchmarks, GPU exploration and an OSDI-level complete paper effort.

**Challenged belief.** A warm mutable session or result cache captures all useful cross-job reuse. The competing position is credible: established Lean REPL environments already remove cold imports, and the retained VeruSAGE sample has sparse exact duplicates and modest ordered-prefix bytes. The central question is whether preserving preparation while separating candidate execution histories changes the attainable latency/throughput/memory frontier beyond competent warm services.

**Central insight and thesis.** Reusable verification state is a native execution prefix, not merely a set of logically equivalent assertions. Reconstructing an assertion-equivalent incremental context can alter solver mode, heuristic history or resource accounting. Immutable prepared states with disposable native branches separate preparation reuse from candidate interference. The thesis is that this separation enables consequential parallel verification under bounded memory, with correctness defined by native verifier behavior rather than accepted-job counts.

**System and method.** The intended system prepares exact ordered native prefixes at supported quiescent boundaries, preserves configuration and solver resource state, and creates independent branches for candidate suffixes. Copy-on-write sharing reduces replicated preparation where feasible; bounded placement and branch lifetimes control memory and cancellation. Unsupported runtime or protocol cases execute on the native baseline. A stock library or frontend hook is distinguished from an unmodified executable. No arbitrary multithreaded fork is assumed safe. GPU work is selected from measured remaining checker costs and evaluated with preparation, transfers, fallback and the best CPU method included.

**Intended contributions.** A source-grounded characterization of preparation sharing in real candidate streams; a native-state isolation mechanism and its observable-behavior argument; a bounded service implementation with useful latency/throughput/memory tradeoffs against established reuse; and a causal assessment of heterogeneous checking after warm preparation. Fork/COW, REPL backtracking, result caching, integer-ID arrays and cached metadata computation are prior mechanisms, not individual novelty claims. Novelty must survive closest-work comparisons without a coined name.

**Scope.** Lean/Mathlib and Verus/SMT verification remain in scope. The initial backend anchors are the official Lean kernel/community REPL and version-aligned Verus with stock Z3. Public source-native proof/candidate streams supply actual work, including failures. Published proofs with mutations are correctness controls, not real generated candidate traffic. Arbitrary backend transparency, semantic canonicalization, full GPU Lean checking and universal acceleration are not assumed. RTX 5090 is the only GPU family used. Final data are produced from a frozen evaluated version; prior inspected measurements remain preliminary evidence.

**Paper research questions.**

- RQ1: How much expensive native preparation can real verification candidate streams share across independent jobs?
- RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?
- RQ3: How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?
- RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

**Evaluation promise.** Use actual ordered proof/program attempts from public Lean and SMT-backed systems-verification workloads; retain all outcomes, context availability and stage boundaries. Cover multiple contexts/projects in both families and unrelated-work controls. Compare the strongest runnable established warm services with result caching, matched native fresh execution as a control, and branch execution; baseline families remain subject to bootstrap literature pressure. Include candidate parsing/elaboration/construction, verifier checks, shared preparation, process/device setup, transport, queueing, replacement and teardown in end-to-end measurements. Report latency distributions, throughput, memory/PSS, CPU work, concurrency and offered-load scaling, and uncertainty across whole-run repetitions. Explain causal effects through preparation depth, COW mutation, state placement and lifecycle ablations. Test exact per-input decisions, requested models/cores/proofs where applicable, incomplete proof handling, timeout/cancellation and scope/history regressions. Evaluate GPU opportunities by measured expensive dynamic work and equal boundaries against tuned CPU checkers, allowing a useful negative GPU conclusion. All four RQs remain unanswered by final evidence.

## Current frontier

BOOTSTRAP step0010 remains unfrozen and all four RQs remain open. The complete
Initial Narrative and accepted evolution below are preserved. Completed evidence
and interface checkpoints are now published on main, under the
user's explicit request to stop withholding completed work until the whole
research effort finishes. Publication is not an independent-review verdict,
a final RQ answer or an OSDI acceptance claim.

The user now authorizes parallel OMP work with file ownership: README, docs,
paper and experiment scripts are delegated; the root owns Lean/GPU implementation,
scientific disposition and final integration/publication. The original Codex
author session remains retained/stopped. A focused independent opportunity
review is separately dispatched without implementation ownership. Neither a
live process nor an issued prompt establishes that specialist work or an audit
has completed.

Completed negative implementations stay closed. Complete native6 ProofNet
device comparisons, shared-process placement and repaired SMT prefix branching
do not demonstrate their claimed acceleration. Their
[published negative disposition](tmp/bootstrap/step-0010-20261014T133154+0000/negative-routes-disposition-20261015.md)
retains the measurements and scope rather than continuing small variants.
The original Lean/SMT/service/device research ambition is unchanged.

Native compilation, native arithmetic and invocation-local product reuse supply
competent CPU controls. They are not the proposed systems novelty. Completed
CPU cells and per-input rows are now
[published](tmp/bootstrap/step-0010-20261014T133154+0000/completed-cpu-cells-20261016/README.md);
unfinished original acquisitions remain running without additional tuning grids.
Their exact current results belong in evaluation, not this narrative.

E033 completes all29,750 native sources and publishes its original capture,
345 thread observations and analysis. Entry metavariable flags do not establish
independent work or GPU coverage. E034's native batch interface builds and
matches two accepted/rejected native fallback smoke cases, with provider
unlinked and no device engagement. The
[existing-data opportunity analysis](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-034/performance-ceiling-and-admission.md)
distinguishes inclusive35% defeq CPU,23.16% argument-comparison CPU and a separate
23.61% observer descriptor. Conditional1.067–1.090x calculations are sensitivity
scenarios, not rigorous end-to-end bounds. The root suspends narrow GPU-backend
implementation pending a credible independent-work and complete-cost opportunity.

A new [source/cohort admission review](tmp/bootstrap/step-0010-20261014T133154+0000/literature-20261016T0845/report.md)
finds one actual import header across all29,750Goedel attempts; native logs
partition them into29,690 started-worker reuses and60 header preparations.
The mini cohort has7,790 matching imported headers and18 empty headers.
Counts do not establish saved cost. Generic multi-context eviction/placement
cannot be a measured new contribution on a single-root cohort; existing
Kimina, native snapshots and AXLE already establish the individual mechanisms.

The four recovered serial generator-output segments cover all13,760 original
ProofNet/miniF2F attempts, but official submission consumes a finished batch.
These are not measured verifier arrivals or multi-producer feedback traffic.
Preparation expense, equal-resource complete service frontiers, native artifact/
history/cancellation behavior and strongest compatible competitors remain
load-bearing evidence requirements. Existing services, caches and snapshots
already provide the individual reuse mechanisms; no surviving novel system
contribution has yet been demonstrated. Ordinary CPU gains cannot fill that gap.

Healthy acquisitions do not justify goal turns that only poll row counts.
Advance substantive mainline work and collect each original acquisition on
completion. The complete paper, causal ablations, limitations and fresh
independent step/paper audits remain required. The
[step report](tmp/bootstrap/step-0010-20261014T133154+0000/step-report.md),
[implementation](implementation.md) and [evaluation](evaluation.md) own detailed
evidence. The previous frontier is preserved in
[the dated archive](tmp/bootstrap/step-0010-20261014T133154+0000/idea-frontier-before-published-checkpoints-20261016.md).
This is a status and admission update; it changes no accepted thesis, RQ meaning,
scope or evaluation promise.


A fresh independent plan review closes the proposed standalone reached-argument
CPU census before execution: its missing fraction alone would not admit a
concrete independent algorithm or a differentiated system. [E035 disposition](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-035/disposition.md)
preserves the uncertainty rather than inventing a negative cost bound.
The [formal Arena protocol/source assessment](tmp/bootstrap/step-0010-20261014T133154+0000/literature-20261016T1025/report.md)
identifies complete post-export declaration checking as a candidate device
boundary with strong already-parallel CPU competitors. No algorithm, backend,
new performance result or novel contribution is admitted by that observation.
It neither transfers to source-verification clocks nor replaces the original
Lean/SMT service and four-RQ evidence requirements.

The [2026-10-16 full manuscript checkpoint](tmp/bootstrap/step-0010-20261014T133154+0000/iter-refine-writing-20261016T1745/round-11-meaning-preservation.md) integrates the published evidence and actual native-runtime alternative into the current paper. Process and runtime constructors, measured and finite-only versions, and strongest compatible baselines remain distinct. The full writing cycle and source-preservation audit do not establish new systems novelty, close an RQ or change this scientific contract. Current detailed data remain in [evaluation](evaluation.md).

The complete [E039 paid-preparation characterization](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-039/result.md) now measures actual request-driven import preparation on all5952ProofNet candidates×3 and reuses complete SMT phase costs. Observed import preparation is modest after competent reuse at this exact boundary; hits/header recurrence cannot establish expensive work saved. This is supporting RQ1 evidence, not a new scientific contract, a full-wall/GPU bound, complete RQ answer or reason to reopen closed fork variants. Broader contexts, strong native frontier and differentiated contribution remain open.

The complete [E040reclamation setup](tmp/bootstrap/step-0010-20261014T133154+0000/experiment-040/result.md) closes this concrete host constructor without a device port: prospective paid support improves, but complete overhead and expensive step-limit failures remain adverse. This is a dependency decision, not a new scientific claim or RQanswer; all native checks remain and independent audit is missing. Do not turn same-capacity GC into systems novelty or another tuning grid.

## Narrative evolution

### 2026-10-07: established native branching enters the competing position

The Initial Narrative challenged warm mutable sessions/result caching as the competing answer. The immediately preceding narrative was that initial disposition. Root now rejects the exclusive mutable-session framing: Kimina reuses immutable roots with candidate pruning, stock Lean supports serialized incremental snapshots, and Snapshot-DSP shares prepared state across independent parallel tactics. The chosen comparison explicitly includes native logical/serialized branching and bounded warm/cache services. RQ meanings and Lean/SMT/GPU scope remain intact. This is stronger and more faithful than both initial and previous framing because acceleration must survive current native reuse, rather than a cold or accumulating worker strawman. Evidence: [complete literature report](tmp/bootstrap/step-0001-20261007T212930+0000/literature-20261007T213700+0000/report.md), primary code/papers in its canonical map, and root E5 disposition in the [step audit record](tmp/bootstrap/step-0001-20261007T212930+0000/step-report.md). No process-cloning novelty claim is accepted. Revisit before freeze if no behavior/resource advantage survives these strong alternatives or a safe native boundary fails. This evolution preserves the complete Initial Narrative above.

Current E100 evidence bounds the current GPU fragment and finite-retirement gains; it does not alter the Initial Narrative or RQs. Complete CPU acquisition continues, useful GPU implementation and full service/SMT evidence remain open. No WRITE, final result review, outer audit, publication or acceptance has completed.


E101 isolated explicit-continuation/closure implementation now has compiled CPU/PTX identities and complete373retained real-graph CPU error analysis:5330/14591exports,57wholegraphs,73/399exact matchednative locals. Oldeager analysis remains168exports/0wholegraphs/2locals. AllareCPU controls, notGPUperformance/coverage orfullkernelproof. PublicWHNF ispartial; nativeMeta bridge remains absent. OfficialCPU fallback/trustedmetadata remainrequired. Rootimplementsresidentactualdevicepathseparatelywithouttouchingfrozenacquisition orresettingE021'sthreeattempts. Mainformal/fullservice/SMT/fourRQ/paperambition remainsopen. [Implementation limits](../artifacts/lean-gpu-checking-2026-10-13/closure-development-20261013/report.md) and E101completecommands/raw preserveprovenance.


E103 whole ProofNet WHNF diagnostic completed all5952 original sources, normalexit0/basic0differences,585.2256s. Raw and reconstruction are experiment015/whnf-full1/whole-counter-analysis.json. Four of five worker sessions have terminal counter dumps; the original operational worker is censored. Observed exclusiveCPU281.3783s in the cache-inadmissible/level-mvar union versus2.5654s cache-admissible cannot be whole CPU shares or GPU bounds: preparation inheritance, missing failed work, profiling overhead and duplicate rechecks remain. Native source proves cache-disabled modes can still be deterministic, so that union does not identify GPU support. E104/E105 classified repair completes all5952 original inputs/basic0differences,5951matched frontend intervals and one censored original5879, fresh whnf-classified-full1/reanalysis. Closed/no-custom scopes contribute97.5767s observed exclusiveCPU; the instances/cache-disabled/no-variable mask alone contributes82.9134s. This resolves the old overconservative cache-derived grouping, not actual GPU coverage or a whole CPU/GPU speedup bound. Native preparation inheritance, instrumentation/non-atomic deltas and failed/open work remain limits. A substantive native reduction/readback/provider integration is underway separately; its current compiled CPU/PTX controls are not device execution. Original queue41070/E015mini full5 child57992 on4–7, E01813440 and E0085450 remain protected. All8 E021 ProofNet CPU cells are complete; the original24 whole heterogeneous matrix remains incomplete. Native reduction/readback bridge implementation is isolated CPU control only until actual complete device integration and measurements.


E107 implementation/evidence update changes noInitialNarrative/RQ/acceptedconcept. Native3's realGPUpreflight1 completes44basic-matched outcomes,16usefulnativeoperationreturns onincompleteProof2913, minizero. Wholeformal32conditioncomparison againststrongwarm/snapshot-cache isadmitted; all16ProofNetcellsrequested, mini16afterheavydependency, nofulldataorGPUgainyet. Complete373graphactualcomponentcost isnegative, retainedratherthanhidden. Offlineprimarymeans/resources are notofferedload/service evidence; theoriginalRQ3promise drivesactualstreaming-interfacequalification. Fullservice/SMT/fourRQ/novelty/paperambition stayslargerthannarrowbeta orCOWprimitive; fullwriting/auditsremainrequired.


E110–E111 implementation/evidence update changes no Initial Narrative or accepted scientific concept. E022 full-cohort native3 CPU/GPU failures invalidate its performance comparisons; actual kernel-rejection exception ABI conflict is repaired in native4, all37 repair rows basic-match, old invalid/partial and valid stock data retained. Fresh matched final16 ProofNet request is ready. RQ3 implementation now separates real disposable candidate branches from unlimited warm sharing; full60-cell offered-load plan is independently reviewed and its first actual preflight started. No new performance/RQ/novelty conclusion follows. Complete main formal/service/SMT/GPU/writing/audits remain the target.


E113 accepts AXLE as additional same-claim pressure for generic isolated preloaded Lean serving, with SOCK/SEUSS/native snapshots already covering reuse mechanisms. This changes the literature/evidence frontier, not the Initial Narrative, RQ meanings or ambitious full verification goal. Complete source-native resource/history/service evidence must establish any surviving distinction; the active E023 full capture and ready repaired E022 request have not yet done so. Current node and literature report preserve limitations and root disposition; no first-isolated-service or OSDI acceptance claim is introduced.


E114 real complete5952-source service observations at one low-load pair show worse branch arrival latency than shared warm while whole time follows offered arrivals; strongest snapshot comparison and complete60-cell scope remain pending. Figures are staged raw-derived evidence, not final contribution/RQ results. This is an implementation/evidence boundary update, not a change to the Initial Narrative or full Lean/SMT/GPU service promise.
