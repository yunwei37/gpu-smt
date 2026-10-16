# E038: native mutable-state branches within a shared Lean runtime

Observed 2026-10-16. Root proposal under unfrozen BOOTSTRAP step0010. This is a different native service mechanism after closing the E036/E037 declaration-interpreter constructors, not a renamed GPU kernel, CPU compilation optimization or import-cache setting. Human instructions, complete Initial Narrative and four RQs remain unchanged.

## Selected RQ and decisive uncertainty

RQ3: How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?

Hypothesis: share the immutable imported/native proof representation between candidate executions, while giving each candidate a private version of runtime mutable reference cells and its complete task lifetime. This can remove duplicated prepared heaps and per-candidate process setup without the cross-candidate mutable-state interference of an ordinary shared process. A complete verification service, not a cell-lookup benchmark, must establish the joint behavior/performance/resource frontier.

The competing answer is that competent warm/native logical reuse already suffices: branch indirection, atomic reference-count promotion, task context propagation, cancellation and unsupported native effects consume any savings, or most useful memory is already shared by the loader. A null/adverse joint frontier closes this mechanism; another table-size or worker-count tuning grid does not follow. A positive must be tied to the mutable-state branch component and complete costs, not ordinary compilation or native tasks alone.

This is supporting evidence for one RQ, with native-response/artifact/isolation qualification as validity conditions. It cannot replace the complete Lean/SMT/GPU research, all four RQs or full-paper novelty/evaluation promise.

## Existing evidence and primary-source pressure

The full official Init setup just rejected a different narrow interpreter: only6.2732% fixed-prior body CPU coverage with large new costs. Original source-level GPU, per-candidate process placement and repaired SMT-prefix negatives remain closed. E023 already observed a poor latency frontier for the earlier process-branch constructor; it is not revived unchanged.

Kimina already supplies native worker pooling/header reuse; Snapshot-DSP already supplies parallel native tactic states; AXLE already supplies preloaded independent execution. New official source findings strengthen that prior position: leanprover/lean-beam exposes concurrent runAt/cancellation/handle lifetimes, and leanprover/leagent's Corpus.Frontend explicitly warms imports, serializes the import phase, then runs whole-file command elaboration in a shared process. LeanInteract also documents native async elaboration and external parallel servers. Thus warm imports, task spawning, a request broker and whole-file in-process execution individually have high same-mechanism risk.

The leagent source identifies process-global import/initializer/extension registries outside per-file command state, and cautions that source extensions can still mutate those registries. This supplies a concrete boundary that a plain per-job StateT clone cannot promise away. Beam has a different interactive operation contract/toolchain than the original4.27 producer. Neither README is a measured superiority result on our cohort.

Faasm/RedLeaf/isolates and immutable-heap/refcount/fork work establish general co-location/isolation/sharing; transaction/versioned-reference primitives are not new. A surviving contribution would be verification-native runtime-state and task-lifetime handling that preserves the supported complete native verification interface at a measured better joint frontier. The implementation and literature must demonstrate that distinction; this plan claims no first mechanism or OSDI acceptance.

Detailed primary-source receipts/compatibility and exact source files live in literature-20261016T1255. Installed4.27 native inspection finds exported lean_st_mk_ref/get/set/swap and task primitives, but the existing REPL statically defines them and libleanshared uses SYMBOLIC binding. Therefore LD_PRELOAD alone is NOT an engaged implementation. A native link/runtime integration or a demonstrated complete alternative is required.

## Proposed integrated implementation

Root owns Lean/native implementation. OMP retains README/docs/paper/experiment-script ownership. No author file or active acquisition executable may be overwritten.

