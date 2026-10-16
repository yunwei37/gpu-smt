# Post-implementation claim audit: native verification branches
Observed 2026-10-16, UTC. Parent: step-0010 / literature-20261016T1255; current implementation d08e1dc, active full capture frozen at v1 (14668bd). This is a BOOTSTRAP literature/implementation judgment, not a completed EXPERIMENT, WRITE or REVIEW gate.

## Objective and declared coverage
The original user-instruction, idea-story and current paper abstract/introduction were reread. Preserve Lean-first full verification acceleration, SMT scope, RTX5090, all four RQs and the intended paper. Do not replace that objective with an ordinary ownership cache or CPU compilation result.

Name-free questions:
1. Does sharing prepared verifier objects with private native mutation/task histories offer a useful additional behavior/resource frontier beyond warm servers, retained proof states and native parallel batches?
2. Can complete real verification distinguish paid preparation reuse from nominal header/state sharing?
3. Does residual heterogeneous execution improve complete verification after the strongest CPU service?

This node checks the strongest same-problem and same-mechanism threats to question 1 and their implications for questions 2/3. GPU/LP and other solver coverage remain in the earlier nodes; no new GPU backend is admitted. The current implementation, rather than an intended system in prose, is the comparison object.

## Search and verification
Executed query revision:
- site.lean-lang.org Lean snapshots parallel elaboration proof state
- site.github.com leanprover lean-beam runAt isolation handle cancellation
- site.usenix.org immutable snapshots shared memory function isolation Faasm Spice

Opened official Beam README/status, pinned leagent source, Snapshot-DSP arXiv v1, official Faasm ATC20 and Spice OSDI26 pages. Prior-node pinned source evidence is linked below. Search results from Reddit, Wikipedia, third-party walkthroughs and gists are excluded as novelty authority. The Lean frontend thesis is a primary lead, not newly read in full or used for a new claim here. Search closes at this finite boundary because the serious threats are already sufficient to reject a generic first parallel/snapshot service claim; this is not an exhaustive literature certificate.

## Verified closest alternatives and operation boundaries
**Matched native competitor.** The exact retained QGC source under experiment-038/service-integration/stock-native-source/REPL/Main.lean:330-343 spawns IO.asTask for each command from an existing initial Command.State, then collects ordered task results. Lines 367-390 select the retained snapshot and native naive batch. This is already same-process prepared-context parallel execution. It is the primary numerical alternative in the active same-toolchain full comparison, not a cold process per proof. Current upstream service README settings do not substitute for this recorded source or the effective address-space policy.

