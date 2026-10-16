# E037: parse-fused representation and canonical worker state for complete checking

Observed2026-10-16. Root proposal under unfrozen BOOTSTRAP step0010, after completed E036 official-input setup and fresh result audit. This is a different substantive mechanism, not another E036 plan-review round, larger-arena tuning, a Meta descriptor census or a device microkernel. Original user instructions, Initial Narrative, allfourRQs, Lean-first/SMT/services/RTX5090/full-paper scope remain intact.

## RQ, hypothesis and research decision

Parent RQ4 is: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

Hypothesis: a complete-declaration backend can retain the expensive native work lost by the frozen interpreter if it combines (1) GPU-ready arrays emitted as part of the existing native parse, and (2) exact closure/environment-aware canonicalization and memoization in a reusable private worker arena. Removing the second whole-graph pointer-map traversal and reducing repeated transient evaluator objects must together create an actual complete-cost opportunity before a GPU port is justified.

The intended main experiment is the full native verifier process, after export input is ready, with device checking and native fallback versus the strongest measured optimized native checker. The two host mechanisms are integrated setup for that experiment, never standalone paper results. If they fail to recover expensive work within a credible whole-cost budget, stop this constructor without launching a narrow GPU substitute. Ordinary CPU compilation is already a baseline and cannot be reported as the new contribution.

A substantial positive would be a real complete-checker heterogeneous execution frontier over standard full inputs, with resource/fallback/representation/causal evidence. It would support RQ4; it would not by itself answer the service/SMT RQs, prove source-elaboration speedup, demonstrate novelty over existing graph evaluators, or establish OSDI readiness. A negative would reject this concrete GPU-friendly representation/evaluator design, not GPU Lean in general.

## Why this mechanism rather than the previous one

Actual E036 full official Init has59626declarations/57544bodies. The stage-only checker spends1.827905of2.167728s in native checking, so total check work is significant. However, frozen host positives cover only4.8413%of recorded body CPU;27378arena-exhausted bodies carry77.44%. Eager pointer-keyed graph packing takes0.621892s, versus0.337582ssummed native CPU in positive bodies. The native4.9prefix gives a different14.53%positive CPU share and remains separately identified.

The existing optimized CPU baseline accepts full Init in2.249777s at the official4thread recipe. One necessary available-CPU baseline at24threads also accepts, observed2.001414s; neither single observation proves a universal optimum. Future matched comparison must inspect actual available CPU resources and use a credible fastest native recipe rather than exploit the weaker configuration.

Current E036 sources, raw inputs, failures, all native verdicts and result reviews are preserved on main e06a9c6. The unchanged eager bridge/frozen interpreter remains deferred. This proposal addresses the two measured causes, not merely declaration-count coverage or launch scheduling. Repeating all old Meta observations, scalar GPU tests or CPU compilation grids would not answer it.

## Concrete implementation contract

### Parse-fused device representation

Inspect the pinned native frontend's existing record-index tables and typed parse path. Emit the closure-compatible expression/level/declaration/name/reference arrays when those source records are already decoded and validated; retain a cheap name-to-declaration index for forward metadata. Avoid a second hash-map traversal from all native pointer roots. Keep the authoritative original parser/verdict policy and raw input identity. Any extra allocation/writing/translation remains charged to parsing/preparation.

This is a source-dependent design to implement, not a claim that the parser already exposes a public dense IR. Determine its actual ownership/lifetimes/layout before editing. Native pointer bytes, Rust enum layouts and arbitrary host pointers must not be assumed CUDA-readable. A compact name/reference fix-up, if required, is part of the actual complete path, not an uncharged preprocessing oracle.

### Exact private worker state

Canonicalize immutable runtime terms with the complete tag/payload/lexical environment/universe environment/substitution identity; canonicalize binding chains and levels with full-key collision checking. Preserve freshness of neutral locals. Inspect and remove any mutation of objects that would become shared. Cache only completed operations whose full inputs and mode/scope are represented in the key; never AST-ID-only inference/equality caching.

Use caller-owned per-active-worker storage and generation/epoch tags to reuse tables across tasks without full per-query clears or cross-query truth reuse. Retain existing arena/step defaults as the initial algorithm condition: do not manufacture coverage by increasing them or run an arena-size grid. Extra table/frame storage is real and must be measured, not called free. Capacity/undecided/unsupported remains native fallback. Record actual arena peaks/reasons naturally during this candidate's full execution, not as another standalone census.

A persistent GPU task cursor, only after the host opportunity is credible, decouples active scratch count from total declarations. Worker count is derived from actual kernel/device/memory availability and shared5090conditions; no exclusive GPU slot, fixed half-memory reservation or new policy is introduced.

