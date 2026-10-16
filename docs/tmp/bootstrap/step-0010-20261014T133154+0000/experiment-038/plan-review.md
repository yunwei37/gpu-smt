# E038 independent plan and admission review

Observed 2026-10-16. Fresh reviewer, first round. Reviewed the complete user instruction, Initial Narrative and evolution, unchanged RQ3 and evaluation promise, current evaluation and paper source, closest-work map, E038 plan, closed service/device dispositions, E036/E037 results, pinned Beam/leagent receipts and actual installed native 4.27 sources/symbols. Only this review file is authored. No candidate implementation, build, native verification, GPU run, full collection or Git action was performed.

## Verdict

**Admit integrated native implementation and real setup as part of the proposed complete service experiment. Do not admit a full-cohort collector, final performance matrix or GPU implementation on this plan alone.** This is not a positive novelty or performance verdict.

The candidate mechanism is materially different from E023 per-candidate process replacement, E029 plain shared-process placement, and the closed E036/E037 partial declaration interpreter. It attempts to retain the native elaborator and kernel while changing the physical ownership of mutable prepared cells and the complete lifetime of tasks. A fair comparison could discriminate whether competent native logical reuse already supplies the attainable frontier or whether candidate-specific runtime mutation/lifetime handling produces a useful additional frontier. Existing timing data do not settle that different mechanism.

The strongest credible positive is a verification-native state/lifetime integration that preserves the supported native interface while improving the joint complete-verification memory/throughput/latency frontier over the strongest warm/native alternative. A table of versioned-cell lookups, successful runtime linking, ordinary concurrent native commands, or one accepted proof would not supply that result. State versioning, copy-on-write, immutable heap sharing, snapshots, native parallelism and task ownership are established mechanisms; assembling them under a new name does not establish a paper contribution.

The current plan has enough executable source grounding to justify implementation/setup, rather than demanding an additional standalone census. Its full-run commands, exact cells, repetitions and target joint-frontier presentation are explicitly unfinished. That is appropriate for an implementation that does not exist yet, but they must become executable in this same experiment before a full collector is launched. This distinction is a scientific executability judgment, not a new approval policy or a user-author wait.

## RQ fidelity, paper value and alternatives

Selected RQ3 remains: “How does prepared-state branching change end-to-end latency, throughput and memory at equal resources compared with established warm-session reuse?” No RQ rewrite, narrower success definition, arbitrary-program transparency claim or positive-speedup prerequisite is accepted.

The central uncertainty is not whether Lean can run two commands concurrently. Current source already demonstrates native concurrency and reuse. It is whether exact candidate-local runtime mutation and lifetime can be separated cheaply enough to improve complete service resources without changing native responses or contaminating subsequent work. The plan identifies this uncertainty and puts all costs and failures inside the comparison.

Role: the completed integrated experiment can be **decisive for this constructor within RQ3**, and supporting evidence for the larger paper. Its initial source/link/real-input setup has **dependency-only independent value** and must remain folded into that experiment. There is no result yet.

Decision outcomes are genuinely different:

- A qualified joint improvement against the strongest matched warm/native method, with a branch-off control explaining the incremental effect, supports continuing this mechanism and its complete causal/service evaluation. It does not by itself establish novelty, complete RQ3, support GPU acceleration, or answer the other RQs.
- A valid adverse frontier closes this constructor for the measured supported regime. It does not prove all prepared branching or GPU verification impossible.
- A memory/throughput/latency tradeoff can be a valid mixed result. Do not require every metric to improve if the actual claim is a joint frontier; retain the cost of worse metrics and the fixed behavior contract.
- An unengaged implementation, unqualified unsupported effects, avoidably broken baseline, changed native resource policy or missing complete task costs makes the corresponding inference inconclusive/invalid, not a candidate win.

