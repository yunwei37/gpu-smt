# E037 independent plan review — round 1

Observed 2026-10-16 UTC. Fresh native reviewer, independent of root implementation and the E036 result reviewer. This is E037's first admission review, not a reset of the closed unchanged E036 constructor. I read the plan, the complete human instruction record and Initial Narrative/evolution/RQs, current evaluation/closest-work map, E036 source and completed official Init result/review, raw baseline/diagnostic receipts and the full 59,626-row paid-cost CSV. I inspected the actual pinned native parser and checker/cache sources in the retained owning Workspace. I made no code changes, builds, checker reruns, GPU calls, Git operations or other-agent changes. This report is my only written file.

## Verdict and exact admission boundary

**Admit integrated development and host setup for the proposed complete-checker experiment. Do not treat this review as GPU-backend, real-preflight, full-matrix, replacement-soundness or paper-contribution certification.**

This proposal changes two concrete mechanisms that E036 found adverse: it replaces the eager pointer-root traversal with representation emission during native parsing, and replaces repeated transient closure/environment construction with exact immutable canonicalization and completed-operation memoization. Those are substantive implementation changes, not another arena-size setting, another descriptor census, a scalar kernel, or a new label for the same unsuccessful implementation. Source inspection establishes plausible integration points and specific current duplication; it does not establish that either mechanism will recover enough expensive work.

There is no scientific or executability defect that blocks **that development/setup boundary**. The complete new executable and device command do not exist, so claiming ready-to-run admission for the main GPU matrix would be false. The plan explicitly says so. Root owns the implementation, scientific disposition and publication; my diagnostic verdict does not authorize broadening the goal or restarting closed constructors.

The full heterogeneous experiment can supply additional evidence for canonical RQ4: “After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?” Its prospective role is **supporting additional RQ evidence**. Parse/host setup alone is dependency work with zero independent paper-result value. Neither outcome answers the native-state service/SMT RQs, source elaboration, all four RQs or OSDI readiness.

## Why the research decision is not already settled

I independently aggregated every E036 official Init row. There are 59,626 declaration rows and 57,544 bodies; all body rows have positive recorded native body-thread CPU. Prospective positives carry 337,581,756 of 6,973,006,231 ns, or 4.8413%, while the capacity group carries 5,399,984,143 ns, or 77.4413%. Positive body count is 40.6072%. The count/paid-cost mismatch is real and already rejects a count-based argument for the unchanged engine.

The retained raw receipts show the original optimized four-thread native checker accepts full Init in 2.249777186 s, and the separate 24-thread observation accepts in 2.001414431 s. The stage-only path reports 0.332858587 s parsing and 1.827904733 s checking within 2.167727732 s whole time. E036's diagnostic pays 0.621891826 s eager packing and 5.025242010 s host queries before all native checks, for 7.930332960 s whole. These are single sequential observations, not uncertainty estimates, an optimum, or an accelerated hybrid result.

The capacity group's cost is **not evidence that canonicalization will successfully check that group**, nor that all its native cost is redundant closure creation. It does, however, identify a specific large paid set that the old constructor misses. Actual source below supplies an independent causal reason to test a different evaluator rather than increase storage. A positive new result changes the decision from “do not port the unchanged eager interpreter” to consideration of a complete device integration; a negative closes the parse-fused/canonical constructor without another narrow kernel. Both differ from merely announcing that an input or compiler is ready.

The principal competing explanations remain credible: native session caches already exploit sharing much more effectively; hash-table traffic or worker scratch can consume the recovered opportunity; unsupported semantic rules rather than allocation may dominate after sharing; and large divergent declaration tasks may have an unfavorable GPU resource frontier. The experiment must let those explanations win.

The strongest alternative use of work is a differentiated deeper prepared-state service design. Current source/cohort and closest-work evidence already makes another import-only replay or generic warm-state primitive weak. Trying this concrete remaining-checking mechanism is a defensible next action; it does not waive the unresolved service contribution or assert that a GPU checker alone satisfies the whole paper.