### Native complete integration

All declaration metadata/type/universe/theorem/inductive/recursor/quotient obligations retain native checking. Any body work removed must be replaced by a positive qualified device/host check on that exact native task. Respect native ordered-declaration visibility and full level/binding scope; the frozen diagnostic does not currently enforce all of them. Invalid/missing references, unsupported semantics, failures and capacity exhaustion remain fallback/complete native decisions. Do not infer replacement soundness from accepted-corpus agreement.

The official good/bad suite supplies proportionate complete-verdict qualification before native body skipping. No new correctness-only research loop is proposed. Source export/elaboration remain outside this declared post-export benchmark, with their actual construction/reuse cost disclosed before any broader source-verification claim.

## Baseline, inputs, controls and main relation

Native algorithm source is pinned sokonanoda7645b1e1fcac. Use official-style native-target/Init.Prelude-trained PGO and real CPU resource evidence; preserve strongest baseline/source/profile provenance and all failures. A diagnostic with discarded profile counts is not silently relabeled the exact optimized baseline. Device/native comparison must run on the same actual machine/input and disclose added GPU resources/shared interference; current owning Workspace is CPU-only.

Official inputs: full Init4.34.1 is already built, byte-preserved and archived (347555345B/6487065lines). Full CSLib4.34.0 and Mathlib4.34.1 use pinned Arena test sources and actual resolved dependencies/exporter identities. Do not replace them with Prelude, generated toy proofs or the retained4.9prefix. Regenerable input/SDK state can use existing owning Workspace /tmp (~295GiB at discovery); durable scientific outputs stay in the repository.

Main methods: strongest optimized native CPU; new memoized algorithm on host plus native fallback as the same-algorithm hardware control; new GPU algorithm plus native fallback. Three ordered repetitions across allthreefullcorpora are intended, with alternating method order and complete original outcomes. A cache-off/fused-representation-off ablation is justified only to explain the implemented mechanism, with its full overhead/fallback retained, not a new competing baseline family or microbenchmark gain.

Primary metric is process-start-to-complete-final-verdict/exit wall, including parse/fused representation, allocation, initialization/JIT, transfers, device execution/synchronization, native fallback and cleanup. Report CPU/RSS, actual GPU resources and shared activity, paid support/fallback and skew with observation limits. No sum of CPU intervals is converted into a wall-speedup claim. Official parser-only is a component control, not a verifier competitor.

## Executability, real preflight and continuation

Current executable pieces are the original optimized native checker, completed official full Init input, diagnostic native patch/host engine and existing finite K8s5090benchmark path. Parse-fused/canonical candidate and its GPU backend are not built; this document is not a ready command or a preflight pass.

Initial admitted development must build the concrete parse/evaluator changes and execute full official Init on the host with actual complete native results and paid-cost association. That is integrated mechanism setup. If expensive work remains outside the candidate or preparation/algorithm cost consumes its opportunity, dispose the constructor and retain raw failures; do not label setup as the main experiment or extend profiling by renaming it.

If actual host/native evidence makes device continuation credible, implement the complete backend and run real GPU preflight on the full official Init through all methods, actual5090engagement and final native decisions. Current Workspace has no visible NVIDIA device, so use the existing bounded owning-PVC K8s test path, with source/build preparation in the owning Workspace. Preserve other GPU owners, use time-sliced5090only, and run both native/GPU methods on that same runtime host. Revalidate actual manifest/runtime/CPU ISA/defaults and resources at that point; no replacement Workspace, B300, persistent service, mount or scheduler.

Only actual successful preflight admits the complete declared matrix; full execution and result review are required before scientific claims. A failed/mixed result is retained and reviewed on its actual boundary. All raw/partial/error/source/build/command/metadata and device receipts must remain, with main checkpoints at completed boundaries.

## Novelty and alternative work

Hash-consing, memoization, dense IDs, prepared state and persistent workers already exist in Lean/native checkers/graph runtimes; none is a novelty claim by itself. Existing sokonanoda session caches and prior Bend/HVM/interaction-net work remain explicit competitors/closest-work risks. The possible systems contribution requires an actual differentiated complete kernel/backend/service and full evidence; no 'first GPU' claim follows from the Arena list lacking a GPU entry.

The alternative is returning to a differentiated deeper native prepared-state service mechanism, rather than ordinary import reuse already present in Kimina/REPL/snapshot systems. Current cohort/preparation data and existing negative routes make another import-only or scalar-pair experiment low value. Root chooses this concrete evaluator/representation mechanism because it targets the dominant observed expensive work and an explicit preparation cost, while keeping the original full scientific scope.
