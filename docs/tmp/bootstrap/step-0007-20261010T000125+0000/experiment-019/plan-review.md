# E019 independent plan review — round 1

2026-10-13. Reviewer: `/root/gpu_declaration_plan_review`, fresh independent child. This is plan review, not result review, whole-step audit or venue acceptance. No experiment was executed by the reviewer. Only this report was written.

## Verdict

**Admit the supporting experiment and proceed to actual integrated RTX5090 preflight.** One necessary basic declaration-rule omission was found and repaired in source during this round: theorem declarations must have a type in Prop. The rebuilt CPU library and PTX must contain that repair before they can discharge declarations in preflight or the full comparison. This is artifact synchronization for the repaired executable, not a new hypothesis or request for additional scientific review.

No other scientific or executability blocker was established from the reviewed files. Device availability, real CUDA execution, resource fit and complete basic outcomes are still unknown and belong to the declared real preflight. A successful build or CPU algorithm control is not a successful GPU preflight.

## Inputs and review scope

Read `docs/user-instruction.md` first, the complete experiment-design skill and plan template, full `docs/idea-story.md` including Initial Narrative, `docs/evaluation.md`, the E019 plan and its primary-source literature node. Inspected `bench/lean-gpu/checker.cu`, `bench/lean_gpu_check.py`, `bench/sokonanoda_gpu_service.rs`, `bench/build_sokonanoda_prefix.py`, `bench/run_lean_gpu_backend.py`, relevant producer code in `bench/LeanCompleteBackend.lean`, and the executed backend-build3 checker/source receipt. Read the official checker's declaration rule and masked suffix loop to examine the actual partition rather than infer correctness from the proposed method's output. Existing acquisitions were neither changed nor interrupted.

Selected RQ remains: **After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?**

## Admission and decision value

The hypothesis is substantive for the stated narrow supporting scope: can real proof-term inference/conversion on the device, followed by actual official CPU checking of everything undecided, reduce the complete frontend/export/check cost after reuse? The existing GPU metadata result and CPU cache observations do not answer it. Success would justify further work on heterogeneous checking; a complete negative identifies this fragment/representation/device-lifetime boundary as unhelpful. Neither outcome closes RQ4 or replaces the formal benchmark/service objective.

The plan explicitly preserves all 24 contexts and 14,913 original edits, failures and duplicates, with three whole paired repetitions plus separate resource profiles. It does not promote the inspected 3-of-40 CPU-control engagement into a general coverage result. This is more decision-relevant than another tiny cache-policy adjustment. A wider GPU kernel or a different residual stage is a possible subsequent scientific choice, not an admission prerequisite for this runnable supporting comparison.

Bare prefix reuse, fork, array representation and dependent typing are established mechanisms. The literature node appropriately distinguishes external Lean checking and GPU proof/certificate generation. There is no defensible novelty or speed claim from implementation alone.

## Baseline, workload and measurement fairness

The main comparator is credible: the optimized official closure CPU checker, reusing an independently checked imported prefix, receives the same producer, source population, success-only cache, archival policy, CPU affinity and matching backend binary with device use disabled. It represents a competing answer that reuse on CPU suffices. A matched measurement is needed; published measurements on another checker/version/export path cannot supply it. The shared-source CPU clone of the CUDA algorithm is correctly labeled an engagement control, not the numerical main baseline. No additional baseline is required for this supporting experiment.

The GPU is explicitly additional hardware, with shared time-slicing rather than a half-card or isolation guarantee. Whole makespan/throughput includes frontend work, independent preparation, export, Python conversion, the CPU algorithm control, CUDA initialization/JIT/transfers/checking, official fallback, archive and EOF/exit. Kernel timing is only component evidence. This prevents a metadata or resident-kernel speed from masquerading as full verification acceleration. The archive-removed bound remains optimistic, not measured production performance.