## Source feasibility: parse-fused representation

Native source inspected: pinned sokonanoda 7645b1e1fcac, actual private package under /tmp/gpu-smt-arena-native-stages-20261016/source.

- src/frontend/parser.rs:44–57 owns names_by_idx, levels_by_idx, exprs_by_idx and the ordered native declaration map. The parser already decodes child record IDs before constructing typed expressions.
- parse_export_mapped at 336–343 and parse_export_file at 407–423 use the same Parser; the stdin path streams blocks through run_over. The native fast path and serde fallback both call shared do_* constructors.
- push_expr at 778–795 records the native typed object; do_app/do_pi/do_lambda/do_let/do_const/do_proj and the level constructors have the source references needed to emit compact arrays. There is therefore a credible way to avoid the E036 Bridge::expr/level pointer maps and flatten traversal.
- finish at 909–920 currently drops raw-index tables and moves only the native DAG/declarations/configuration into ExportFile. New arrays need explicit ownership and lifetime through complete host/device execution. They cannot borrow a parser scratch vector, refer to moved Rust storage, or use native pointers as CUDA addresses.
- Native declaration insertion assigns the declaration index to the interned name. Constants and projection metadata use names, not declaration indices supplied by the export. A cheap name-to-declaration resolution/fix-up is legitimate, but all its actual time and memory remain charged.

**Important actual parser behavior:** push_expr can overwrite an existing raw export slot; put_at at 708–717 can similarly overwrite name/level lookup slots. Existing parent objects have already captured the old native pointer. A packed graph that uses a raw export slot as permanent object identity, and overwrites its contents, would silently change those earlier parents. The implementation must retain append-only packed object identities with a current raw-ID-to-packed-ID map, or an equivalent faithful representation, and capture children at original construction. Sparse IDs and undefined-reference rejection must preserve native behavior. This source requirement was returned to root immediately; root acknowledged append-only identities and correct name interning/alias handling. It is necessary integration work, not a request for another census or a separate correctness project.

Names, universe parameters, string contents, bounded versus large natural literals, special Nat/String names, native-only declarations and recursor metadata must retain exact meanings. Unsupported payloads can conservatively fall back. Parse fusion is not permission to implement a second more permissive JSON parser. Emit after successful native decoding/validation at shared semantic constructors, so fast and general input forms have one meaning. Any forward-name fix-up must preserve declaration cutoff checks; resolving the full graph cannot grant a task access to later declarations.

The plan's “remove packing” language should mean remove the **second traversal**, not assume that extra array writes, allocations, fix-ups or host/device transfer become free. Actual parse-plus-representation cost is what matters. A fused-off comparison is a component ablation only when necessary to interpret the final mechanism.

## Source feasibility: exact evaluator sharing and reusable workers

The frozen bench/lean-gpu/closure-checker.cu supplies concrete reasons why sharing can change the algorithm rather than just its capacity:

- Machine::term and Machine::env append a new object on every call. closure creates another REF; concat reconstructs binding chains; subst reconstructs a term/substitution composition; mat repeatedly exposes closures; nth_arg repeatedly calls mat while walking application spines.
- lv/lv_max already perform a linear full-prefix search for canonical levels. A collision-checked table changes lookup work; levels are not an entirely unshared starting point.
- The current explicit frame machine has no general completed I/W/E result memo. Its equality path can revisit inference/reduction/proof-irrelevance work after structural comparison.
- arena-native-support.cpp already reuses one scratch allocation per active host worker and claims declaration chunks of 64. Merely reusing allocations, adding a cursor, or calling workers persistent is not new evidence.

Exact term keys need all meaningful tag/payload/lexical environment/universe environment/substitution fields, including distinctions between source-level and resolved-level SORT payloads. Binding/environment keys must preserve order, not just the set of bindings. Fresh neutral-local identities must remain fresh. Operation-cache keys need operation, full inputs, mode and all relevant declaration scope/configuration/context. Canonical IDs become valid equality shortcuts only after those invariants hold.

