# Reclamation/complete-checker mechanism source review

Observed2026-10-16, parent BOOTSTRAPstep0010/RQ4 and closed E037. Root directly applies research-literature-novelty; no new agent, scientific-contract change or iter-refine-ideas invocation.

## Declared question and finite coverage

Claim1: a complete GPU checker requires actual expensive dynamic work and paid memory/reclamation, not only device-ready object IDs. Claim2: replacing append-only exhaustion with recovery at explicit evaluator boundaries is a concrete algorithm detail worth testing, not by itself novelty. Coverage: same normalization/allocation mechanism, official Lean kernel workload/competitor and validation boundary, plus adjacent GPU functional runtime. Completion is primary-source verification of each category and a falsifiable host-setup decision; no exhaustive absence/first-GPU claim.

Exact current web queries: HVM2 GPU memory allocation garbage collection interaction combinators paper; nanoclo lean kernel checker arena allocation garbage collection; Lean proof checker GPU full kernel normalization garbage collection. Secondary Reddit/aggregate results are excluded as evidence. Reopened material is limited to the untested reclamation/complete-checker alternative, not a repeated import-cache or thread-count survey.

## Verified primary evidence and threats

[HVM2 paper source](https://github.com/HigherOrderCO/HVM2/blob/main/paper/HVM2.typst), opened full primary page, describes a CUDA interaction-combinator runtime with dynamically freed nodes via erasure and explicit semantic limitations for duplicated lambda terms. This makes dynamic reuse and a GPU lambda evaluator prior art, not our contribution. Its interaction throughput is not a Lean complete-checker result and cannot replace the matched CPU competitor. A direct Lean substitution into that evaluator needs a semantic translation argument; no such port is admitted here. The page identifies itself as work in progress, not verified OSDI acceptance.

[Official NanoClo entry](https://arena.lean-lang.org/checker/nanoclo/), opened primary benchmark, describes delayed substitutions/closure environments and official accept/reject/decline tests. This pressures closure representations and points to runnable native checkers; no current displayed number is relabeled a matched local observation. The existing project already pins source-native sokonanoda and official Init. The official page alone does not settle GPU suitability or the live/dead-state question in our interpreter.

[Official Arena protocol](https://github.com/leanprover/lean-kernel-arena/blob/master/README.md), opened primary repository, uses lean4export inputs and multiple full real-world/adversarial tests. Reuse that protocol and original export identity; do not promote one Init setup into the complete official comparison or replace corpora with a toy lambda benchmark.

[Lean proof-validation documentation](https://lean-lang.org/doc/reference/latest/ValidatingProofs/), opened official source, separates proof/kernel validation and import/runtime risks. Keep the post-export boundary explicit; full source parsing/tactic elaboration is outside this proposed native checker measurement, and existing end-to-end source/service/SMT requirements remain.

## Contradiction/coverage disposition and handoff

High same-mechanism risk for GC, closures, array IDs and prepared sharing separately. Potential larger contribution remains an integrated supported complete checker/system with a better measured joint frontier and honest fallback, not a renamed allocator. No such contribution is demonstrated by these sources.

Existing E037data cannot distinguish live capacity from retained dead transient allocations. Its parse-time pointer-map overhead also remains charged. A quiescent-step tracing/reuse algorithm would test that distinct uncertainty at the same capacity; merely enlarging buffers or dropping fallback work would not. An adverse complete host result must stop this constructor before another narrow GPU implementation. A positive still needs complete-cost opportunity, actual GPU engagement, compatible full validation and strong native comparisons.

Strongest native competitor remains the existing version-pinned optimized sokonanoda, not a new collection of weak interpreters. No new benchmark acquisition, extra numerical baseline, service deployment or GPU job is requested by this review. The reference official protocol defines the eventual full-corpus metrics; current E040is integrated development setup and has zero independent novelty. Source-level alternative only; root retains the original contract.

Canonical background-related-work.md contains another owner's pre-existing dirty work and is left untouched; this detailed node and current evaluation link retain the finding without staging their content. No paper/bibliography or user-instruction rewrite is made by this literature node. Residual uncertainty: source-to-runtime semantics, collection/root correctness, actual full paid work/cost and differentiated system novelty; all remain empirical obligations.