Ordinary wall/CPU/memory metrics are suitable; their source attribution can be made more precise in eventual paper writing. This is not a scientific blocker. Three whole paired repetitions can reveal variation but cannot support a stable tiny advantage merely because their mean is favorable. A GPU win over this comparator alone must remain this comparison's result; it does not establish superiority over native snapshot execution unless the relevant strong-native evidence also supports that interpretation.

The public LeanPolish subset is honest supporting evidence rather than a substitute for the complete miniF2F/ProofNet main evaluation. Version separation between 4.21 supporting inputs and the retained 4.9 formal data is explicit. No accepted-only selection, fabricated online arrival workload, or stitching across execution versions is admitted.

## Necessary basic semantic finding and disposition

The official checker in `src/checker/infer.rs::check_declar_info_v` requires a theorem's declared type to inhabit Prop (`sort.is_always_zero()`). The initially inspected GPU `Machine::check` discarded the result of `sort_of(d.type,0)` and consequently lacked this declaration-kind rule. CPU/CUDA agreement would not detect the omission because they share the implementation. It could allow discharge of a theorem declaration that the official checker rejects; this is directly relevant to the plan's fixed basic oracle.

The reviewer notified root. The source now retains `type_level` and returns undecided for `d.kind == 2 && type_level != 0`; the official CPU fallback handles it. This restores the necessary rule at source level without adding diagnostic matching or a general proof-of-checker campaign. The concrete library/PTX identities must be rebuilt and recorded. Build3's Rust partition identity is otherwise unaffected by this CUDA-source repair.

The remaining reviewed fragment is deliberately conservative: unsupported node/rule, universe scope, local polymorphism, inference/conversion failure or working-capacity exhaustion discharges nothing. The official parser consumes an overlay first; returned serialized names map to actual declarations; imported declarations cannot be skipped; every unmasked appended declaration passes the official checking algorithm before complete acceptance. The global partition, not a lone GPU flag, provides the basic acceptance boundary. This review is not a formal soundness proof, and real source verdict agreement remains necessary.

## Executability and fixed run contract

The full command, source paths, pinned build receipts, ordinary raw outputs, repetitions, condition ordering, whole-source coverage and EOF completion rule are concrete. The runner uses source hashes, preserves incomplete cells and avoids treating partial progress as whole timing. The inspected selective checker actually skips only named suffix declarations; CPU mode checks the full suffix. A failed GPU command leaves the skip set empty, so it does not become an acceleration win through missing checks. Missing/failed GPU engagement must be reported explicitly even if CPU fallback completes.

The original 143→0→143 preflight is real input, with native/official-CPU/GPU-plus-fallback paths and expected basic accepted/rejected/accepted outcomes. It must demonstrate actual 5090 work and full fallback, not just the retained CPU-only qualification. Retain the proposed limits of one reviewer plus at most two follow-ups and at most three integrated preflight attempts; this round does not reset them.

The source PVC has little remaining capacity and concurrent acquisitions consume storage/CPU. Before the full run, use actual preflight/resource evidence to ensure the declared raw capture can finish or obtain the existing authorized resource repair. Do not delete retained raw data or change timing boundaries to force completion. These are execution dependencies, not a demand for extra workloads, arbitrary quotas or another scheduler.

## Handoff

Continue the declared real preflight with repaired, pinned CPU/PTX artifacts, then the complete unchanged supporting matrix if it runs. Preserve all failures, basic discrepancies, fallback and shared-device receipts. Perform one fresh result review only after the promised full coverage is terminal. This approval is not GPU execution, a performance result, complete verifier correctness, RQ closure, a whole-step audit or OSDI acceptance.

## Follow-up round 2 — resident worker before full acquisition

2026-10-13. Same reviewer; cumulative plan-review count **2/3**, actual integrated GPU preflight count **1/3** before the proposed second device attempt. The previous review and cold-path evidence remain intact. Reviewer read human intent again, the revised plan, E92 and continuation frontier, resident worker and incremental representation sources, resident Rust service, builder selection, backend-build5 executed receipt, frozen `runtime-source2/execute-preflight.py` and `execute-full.sh`, and the retained CPU-only 143/0/159/143 dependency output. No test, device operation or Git action was performed; only this follow-up was added.