A concrete mutation exists in mat: the MDATA branch creates a closure and then writes z.terms[id].s. If term creation becomes hash-consed, that write can alter a shared object. Root should remove or preserve uniqueness for such mutations before interning. Do not cache a partial/in-flight computation as successful, reuse a capacity/unsupported answer as proof, or carry stale task-local IDs into a new epoch. Task reset must handle epoch wrap safely. These are ordinary implementation invariants, not demands for a formal proof campaign.

The native competitor already has strong sharing. src/checker/cache.rs:150–200 includes closed/open evaluation, type, positive/negative conversion, environment/application/rigid-value hash-consing and related caches. src/checker/eval.rs:30–59 keys open evaluation by a context-sensitive environment plus expression, and distinguishes level substitution. src/checker/tc.rs:140–199 retains session caches across declaration chunks, resets on the 16 MiB session budget, and keeps a separate inductive cache. Canonicalization/memoization itself therefore cannot be the claimed novelty or a supposedly absent CPU optimization.

New hash tables, epochs and memo entries consume memory and work per active GPU worker. Measure actual capacity/arena peaks as part of execution, retaining the reason distinction. Do not equate fewer term allocations or more positive declarations with whole-process gain. The unchanged defaults are a useful initial algorithm condition; no arena-size grid is needed.

## Complete replacement boundary and proportionate correctness

The plan correctly retains complete native declaration/type/universe/theorem/inductive/recursor/quotient obligations. Source anchors are:

- tc.rs:97–105 constructs EnvLimit::ByName(current declaration), marks ordered_declaration, and checks simple declaration bodies or headers.
- env.rs:243–283 derives the cutoff and only exposes old declarations whose native index is less than it.
- infer.rs:117–139 validates universe parameters used by Sort/Const; 467–479 checks declared type well-formedness, duplicate universe parameters and theorem Prop.
- infer.rs:482–490 checks body inference and its definitional equality with the declared type after header checking.

The E036 packed CHECK path does not reproduce all those conditions. Preserving native headers alone does not validate body-only forward references or undeclared universe uses. Exact scope support or conservative native fallback must cover them before any body skip. A “same accepted official input” test cannot by itself establish rejection behavior.

The proposed official good/bad suite and native verdict comparison are a proportionate qualification of the actual implementation, not an invitation to keep performing correctness-only research. Retain accepted/rejected/declined/internal/failure cases and charge fallback. If all native bodies still run, label the execution diagnostic/setup; if qualified positive results replace bodies, demonstrate that the actual native body path is skipped for those exact tasks while all remaining obligations execute. CPU/GPU agreement of the same algorithm supplies a hardware control, not an independent semantic oracle.

## Baselines, workload, metric and resource fairness

One main competitor—the strongest runnable optimized native checker—is sufficient. Its position is that competent native CPU checking already captures the useful sharing and beats heterogeneous complete checking once representation/fallback costs are charged. A matched run is necessary because published Arena numbers use different machines/resources/versions. Extra checker families or a CPU-thread grid are not required to admit the design.

The same-algorithm host plus fallback is correctly a hardware/algorithm control. Parser-only is a component control, not a proof verifier competitor. Cache-off and fused-off are causal ablations, not extra main baselines. Root need not require the same-algorithm host to beat native CPU before any device test: GPU parallelism can change the relation. The continuation requirement is a credible **paid supported work and complete-cost case**, not an arbitrary positive-count percentage or a host-only winning threshold.

The full official Init input is real and preserved, with 347,555,345 bytes, 6,487,065 lines, Lean 4.34.1, exporter/format 3.1.0 and actual exporter commit in E036 receipts. Full CSLib/Mathlib remain unavailable in this plan and must use the declared pinned source-native construction, actual resolved dependencies and preserved input identity; the old 4.9 prefix cannot replace them. The three-corpus, three-method, three-repetition scope is a complete final relation, not 27 independent contributions. Input generation outside the post-export boundary must remain disclosed, and must be included or justified as reused before a source-verification claim.

