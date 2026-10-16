# Blind full-paper read and attack map

Started: 2026-10-16T10:39:30Z. Completed: 2026-10-16T10:41:48.237812+00:00.
Parent: step-0010-20261014T133154+0000, intermediate published-version review, target OSDI.
Objective: judge the published paper as one scientific argument before reading external answers or cycle intentions.

## Provenance and reviewer context

Native Codex reviewer, not OMP and not an impersonated external model. Read the complete iter-review-critique skill, research-taste and systems-review references before the paper. Classification: systems (verification serving, process isolation, memory and heterogeneous execution), OSDI bar; using Lean and SMT does not make this an ML-method paper. No ML quality or training contribution is claimed, so the systems reference is the appropriate domain reference.

Entry is entry-provenance.json, retained unchanged. Bundle: /tmp/gpu-smt-published-paper-review-9361cf4/docs/paper; exact published bytes identified by root as commit 9361cf4725a1076f7c839a1065097ca511e9318e, clean at capture. No Git action used. Read all 729 main.tex lines, complete references.bib, Makefile/.gitignore, both plotting programs, cpu-paired-whole-time.source.json, all three standalone claim-bearing figure PDFs rendered with pdftoppm, and published PDF metadata/page extraction. Inspected rendered PDF page 3 including architecture figure. main.pdf is 15 pages, built 2026-10-16T07:10:58Z. Source, plot-source and PDF captions are the paper evidence, not assumed implementation truth. No build or benchmark executed.

Unavoidable contamination: task specifies a published-version intermediate review and active authors, source identity, and later audit paths. General repository safety/ownership rules and task context are inherited. No earlier review, proposed repair, user-instruction, idea-story, internal gate report or author cycle disposition was opened before this record. Bibliography annotations were read as authored paper metadata, not independently verified evidence. No project memory was consulted to preserve this blind assessment.

## Initial paper-only verdict

Reject for OSDI in its current published form. Incomplete but potentially useful investigation; neither an established systems advance nor a completed negative-result study. All four explicit RQs are honestly marked unanswered, with abstract, motivation, evaluation and conclusion placeholders. Completed results actively undermine the two prospective performance mechanisms. Honesty improves trust but cannot replace an answered contribution.

Plain principle: retain expensive preparation while giving each independent candidate its own native execution history and lifetime. This is coherent and potentially durable. The challenged tradeoff is preparation reuse versus native behavior/isolation/resource cost. The paper already admits snapshots, warm bounded pools, copy-on-write sharing and per-request processes exist, so merely combining them is not a belief challenge. A genuinely new verification-specific invariant/mechanism and useful resource frontier must be demonstrated.

## Argument reconstruction

Problem/stakes: proof generators emit many related candidates; repeated imports and initialization consume CPU/memory, while shared sessions can carry history and complicate cancellation. Preparation may be shareable without sharing suffix mutation.

Mechanism: choose a retained prefix; qualify native runtime quiescence/interface compatibility; keep parent immutable; execute original suffix once in a disposable copy-on-write child; own communication, counters and cancellation; fall back to native execution where unsupported. Device path is optional, supported expression work with native fallback and full service costs.

Architecture concerns: qualification is mostly a requirement rather than an inspectable implementation protocol. Exact supported Lean runtime state, thread/finalizer/extension restrictions, timer restoration, descriptor ownership, cancellation within a native check, and placement policy are not specified enough to establish correctness or reproduce the claimed bounded service. Saying that unsupported boundaries fall back is safe only if support is decidable before a mismatch and sufficiently useful in real workloads.

Four claimed contributions: opportunity characterization; native branching and observable behavior argument; bounded integrated implementation; equal-resource evaluation with causal device assessment. Every one depends on missing evidence or specificity.

| RQ | Claimed test | Actual paper answer |
|---|---|---|
| RQ1, preparation opportunity | Real original attempts; expensive shareable work, temporal locality, CPU/memory | Unanswered. Header/reuse counts exist; cost and aggregate sharing missing; LibrarySearch True warmup modifies protocol. |
| RQ2, behavior/isolation | Native results/artifacts, resource limits, candidate/cancellation independence | Unanswered. 10,698 SMT stock/branch comparisons match reported artifacts; full qualification and cancellation matrix absent. Basic Lean outcomes alone are insufficient. |
| RQ3, frontier | Matched CPU/memory, offered load, cancellation, ablations and contexts | Unanswered. ProofNet branches have worse p95 at every rate; >7x warm pool at highest load. SMT branches 28.84–37.91% slower, with more observed CPU and no sampled stock-relative memory saving. |
| RQ4, heterogeneity | Strongest complete CPU path after reuse; real residual dynamic work | Unanswered. GPU is 1.58–3.64% slower on ProofNet; single CUDA thread per supported beta/zeta operation, 0.0925% call coverage; no complete miniF2F or strongest-checker comparison, no cost-weighted opportunity bound. |

