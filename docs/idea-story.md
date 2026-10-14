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

BOOTSTRAP step0007 REVIEW_GATE after complete E028 and serial root WRITE, scientific contract unfrozen and all four
RQs open. Initial Narrative and accepted evolution below remain intact.
The desktop root implements directly under the human request; the original
native author session is retained/stopped, with no delegated new author.

Native6 complete16ProofNet/95232source outcomes preserves all paired basic
results, but GPU loses1.74%,3.64%,1.58% to fastest nativeCPU (mean2.32%).
The full16miniF2F run failed in its native warm baseline: active source663
allocated about95GiB and host global OOM killed the benchmark before GPU cells.
The former Workspace Pod was then replaced by the same ReplicaSet/PVC; its
deletion actor is unknown. Raw/partial/failed data and all original cohort scope
are retained. Former CPU captures are interrupted, not active; E018 resumed after restoring its dependency alias, then root closed further
repetitions of that invalid/slower version after complete first-primary review. No memory cap,
source exclusion, blind mini retry or delegated author has been introduced.

E026 complete native diagnostic5952source stream now matches all original basic
outcomes. Common class/structure projection reports recur across distinct sources.
Reused classified source deltas find most observed native WHNF-miss CPU has
context flags. These are supporting selection evidence, not whole-time fractions,
GPU eligibility or speedup. Current official dependency-aware instance caching
is prior art and a necessary competing mechanism, not proposed novelty.

E027 exact projection cost rejects per-operation projection offload as the next
mechanism. E028 conservative closed-mode CPU cache completes all8cells and
47616original outcomes. Its paired wall reductions7.39%,-0.06%,-1.03% do not
establish stable acceleration; single-profile PSS differs0.85%, without replicated
memory evidence. Current official WHNF already caches these eligible modes.
The candidate is closed with code/raw retained. All12writing rounds are performed
by root and compile to9pages; user forbids delegation, so self-review is explicit
and no independent audit is claimed.

Runtime11 first full paired block loses to strong native preparation/snapshot;
the complete12ProofNet/12mini service matrix remains open. SMT E025 first
stock/branch/logical trio preserves native artifacts but branch is24.8%slower
thanstock and essentially tied with logical reuse; the full12condition matrix still requires recovery and completion.
Complete externalCPU context22 now uses a charged native fallback for an
unexportable prefix, all814original source outcomes matching stock; the original
failed attempt and remaining192context-cell scope are preserved.

These results bound current implementations, not the Initial Narrative or
research ambition. Genericfork/cache/hostfiltering is prior art; no positive
systems novelty, completeGPUkernel, cross-version tuning causality or venue
acceptance follows. Full behavior/resource/load/scaling/placement/history/
cancellation, both formal datasets, strongest competitors, closest work,
paper/WRITE/reflection/independent audit/main completed-step publication remain.

[Current complete evaluation](evaluation.md), [implementation](implementation.md)
and [step report](tmp/bootstrap/step-0007-20261010T000125+0000/step-report.md)
own current evidence. [Prior extended frontier](tmp/bootstrap/step-0007-20261010T000125+0000/archived-idea-frontier-before-direct-mini-20261014.md)
preserves all historical intermediate details. No scientific-contract change
or accepted idea-level change is made by this frontier clarification.

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