Process-start-to-complete-final-verdict/exit wall is appropriate for this declared checker boundary. The official Arena README/interface and pinned sokonanoda recipe are the protocol anchors; resource/cost records supplement that ordinary complete-process measurement. Native body-thread CPU sums are useful task-attribution evidence, not a removable wall fraction. Report initialization/JIT, parse/fused writes, fix-ups, allocations, transfers, kernel/synchronization, native fallback and cleanup. Do not subtract a different parser or convert an instruction/summed-CPU metric to wall speedup.

The four-thread official-style baseline and the 24-available-CPU observation are disclosed. Neither single run proves an optimum. Future matched baseline must reflect actual CPU eligibility/quota and current strongest runnable recipe without a gratuitous tuning matrix. Diagnostics with discarded PGO counts are not silently the exact optimized baseline.

The current owning Workspace has no exposed NVIDIA device. Root's subsequent resource discovery says the Workspace is already on lab, with 24 eligible CPUs and no CPU quota; the established finite owning-PVC Job path uses the RTX5090 selector, cached pinned Rust image and one shared nvidia.com/gpu device request, without CPU/memory limits. I did not launch or independently revalidate that job in this review. Actual preflight must inspect the existing manifest/runtime and match native/control/device methods on that same machine; don't compare a Workspace CPU baseline to another machine's GPU candidate. Revalidate ISA support for both binaries and actual shared-device engagement/resources. No exclusive reservation or eviction is implied.

The separate existing /tmp filesystem has room for regenerable SDK/export/build state according to the retained storage observation. Durable inputs/results/source stay in their scientific home; don't delete active/original captures or create a new volume/Workspace to satisfy this review.

## What is and is not executable now

The plan accurately identifies executable original CPU/full Init paths, and an unbuilt parse-fused/memoized candidate. No exact candidate command or GPU run is pretended. That is sufficient for development/setup admission, not for declaring the full experiment executable.

The next useful owner action is to implement the two named mechanisms and execute the actual full Init host setup, associating successful prospective tasks with paid native work and charging the complete new representation/algorithm path. Record the result even if it remains negative. Do not launch another standalone profiling population or repeat old CPU grids to produce activity.

If that evidence preserves a credible complete device opportunity, root can implement the complete backend and perform the planned real full-Init native/host/GPU preflight through the established shared RTX5090 path. Before full-run admission, the actual command, input paths, final outcome rule, raw/resource paths, implementation identity, native replacement engagement and device engagement must exist and run. A unit smoke, toy proof, compilation, this review or a host-only support pass is not that preflight.

Only a successful actual preflight supports execution of the declared complete matrix. Respect the skill's existing preflight/review procedure; do not create new control schemas, quotas or repeated review identities. A valid negative closes this particular constructor; an implementation fault can be repaired within the admitted mechanism with raw failures retained. No desired speedup is specified.

## Paper consequence and owner return

The novelty risk remains high: native checkers, graph evaluators and prepared-state systems already establish hashing, exact sharing, closures, dense IDs and persistent execution. A credible new systems claim needs an actual differentiated complete implementation and a measured resource/performance frontier, with causal ablations and external comparison. No “first GPU” inference or contribution follows from this plan.

E037 is admissible because it tests a different source-grounded algorithm/representation against a serious measured obstacle and has a meaningful stop/continue scientific decision. It is **not** admissible as a standalone report that parsing and memo tables work. Preserve the full user objective, RQ meanings, all negative routes and raw source/build/results. Root should now implement and evaluate the admitted setup; OMP ownership of README/docs/paper/experiment scripts remains intact.

Return: integrated development/setup **admitted**; GPU backend continuation **conditional on actual opportunity evidence**; real GPU preflight/full matrix **not yet admitted as executable**; whole-paper/OSDI readiness **unproven**. No further review round is needed for an unchanged plan. This is round 1, with at most two genuine follow-ups in this same report if the root requires clarification.
