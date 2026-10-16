# Native runtime sharing: closest-work and source admission

Observed2026-10-16 UTC, after completed E037 negative evidence. Parent is BOOTSTRAP step0010 EXPERIMENT selection. Root reads human scope, Initial Narrative/RQs and paper/current closest-work frontier; canonical author files remain under original OMP ownership.

## Claim questions and coverage

The finite coverage questions were whether (1) batching GPU LPs or freezing a prepared refcounted heap is a differentiated next mechanism, (2) parallel complete Lean source execution in one process is missing from established systems, and (3) versioning native mutable state while sharing immutable verification data could support a complete behavior/resource frontier. These are alternatives within the original full research goal, not adopted changes to thesis/RQs.

Searches covered same problem (Lean verification/proof services), mechanism (parallel native tasks, mutable cells, prepared execution/heap freezing), setting (full source versus tactic probes), evaluation/compatibility and systems precedents. Queries used:
- site.docs.nvidia.com cuopt batch multiple linear programming problems solver API
- GPU batched linear programming exact certificates Lean linarith Farkas
- Lean GPU kernel checker batch proof verification2026
- Lean theorem verifier GPU checker CUDA
- Lean verification server Task parallel frontend
- Lean proof verification server in-process parallel requests shared environment cancellation
- Kimina Lean server thread multi process parallel LeanInteract Pantograph native tasks memory
- SOSP OSDI language runtime mutable global state isolation shared heap per request snapshots isolates
- PLDI thread local copy on write global references isolate snapshot language runtime
- site.usenix.org serverless language runtime shared immutable heap isolation mutable state
- reference counting fork copy on write immortal objects serverless snapshots heap freezing
- reversible heap freezing reference count copy-on-write fork serverless paper
- site.docs.python.org gc.freeze fork copy on write

Primary docs/repositories/runtime code/proceedings were opened. Secondary tutorials and search-result claims are leads only and supply no novelty decision. This is a source/selection node, not performance progress or an RQ answer.

## Verified primary findings and implications