**Beam.** [Pinned official status](https://raw.githubusercontent.com/leanprover/lean-beam/c98913c7feb6f0146ffb115ffafd124ff762aa16/docs/STATUS.md) documents speculative execution, explicit continuation handles, document/version invalidation, concurrent calls and cooperative cancellation. The supported release window is 4.33-4.36; it is not a matched 4.27 executable. Read-only protocol hints do not constitute an OS sandbox. Existing handles/lifetimes/cancellation therefore cannot be claimed as new simply by listing them. Citation-level overlap is high even without a fair direct numerical port.

**leagent.** [Pinned Corpus frontend](https://raw.githubusercontent.com/leanprover/leagent/87dc16bef0cda8ad1c973a5146510a3e6f1bfda9/lean-extract/Corpus/Frontend.lean) warms imports and serializes header processing before optional parallel command execution. It explicitly identifies process-global extension hazards and asynchronous work that requires draining. Its extraction trust level and default synchronous elaboration are material differences from our native service. It is source evidence against generic novelty, not an automatically interchangeable full verifier benchmark.

**Snapshot-DSP.** [Primary arXiv v1](https://arxiv.org/html/2605.25556v1) describes capture/branch RPCs sharing elaborated environments and copying metavariable state for tactic trials. Its 48-problem miniF2F-v2 evaluation uses a patched 4.25.1 and a fresh lake-build fallback; persistent cross-theorem reuse is future work, not a measured result. That denominator differs from our strong warm/native batch. The paper-linked artifact https://github.com/A2DR1/Lean_Snapshot could not be retrieved: official GitHub repository API returned HTTP404 on 2026-10-16. This is an access/availability observation, not proof the authors have no artifact or that the prior claim disappears. Publication is verified as arXiv v1; no accepted venue is asserted.

**Systems primitives.** [Faasm, ATC20](https://www.usenix.org/conference/atc20/presentation/shillaker) combines initialized snapshots with lightweight execution isolation and direct shared memory. [Spice, OSDI26](https://www.usenix.org/conference/osdi26/presentation/holmes) contributes snapshot storage/address-layout and kernel restore co-design. They defeat generic claims that shared prepared memory, private execution and snapshot reuse are themselves new. Their different runtimes/workloads make them conceptual precedents, not additional numerical Lean baselines.

## What the implemented difference actually is
The candidate interposes native reference access, selected deferred work and descendant task ownership over a prepared runtime; this reaches mutable cells outside a copied logical command/metavariable state. That is a concrete implementation distinction from merely retaining a StateT record. It is NOT yet a demonstrated broader behavior guarantee or useful systems contribution. Arbitrary globals, FFI and general interactive handles are not established by the current complete-source interface. A cache tag only reduces a resolver lookup; it adds no new scientific property. The v2 source audit also retains direct unsafe ShareCommon Object.eq/hash visibility of the ref-header tag as an experimental limitation; this is not a new general semantic-isolation claim.

The decisive same-claim comparison is therefore at the operation/behavior boundary: can two original full native requests require independent runtime histories that the existing logical-state/native batch cannot faithfully support, while the candidate preserves exact outcomes and improves a useful latency/throughput/memory frontier? Describing that as a hypothesis does not claim it has happened. Source-level isolation plausibility cannot fill a missing end-to-end performance result.

Risk: HIGH for generic prepared-state reuse, parallel speculative verification, snapshot APIs and ordinary lifetime handling. The intended stronger complete verification frontier remains OPEN, not low-risk or proved. No new name, narrower thesis or frozen scientific-contract change is adopted.

## Experiment handoff and publication implications
- Active E038 is full original 29,750-source stock/private/off across three rotated blocks. Frozen v1 remains untouched by v2. Stock can win, match or fail; every outcome must be retained. Off is a causal control, not another weak baseline.
- This single prepared-context offline ordered batch can settle a restricted native batch cost question. It cannot establish interactive continuation semantics, multi-context eviction, arrival/load tails or every RQ.
- Owner-cache-v2 has one source-preserving native engagement validation only. Co-run clocks are not performance. The v2 compiler/native engagement check overlaps v1 rep1-stock; exact UTC/resource receipts in experiment-038/native-owner-fastpath/development-overlap.json must remain with interpretation of that block. It must not be pooled into frozen-v1 results or called a new contribution.
- Admission of any later experiment belongs to research-experiment-design using these competing positions. Do not add all cited services as redundant weak matrix cells. A closest artifact that requires another toolchain/operation boundary is citation evidence until a fair numerical comparison is actually possible.
- Accepted systems precedents motivate whole invocation latency, throughput/tails and resource comparisons against competent runtime alternatives. Their external workloads do not replace formal Lean/SMT assets. The original Goedel corpus, retained native source and captured full command are available now; no extra toy suite was created.
- The GPU bound remains unresolved for the exact proposed independent work. The corrected 23.6089% is observed wrapped outer thread CPU, not a proof that this fraction of full verification wall time is offloadable. No multiplication of unrelated CPU samples is a strict wall ceiling.

Canonical docs/background-related-work.md and paper are owned by the existing OMP author. This report is handed to that original session; it does not overwrite active canonical files. Completion of this source judgment does not mean canonical integration, full 12-round writing refinement, independent whole-paper review or manuscript readiness is complete.

## Larger axis, uncertainty and next node
The useful larger question is a verification-native shared-runtime mechanism with independent supported effects/lifetimes and a superior complete resource frontier across meaningful contexts. That remains the original ambitious target, not an adopted claim or an instruction to build a new isolation platform. A negative full native comparison should close or revise the current implementation route rather than rename ordinary CPU engineering as novelty.

Next: accept the terminal full-capture outcome once available, retain failures and complete resources, then decide the highest-value consequential experiment. During acquisition root advances actual implementation/scientific work; no goal-turn row polling. Canonical authors reconcile current evidence in their existing owned files, followed by actual delivered-file review and main publication. Missing cross-context/interactive evidence stays visible without an oversized correctness detour.