1. Establish a prepared native command state at the existing supported import/quiescent boundary. Retain exact code/options/compiled-library identity, not a reconstructed logical approximation. The original captured source remains unchanged.
2. Record reference identities created during preparation and retain safe ownership. At a branch, existing prepared mutable cells read the base until first branch write; writes update a branch-local version. Native immutable values remain shared and use the actual runtime's required multithreaded ownership rules. New candidate-local cells remain local rather than copying the complete heap. Get/set/take/swap/identity operations must preserve their native ownership and alias meanings. No borrowed/stale object may be cached as truth.
3. Propagate branch identity through native task spawn/bind/asTask execution, including exceptions and detached/background work. A returned frontend response is not a released branch: keep versions and the prepared owner alive until all admitted descendants settle. Cancellation uses the existing native cancellation mechanism; it must not target another job or allow an old descendant to publish into a reused branch.
4. Keep independent native command/proof state, messages/trees/artifacts, deterministic resource configuration and frontend/kernel checks for every job. No skipped proof, cached verdict, reused mvar assignment, changed proof source, dropped failure or new timeout/memory policy supplies the gain.
5. Classify effects outside this supported runtime boundary honestly. Arbitrary native globals, FFI/external objects, imports/registry growth and OS IO are not made private by a reference overlay. Demonstrate an executable native fallback BEFORE an unsupported effect can contaminate a shared root, or decline the route. Do not retrospectively claim isolation because the ordinary cohort happened to accept. Do not silently exclude difficult original attempts. A general arbitrary-program/process-equivalence claim is not admitted.
6. Native build/link integration must actually engage the implementation despite the observed static/SYMBOLIC binding. Keep original baseline binaries/libraries untouched; use the owning Workspace's existing test-local build area and source overlay. Preserve source and failed builds. Match the final native-compilation composition on every method; compiler flags themselves are not contribution.
7. Include preparation, all snapshots/versions/ownership promotion, dispatch/transport, parsing/elaboration, tactics, kernel checks, queueing where applicable, fallback, artifact construction, task completion, branch destruction and final EOF in whole execution. Record response and final release separately without equating them. Charge memory for base, versions, descendants, native code/driver processes and the baseline fleet.

This is a substantive integrated development/setup proposal. No native runtime overlay, executable frontend integration or device method exists yet. The first setup must establish engaged full native verification and actual costs, not end at symbol discovery, toy cells or compilation. If the system cannot cover a useful actual complete-verification regime without breaking the fixed interface/resource contract, close the constructor rather than weakening those requirements.

## Workload, comparator and planned complete evaluation

Use preserved unchanged original public generated candidate streams, with rejected/incomplete/operational attempts and original order: GoedelWorkbook/Lean4.27 (29,750 attempts), plus version-aligned ProofNet/miniF2F where the supported integration is real. Versions cannot be silently upgraded to obtain a convenient official baseline. Distinct real import roots may be used only when the original corpus supplies them; renaming a single header is not a multi-context workload. The current Goedel header is one root, and that scope remains explicit.

Main competitor: strongest runnable matched native warm/logical-cache service using the same source/native compilation composition. It represents the position that established reuse already reaches the useful frontier. A current official in-process native frontend/Beam path is a main comparator only if its real input/toolchain/verification contract can match; otherwise use it as same-mechanism prior art and report compatibility, not an unfair failure-as-win. Published numbers cannot settle the exact cohort/resource comparison.

Plain in-process parallel frontend without the mutable-state branch is a causal control, not another main baseline or the claimed new system. Existing process-branch measurements are citation evidence until a matched current boundary is actually needed. No grid of weak baseline variants is required.

Primary metrics are published-standard whole-corpus verification throughput/makespan, per-input response latency distribution and complete process/fleet memory/PSS, with CPU/task/fallback costs and whole-run uncertainty. Reuse the actual Kimina benchmark/Lean native evaluation paths and OSDI prepared-execution joint resource measurement precedents. Cold preparation is a labeled component control, not the only competitor. Memory is measured at equal actual CPU resources; no new hard cap, exclusive GPU reservation or assumed fixed share is introduced. Preserve existing native defaults and distinguish any service policy that cannot be matched before interpretation.