**Plain native parallelism is established.** [Lean Beam](https://github.com/leanprover/lean-beam) exposes concurrent contextual trial execution, saved state, cancellation and handle lifetimes. Actual source was pinned at c98913c7feb6f0146ffb115ffafd124ff762aa16. Its validated toolchains are4.33.1/4.34.1/4.35.0/4.36.0-rc1; compatibility lines begin4.33. It is not an immediately matched4.27 producer baseline. Its interactive runAt contract is not automatically unchanged whole-file verification. README/status and version receipts are retained. Same-mechanism risk is high for any generic task broker or saved-state wrapper.

[leagent frontend](https://github.com/leanprover/leagent/blob/87dc16bef0cda8ad1c973a5146510a3e6f1bfda9/lean-extract/Corpus/Frontend.lean), pinned87dc16bef0cda8ad1c973a5146510a3e6f1bfda9, already performs in-process complete-file elaboration. It warms imported registries, serializes header/import work, and runs command elaboration outside the lock. It explicitly warns about source code that registers process-global extensions and explains why async task draining matters. This directly rejects “put requests in one Lean process” as a new contribution. The package toolchain is4.33.0, so matched4.27 execution is unproved. Its extraction collector/metrics are not a ready service-response comparison.

[LeanInteract's official performance documentation](https://augustepoiroux.github.io/LeanInteract/v0.10.1/user-guide/performance/) distinguishes within-command async elaboration from external multiple-server parallelism; thread-safe server calls are serialized within one server. That is another established concurrency/reuse position, not evidence that all native global state is independent.

[Kimina's official implementation](https://github.com/project-numina/kimina-lean-server) and [technical report](https://arxiv.org/abs/2504.21230) supply the competent warm/header-pool comparison. Current upstream limits differ from retained producer captures and must not be silently substituted. Matched runtime/source/native-compilation and resource policy, not simply server brand, determine the usable competitor.

**GPU LP batching is not new.** [NVIDIA official convex features](https://docs.nvidia.com/cuopt/user-guide/latest/convex-features.html) already describe parallel batches and sequence solving; current BatchSolve is deprecated in favor of sequential calls or caller parallelism. The official FAQ warns that sufficiently large tasks are needed. These do not establish exact Lean certificate repair, full source speed or a new contribution. Existing finite9-LP certification evidence and huge exact coefficients still matter. A new broker plus batching alone is not admitted by this search; no GPU run is launched.

**Generic freezing is established.** [CPython's official GC documentation](https://docs.python.org/3.11/library/gc.html) already documents freeze/unfreeze and fork/COW sharing. [Official CPython issue40255](https://bugs.python.org/issue40255) discusses reference-count writes, immortality and sharing costs. Thus merely freezing a Lean heap or suppressing refcount writes is high same-mechanism risk, not an alternative headline after E037. No heap-size/freezing grid was started.

**Co-location plus private mutable state faces strong systems prior art.** [Faasm, ATC20](https://www.usenix.org/conference/atc20/presentation/shillaker) combines lightweight execution isolation, shared memory and initialized snapshots. [Spice, OSDI26](https://www.usenix.org/conference/osdi26/presentation/holmes) grounds snapshot restore co-design rather than generic COW as contribution. The candidate must establish verification-native behavior and a complete equal-resource frontier beyond those primitives. These are conceptual precedents; rerunning different serverless workloads would not numerically settle Lean's current cohort.

## Actual installed native boundary

Read-only inspection uses original4.27 SDK /tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux and original repl-producer-native. Installed lean.h declares reference get/set/swap and task interfaces; actual runtime source [io.cpp](https://github.com/leanprover/lean4/blob/v4.27.0/src/runtime/io.cpp) owns reference operations, while [object.cpp](https://github.com/leanprover/lean4/blob/v4.27.0/src/runtime/object.cpp) owns task scheduling and thunk forcing.

The original REPL statically defines reference/task symbols. libleanshared additionally has SYMBOLIC binding. Therefore a proposed LD_PRELOAD hook would miss internal/native paths; exported names alone are not engagement. Both static and loaded native code must use the same actual branch mechanism, with unchanged baseline images retained.

The source's persistent/multithreaded reference reads use atomic ownership transfer before incrementing the returned value; writes promote stored values to multithreaded status. A naive pointer-map replacement must preserve that ownership. A filename guess from libleanrt.a initially suggested object_ref.cpp; actual opened code disproved it (that file only wraps constructors). Correct locations are recorded, not inferred from archive names.

Task spawn/map/bind include sync paths and continuation re-enqueue. Thunks and promises have mutable state beyond references; existing prepared deferred work and task context/lifetime cannot be ignored. These are ordinary source feasibility and fidelity issues inside a substantive mechanism, not grounds for another standalone descriptor census.

## Candidate and baseline handoff

Root proposes E038: native mutable-state branches with task lifetime ownership over a shared prepared Lean runtime. It aims to remove duplicated prepared heaps/process setup while avoiding logical-StateT-only interference. Full native source checking and original configuration remain; effects outside supported runtime state require actual pre-contamination native fallback, not retrospective exclusion.

Same-claim risk remains high. Versioned cells/task ownership are prior concepts, and source inspection establishes neither their complete coverage nor a new systems contribution. The scientific decision is whether an implemented verification-native boundary supplies a better joint behavior/latency/throughput/memory frontier. If no faithful useful regime survives, close it instead of claiming a smaller cache/compilation result.

The strongest matched warm/logical service is the main numerical competitor. A current official in-process artifact is numerical only if version and full verification/response boundaries match; otherwise cite it and label any port/control honestly. Ordinary native parallel execution is a causal control, not the proposed method or another weak main baseline. The unchanged real Goedel/ProofNet/mini source streams, existing exact native outputs and complete capture protocol are available assets; a single-root cohort is not a multi-context eviction workload.

E038 plan and first-round source admission review own the next implementation decision. No runtime overlay, baseline port, new benchmark, GPU allocation, source exclusion, native policy change or paper novelty claim was performed by this node. Canonical background/paper integration is handed to the existing OMP owner; this report does not overwrite their work.