The best alternative next action would be to finish the already-running strong CPU evidence and synthesize the existing negative results, or implement a different source-grounded high-cost native mechanism. The former must continue but cannot resolve this new native ownership uncertainty. Another scalar GPU port or narrow eager interpreter would have less decision value given the measured closures. This native integration is therefore a defensible next implementation within the complete goal. No claim that it is certain to outperform all unexplored ideas is warranted.

## Closest work and baseline pressure

The pinned official [leagent frontend](https://github.com/leanprover/leagent/blob/87dc16bef0cda8ad1c973a5146510a3e6f1bfda9/lean-extract/Corpus/Frontend.lean) already shares a process, warms discovered import registries and uses a mutex around imports before command elaboration outside that lock. It also explicitly warns about source code registering global extensions. Its current source is a direct same-mechanism threat to warm imports plus native parallel frontend execution. It is not a matched numerical baseline on this exact 4.27 producer cohort: its actual toolchain, outcome contract, options, returned artifacts and service accounting must match before making that comparison.

Pinned [Beam status](https://github.com/leanprover/lean-beam/blob/c98913c7feb6f0146ffb115ffafd124ff762aa16/docs/STATUS.md) documents concurrent operations, follow-up handles, cooperative cancellation and handle invalidation. These capabilities remove cancellation, retained state and concurrent request handling individually from novelty. Beam explicitly limits its managed-state annotations rather than promising OS sandboxing. Its current compatibility receipts are not evidence that it can directly replace the original 4.27 whole-source verifier, and its reported features are not measured superiority on our workload.

Kimina, native REPL backtracking/snapshots, Snapshot-DSP and AXLE remain existing reuse/isolation competitors. Faasm/RedLeaf/isolates, SOCK/SEUSS and snapshot work also make general heap sharing/isolation and lifecycle ideas established. The incremental claim must be the concrete verification-native integration and its demonstrated resource/behavior benefit. Source inspection has not established that no earlier work implements that same combination. A positive still needs source-grounded same-claim literature pressure and full-paper review.

The plan correctly selects the strongest runnable matched warm/native service as the main competing position: existing logical reuse may already capture all useful benefit. Its victory would reject an incremental advantage in the tested regime. An unchanged cold process is only a cold/setup control. Plain in-process parallel native frontend execution without the mutable-state overlay is a causal control; it must not be promoted to another new main baseline or mislabeled as the proposed contribution.

Published Beam/leagent/AXLE claims cannot settle the exact current numerical comparison. Conversely, incompatible toolchain or artifact contracts must not be manufactured into an external-baseline failure or candidate win. There is no need to expand the baseline count. The strongest fair existing configuration and the necessary component control are sufficient in principle.

## Actual native source and binding findings

Installed SDK examined:
`/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux`.

Exact producer-native REPL examined:
`/tmp/gpu-smt-goedel427-20261014/repl-producer-native`, including `REPL/Main.lean`, `REPL/Frontend.lean`, `lakefile.toml` and actual binary symbol receipts. This avoids accidentally reviewing the separate 4.9 or 4.21 trees as the 4.27 baseline.

### 1. Engage the real native path

The current receipt records statically defined ref/task primitives in the REPL and `SYMBOLIC STATIC_TLS` flags on SDK `libleanshared.so`. A preloaded shared library alone cannot be assumed to replace those calls. This is an actual implementation boundary, not a stylistic preference.

Independent `nm -A --defined-only` on installed `lib/lean/libleanrt.a` locates `lean_st_mk_ref`, get/set/swap/take/ptr_eq and `lean_io_as_task/map_task/bind_task` in **io.cpp.o**. Scheduler task core functions are in object.cpp.o. The similarly named upstream [object_ref.cpp](https://github.com/leanprover/lean4/blob/v4.27.0/src/runtime/object_ref.cpp) contains a constructor wrapper, not the ST reference primitive implementation. Do not choose an archive replacement from its filename alone.

Native runtime/library integration must cover both compiled calls and any interpreter/dynamic paths used by this exact producer. Preserve the original binaries and matched native compilation composition. A counter that increments only in an unused wrapper is not engagement. Source/link receipts plus a real original command and a proportionate imported-reference control should establish the actual path without turning this into a detached symbol-discovery program.

### 2. Reference versions must preserve native ownership

[4.27 ST source](https://github.com/leanprover/lean4/blob/v4.27.0/src/Init/System/ST.lean) binds mkRef, get, set, swap, unsafe take and pointer identity. The installed header additionally declares reset; a prototype should reconcile symbols actually used by the exact binary rather than guess from a nearby release.

[4.27 runtime IO source](https://github.com/leanprover/lean4/blob/v4.27.0/src/runtime/io.cpp) handles persistent initialized refs as potentially multithreaded. Reads acquire ownership safely; take temporarily empties a cell; set consumes a value; swap returns the old owned value. An overlay must preserve these ownership and empty-cell semantics across aliases and branches, including descendant threads. Copying an address/value into a map and incrementing it later is insufficient if another thread can release its last owner. A branch-local cell accessed concurrently still needs native-equivalent synchronization. Pointer equality concerns reference identity, not the address of a replacement value. These are implementation facts of the chosen integration, not demands for exhaustive arbitrary-program equivalence.

Retaining base refs safely also avoids address reuse masquerading as an earlier prepared identity. Preparation enumeration must account for cells initialized before the overlay's entry, including persistent globals, instead of assuming all useful cells are created after a late hook is installed.

### 3. Task context is larger than spawn-time worker TLS

The installed header exposes spawn_core, map_core and bind_core, plus synchronous paths. In the inspected [4.27 scheduler](https://github.com/leanprover/lean4/blob/v4.27.0/src/runtime/object.cpp), bind can suspend and later resume through another task dependency. The current-task TLS is scoped during closure execution; queued dependency and finalization states have separate lifetimes.

Installed `Init/System/IO.lean` explicitly documents that impure asTask/mapTask/bindTask work keeps running after the last external Task reference is dropped. Therefore branch identity must be captured at task admission and preserved through map/bind, synchronous execution, re-enqueue, cancellation, exceptions and deactivation. Merely setting TLS in the HTTP worker or releasing a branch when its main Task handle disappears loses legitimate descendants.

Keep the branch owner until all admitted work is settled, and distinguish a returned response from final release. Cancellation is cooperative and cannot promise prompt termination of arbitrary native code. A process-shared candidate cannot use killing the whole worker as if that were independent cancellation. These source constraints belong to the integrated implementation and complete-cost comparison; they do not justify indefinite lifecycle-only investigation.

### 4. Not every mutation is an ST reference

The same scheduler/object source contains `lean_thunk_get_core`, which exchanges a thunk closure and memoizes its value in the shared thunk object. A deferred computation whose result can depend on branch-local mutable reads cannot automatically reuse the first branch's memoized result. Ordinary genuinely pure imported thunks can remain shared. The implementation must handle the actual supported effect boundary rather than assert that versioning refs makes all heap mutations private.

Promises, external objects, native globals, loader/initializer caches, OS streams and FFI are also outside a plain ST cell overlay. Their presence is not blanket proof of impossibility. It is a reason to establish a useful supported native regime and a real fallback before an unsupported mutation reaches shared state. Dynamic discovery after an unsafe side effect cannot retroactively make that candidate isolated.

### 5. The exact REPL still executes global entry actions

Producer `Frontend.lean:37–57` calls `Lean.initSearchPath` and `enableInitializersExecution` even when a saved command state is supplied. The latter writes a runtime-global reference. A proposed branch boundary cannot assume that the saved-state path touches only StateT-local state.

Installed [ImportingFlag.lean](https://github.com/leanprover/lean4/blob/v4.27.0/src/Lean/ImportingFlag.lean) explicitly assumes single-threaded access while importing and resets flags in finally. Installed Environment.lean also has global extension registries, realization refs, and persistent imported regions. This supports the plan's preparation/unsupported-effect distinction. The stock import synchronization requirement cannot simply be removed by sharing logical command state.

The original `runCommand` includes native processInput, message conversion, sorry/open-goal extraction, optional tactics/infotrees and new snapshot construction before response. `maxHeartbeats=800000` and `autoImplicit=false` are explicit in this producer. These remain part of the comparison. A whole-source command is not equivalent to merely closing saved tactic goals; neither library extraction nor Beam tool success substitutes for the original native result.

## Workload, metrics, resources and executability

The original 29,750 Goedel4.27 sources, order and all outcome classes are the appropriate first actual population. There is one import root; this cannot be relabeled as a multi-context working set. ProofNet and miniF2F can expand the same comparison when their actual version-aligned adapter exists. Neither a new convenient compiler version nor a renamed common header supplies broader evidence.

The currently published measurements show substantial competent warm reuse and low sampled import entry weight, not a large saved import-wall fraction. Therefore the plan should not promise a large import-time speedup. A runtime mutation/ownership mechanism can instead change the fleet memory/concurrency frontier, which the old CPU percentages do not bound. No new standalone Amdahl census is necessary before integrated setup. Actual complete setup should report base/private/version/task footprint and fallback, not only count refs.

The primary service metrics—corpus makespan, attempts/second, per-input response latency distributions and fleet PSS/memory—match existing Kimina/Lean service and prepared-execution evaluation practice. Responses and final task release must be measured separately, with complete costs charged. Component counters explain results; they are not an invented paper score or denominator. Do not subtract overlapping request times or sampled CPU shares from makespan.

The current main plan cites precedents descriptively, but its final executable matrix should link the exact official native/service benchmark entry and target latency/throughput/memory table or figure. Repetitions should expose whole-run uncertainty rather than pool requests into an artificial confidence interval. Offered-load replay must be identified as synthetic unless actual verifier arrivals exist; existing generation-availability clocks are not such arrivals. This is an experiment-protocol completion item before full-run interpretation, not a blocker to native implementation.

Resource discovery records 24 eligible CPUs with no cgroup CPU quota or memory cap and no visible NVIDIA device in this Workspace. Independent current filesystem reads show approximately11.03GiB project free and288.25GiB free in existing /tmp. Private regenerable builds should use that existing test-local space; preserve raw/failure evidence and project source. No volume, mount, hardware placement, quota, scheduler or persistent helper is needed for the proposed native setup.

This experiment is CPU-native service work. It neither allocates a GPU nor establishes a GPU opportunity. Any later device work remains RTX5090 only through the existing authorized resource path and needs its own concrete remaining-work/cost case. There is no reason to occupy GPU resources for a runtime-ref proof control.

## What makes the next boundary real

Proceed with the substantive integrated implementation at the root's technical discretion. The next completed setup must include engaged native full verification of a real preserved source, the matched original path, response construction and actual final release with costs. Imported-ref/alias/task/cancellation sentinels are small validity controls within that same setup. They must not replace the real source or become an open-ended correctness campaign.

Before a full preflight/collector, complete the same plan with actual source/binary/library identity, command and data/raw paths, fixed native resource/timeout policy, observed supported effects/fallback behavior, main baseline and branch-off control, ordered repetitions and completion rule. If a useful unchanged-source regime cannot be supported before shared-state contamination, close this constructor or return the concrete limitation; do not filter difficult original attempts, weaken the claim, or run the whole cohort first and call matching accepts isolation.

No new collection or GPU run is admitted by this review. No measured E038 result, surviving systems contribution, complete RQ answer, completed paper or OSDI acceptance exists. Root retains implementation and scientific disposition; existing OMP file ownership and unrelated dirty source remain untouched.

## Review accounting

First fresh plan-review round only; no follow-up used. The source findings above are specific implementation evidence and executable-result conditions, not additional runtime quotas, hard performance targets, model limits or demands for author confirmation. Re-review is warranted only after a substantive revision or executable setup changes the evidence, not for waiting or an unchanged plan.