## Strongest reject hypotheses and attack priorities

1. Blocker, evidence/scientific framing: proposed service advance has no demonstrated useful operating range. Current strongest direct tests reject its acceleration; missing matrices cannot be rhetorically replaced with many CPU optimization pairs. Need either a genuinely new mechanism that beats competent existing reuse under real demand, or a complete explanatory negative result that answers the ambitious question.
2. Major, novelty: generic prepared-process sharing and isolated preloaded Lean serving may already realize the central principle. The paper's acknowledged prior art makes verification-specific delta especially important.
3. Major, mechanism: branch runtime/behavior fidelity and bounded placement are declared contracts without enough implementation/invariant evidence. Fresh adapter equivalence, split parser effects, resource counters, cancellation inside active work, and mutable runtime extension behavior are load-bearing.
4. Major, evaluation: modified preparation warmup, legacy/current version split, synthetic arrivals and mixed resource blocks prevent a single causal end-to-end frontier. Repeated whole-corpus observations and clear failure accounting are strengths, but unreplicated incomplete PSS profiles do not answer memory tradeoffs.
5. Major, scope/construct: GPU micro-operation has tiny observed coverage and no batching, so this implementation's loss does not answer whether meaningful verifier checking is GPU-suitable. Lean Meta elaboration is distinct from kernel checking; current text correctly warns about this.
6. Major, global logic/writing: four unanswered RQs, prospective design and an evaluation dominated by unrelated CPU baseline repairs do not form a finished argument. Largest writing-only gap is the absence of a compact result/claim map in abstract/introduction/conclusion once scientific answers actually exist.

Strongest alternative explanation: existing warm reuse already captures valuable preparation; disposable per-attempt process overhead destroys remaining benefit; ordinary compilation/arithmetic engineering explains positive results. Small GPU launch/synchronization overhead on almost no work explains its negative result without teaching a new general GPU principle.

## Figure, number and calibration audit

Three result plots visually agree with captions: CPU pair plot uses point ratios with visible parity and does not cross-rank 24- versus 4-eligible-CPU rows; latency survival plot uses per-population log survival, not speedup; offered-load plot visibly shows branch queue growth. Tables are complete per-condition makespans, not kernel/device time. The draft properly preserves operational transitions, background-load uncertainty and failure costs. No obvious arithmetic contradiction found on paper-only inspection. The main inconsistency is rhetorical: asserted implementation/evaluation contributions versus explicitly incomplete qualification, placement and all RQ answers. Need a unified supported-path inventory and per-RQ closure rather than more caveats.

## External verification plan

For contributions/RQ1–3: open SOCK/SEUSS/Spice, Axle, Kimina source/paper, REPL and Lean snapshot work; verify same-claim overlap and whether real serving demand includes expensive repeated setup and cancellation. Check Linux fork safety/accounting and Z3 solver histories/resource limits against claims.
For RQ1/workload validity: official Goedel inference/compile scheduler, ProofNet and released Workbook identities; distinguish task corpus, candidate stream and arrival trace.
For RQ2: actual native APIs, SMT-LIB artifacts/behavior, multithreaded fork, Lean native snapshot support; search contradictory safety limits.
For RQ4: strongest CPU kernel arena checker source and boundaries, Lean Meta implementation, Farkas/HiGHS exactness and cost; GPU dependence/launch construct and full-cost protocols. Search sources that undermine claimed novelty or opportunity, not merely confirm citations.

## Decision, recommendations and next node

Alternatives considered: submission-ready reject/accept, writing-only pass, incomplete scientific program. Choose incomplete scientific program; do not shrink to a micro-optimization paper or declare GPU impossible. Largest plausible claim worth defending is a behavior-faithful verification execution substrate with a useful, predicted latency/throughput/memory frontier, including where heterogeneous dynamic checking helps or provably has insufficient opportunity. Current evidence does not establish it.

Tree/search recommendation only: proceed to mandatory targeted primary-source verification, then full reread before cycle audit. No edits to canonical tree, paper, user log or memory. Project-memory recommendation: preserve provenance boundaries and negative results when the owning orchestrator later reconciles; none written by reviewer.

Completion: blind full-paper assessment complete, initial verdict recorded before external search. Uncertainty: implementation truth and source claims remain unverified; no claim that future active-author work has been reviewed. Next-node contract: 02-external-verification.md must verify every contribution/RQ and report inaccessible branches explicitly; source-grounded verdict follows full reread.