The intended final comparison uses ordered complete repetitions, workload/concurrency coverage grounded in actual resources and a causal branch-off control. Exact commands/cells/figure are finalized in this same plan after an actual supported executable exists and before real preflight/full-run admission. A successful setup does not authorize claiming the complete matrix or RQ done. Do not start a background full collector before the actual protocol/resource/behavior boundary is executable and independently reviewed.

## Setup, preflight and interpretation

Initial setup is inside the main mechanism experiment:
- implement actual native/reference/task lifetime integration and matched original path;
- exercise one real original source through preparation, native verification, response and final branch release;
- use proportionate native imported-reference/assignment/cancellation controls to distinguish base/branch isolation and lifetime faults; generated sentinels are correctness controls, not workload performance;
- measure complete setup costs and memory on real input, retain every failed/partial observation;
- establish which native and service resource/timeout policies are actually unchanged before a full native cohort comparison.

Only actual engaged complete verification can admit a real preflight, and only actual preflight supports the final complete comparison. No isolated counter, setup success, synthetic concurrency, reviewed plan or apparent process health is a performance result. No desired speedup, scientific quota or model/agent limit is imposed.

A contradictory result normally bounds this constructor/workload rather than refuting the initial full thesis. A valid positive still needs external same-claim comparison, full causal/resource/behavior evidence and the complete paper gates. Root retains scientific disposition and the full user goal.

## Native service integration update, 2026-10-16 (same RQ3, before full admission)

Actual constructor now runs pipelined native candidates with independent StateT results, prepared runtime-cell versions and descendant lifetime, emitting existing native JSON payloads with custom_id and ordinary timing/fallback metadata. CPU-native external-effect entries are guarded before the listed filesystem/process actions; a marked candidate's response is discarded after branch cleanup and its unchanged original command is replayed through the unmodified producer with the matched plain runtime. Raw fallback exit/stdout/stderr and cold replay/EOF costs remain charged. Process-exit/in-flight-thunk cases terminate only the experimental worker before the unsupported action; pending-request replay after worker death is not implemented yet. Arbitrary native globals, native extensions and uninstrumented FFI remain explicitly unqualified. This is not arbitrary source/process equivalence.

The initial std-stream fallback was over-conservative: upstream MK_THREAD_LOCAL_GET already makes the current stream slots thread-local, and native frontend uses them for isolated streams. Root retains that failed version and removes its redundant get/set guards. The actual filesystem-handle boundary still triggers fallback before open; a finite file-write control subsequently runs only through the original native child. Generated controls remain separate from the official workload.

Source inspection exposes a stronger actual competing path: the retained original Kimina4.27 GC/header-repaired REPL already supports BatchCommand/runBatchVerify, mode naive, sharing one prepared Command.State and native parallel asTask. It is runnable on the EXACT current toolchain; newer Beam toolchain incompatibility does not justify ignoring it. Root builds that path against the same plain rebuilt runtime composition. It supersedes multi-process-only warm reuse as the strongest relevant comparator where batched source verification matches the requested interface; not an extra baseline-count row.

This strengthens the competing explanation: ordinary native batch can already share imported heaps. Removing duplicate warm processes therefore cannot alone be attributed to our runtime versions. The required branch-off streaming component control remains separate, and unknown/untrusted state effects remain part of the mechanism's declared support. Native batch emits one array after its slowest member, while the prototype emits individual completed commands; batch/stream timing must be compared under a stated common request contract, not mixed into an artificial latency gain.

Actual four-original-source integration and listed-effect fallback are dependency/setup inside E038, not the full cohort comparison. Full29,750source outcome coverage, strong baseline mechanism engagement, actual HTTP/request grouping, matched memory/deadline behavior, emitted-response and complete-release costs, PSS/CPU and repetitions are still required before the plan can admit its complete evaluation. No standalone tuning grid, extra native correctness program, GPU use, changed RQ or smaller completed-paper claim follows.