**Verdict: approve the implementation refinement and proceed to actual resident GPU preflight2, then the unchanged full matrix if that preflight succeeds.** No new blocker was established. The hypothesis, RQ, expected direction, official basic oracle, main CPU comparator, complete source population, repetitions and primary whole boundary remain unchanged. This is a changed executable before any full acquisition, not a mid-run timing splice or reset of review/attempt counts.

The change is scientifically preferable to repeatedly paying the already observed cold CUDA initialization for every candidate while comparing against a resident CPU checker. Standard context-lifetime reuse has no standalone novelty claim. The revised implementation measures the full cost of preparing the worker, converting/uploading the imported prefix, checking candidate overlays and completing device EOF/exit, so its whole latency cannot be inferred from a warm kernel timer.

The separate Python worker owns CUDA. The CPU parent independently checks and seals the prefix, starts that worker before acknowledging readiness, and forks only CPU candidate children. Each child invokes the official parser on the real overlay first, maps returned serialized names back to actual suffix declarations, and checks every undecided declaration with the official algorithm. Imported declarations cannot be skipped. The device worker merges each candidate with a copied host prefix state; device allocations retain the prefix, replace the current candidate tail, and use current graph sizes. The inspected growth path restores the prefix after reallocation. No candidate's appended declarations or literal identifiers are promoted into the next candidate's host base. These are source observations, not a general isolation or formal kernel soundness proof.

CUDA rules, theorem-Prop guard and working-capacity/depth limits are the already qualified build2 rules. CPU/CUDA shared-source agreement remains a control rather than an independent semantic oracle. The actual second preflight still needs useful 5090 discharges and official checking of all remaining declarations. CPU-only resident qualification does not establish either device reuse or GPU performance.

Adding original edit159 to preflight yields two distinct real overlays instead of counting the cached repeated143 as a second worker request. The retained dependency output has 143 and159 uncached, each 40 declarations with 3 discharged and 37 official-CPU checked; source0 rejects and the final143 is explicitly cached. This is a valid readiness refinement within the existing population, with no accepted-only selection of the full experiment. The frozen preflight checks all four native/CPU/GPU basic outcomes and requires two actual nonempty 5090 result records before returning success. A failed command stops `execute-full.sh` before full acquisition; it does not automatically retry.

The final command is `sh artifacts/lean-gpu-checking-2026-10-13/runtime-source2/execute-full.sh`, using producerbuild6, resident backendbuild5, frozen resident Python sources and unchanged build2 CPU/PTX artifacts. The older command remains historical cold-path evidence, not the final executable. Backend-build5's receipt reports normal build exit0 and the same official native-CPU/profile recipe. No live CPU comparator or acquisition was replaced.

The main comparator disables the worker environment in the same backend binary; it remains a real resident official closure checker rather than the CUDA algorithm's CPU clone. GPU resources are additional and shared, not equal total hardware or isolated performance. The proposed interpretation remains restricted to this matched supporting comparison until stronger native/main-formal evidence supports a larger statement. All192 context cells and119304 source outcomes, resource profiles, deviations and one fresh complete-result review are still required.

The existing capacity concern remains an execution dependency, not a newly imposed budget. Actual preflight/device errors, fallback, resident setup/teardown and raw records must be retained. A startup failure or silent all-CPU fallback cannot be counted as useful GPU engagement; whole measurements with such a failure need the plan's invalid/inconclusive qualification. Do not extrapolate preflight1's cold overhead or preflight2's component times into a full-corpus benefit.

No further baseline, diagnostic-string matching, thread-cleanup test campaign or extra workload is required by this review. Resident device execution remains unqualified until the actual preflight returns; no whole result, RQ completion, final step audit or venue acceptance follows from this approval.
