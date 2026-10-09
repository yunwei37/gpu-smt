# Round 8 — Terminology and claim tone

Started: review began before the first recorded clock sample, 2026-10-09T19:22:13+00:00; exact start was not captured.
Completed: 2026-10-09T19:23:42.864022+00:00.
Parent: BOOTSTRAP step-0004-20261009T183603+0000, iter-refine-writing-20261009T190400+0000.
Objective: read-only terminology-infoflow and claim-tone review of the complete current paper.
Entry revision: current 219-line docs/paper/main.tex following Round 7; no Git operations performed. Scientific contract and all numerical values treated as read-only.

Read completely: docs/user-instruction.md; /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md; /workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md; /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md; docs/paper/main.tex. Actual skill files were read directly because no Skill invocation tool is exposed. No invented tool invocation is asserted.

Method: entire-paper reading, compound-frequency audit, concept inventory, ordered J/C/F/X checks, and sentence-level scope-versus-self-attack assessment. BOOTSTRAP present-tense intended-completed prose and explicit results placeholders accepted. No source edits, compilation, Git operations or source copies made by reviewer.

## Concept inventory

The inventory groups standard related terms rather than treating each adjective as a new named concept. Use locations below are all relevant sections/line ranges; repeated common words inside each range are not new concepts.

| Concept / technical vocabulary | Definition or grounding | Uses |
|---|---|---|
| Formal verification; candidates/attempts; proof-generation streams | Abstract 12–15; Introduction 24–26 | Introduction 24–45; Background 48–56; Motivation 66–74; Design 77–125; Implementation 128–153; Evaluation 156–196; Discussion 199; Conclusion 215 |
| Lean, proof assistant, parsing, elaboration, proof construction, kernel checking, proof term, dependent type theory, imports/declarations/environment, accepted commands/context, admissions/sorry | Introduction 24,28,30; Background 49,55,58–59 | Abstract 19; Introduction 24–45; Design 103–125; Implementation 128–153; Evaluation 165–196; Related work 203,212 |
| SMT, SMT-backed verification, solver; translation, preprocessing; SAT/UNSAT/UNKNOWN; models/proofs/unsatisfiable cores; solver scopes/options/assertions/queries | Expanded Abstract 19 and Introduction 24; Background 51,58 | Introduction 28–45; Motivation 72–74; Design 99–107; Implementation 128–146; Evaluation 165–191; Related work 206 |
| Logical context, native execution history, native state, original interface, observable behavior/fidelity, artifact validation | Introduction 28; Background 58–61; Design 103–107 | Abstract 14–18; Motivation 72–74; Implementation 128–151; Evaluation 179–194; Discussion 199; Related work 203–209; Conclusion 215 |
| Result cache, persistent environment/session, REPL, backtracking, pickling, proof-state snapshots, incremental elaboration/post-import snapshots, bounded warm services/workers | Introduction 30; REPL expanded there; Background 58–61 | Abstract 15,19; Motivation 68; Evaluation 160,167,174,184–186; Related work 203–209 |
| Native execution prefix, preparation, prepared state, preparation boundary, candidate suffix | Introduction 32–36; Background 58; Design 77,97–101 | Abstract 16–19; Motivation 66–74; Implementation 128–148; Evaluation 158–191; Discussion 199; Related work 208–209; Conclusion 215 |
| Parent, branch, independent/disposable branch, immutable preparation, branch-local mutation, branch-owned communication, quiescence, runtime threads/extensions/descriptors | Introduction 34–36; Background 61; Design 97–113 | Abstract 17–18; Figure 79–95; Implementation 128–148; Evaluation 179–186; Discussion 199; Conclusion 215 |
| Candidate lifetime, cancellation, failure, isolation | Introduction 26,32–36; Design 109–113 | Abstract 13,18; Motivation 66–74; Implementation 142–146; Evaluation 159,179–186; Discussion 199; Conclusion 215 |
| Copy-on-write, private dirty pages, proportional shared/fleet memory, retention/admission/placement/concurrency, replacement costs | Background 61; Design 116–118 | Implementation 142,148; Evaluation 169,184–186; Discussion 199 |
| Native resource counters/work limits, service elapsed/CPU accounting, wall-time limits, machine load | Introduction 28,34; Background 61; Design 105–107 | Abstract 14,18; Implementation 142–146; Evaluation 169–171,179–181,194 |
| Equal-resource service frontier; latency/throughput/memory, matched CPU capacity/memory budgets | Introduction 34 | Abstract 15,19–20; Design 77,116–118; Evaluation 156,160,167–171,184–186; Conclusion 215 |
| Heterogeneous checking/device operation; CPU reference/fallback, representation construction, setup, upload/download/transfer, synchronization/queueing; RTX 5090 | Abstract 19; Introduction 36; Design 121–125 | Implementation 151–153; Evaluation 161,188–191; Limitations 196; Related work 212 |
| Source verification versus post-export checker replay; complete verification/checking; matched measurement boundary | Background 49–51 | Design 123–125; Implementation 137,151; Evaluation 167,169,189–191; Limitations 196; Related work 212 |
| Dynamic context-sensitive checking, reduction, binder environments, instantiated constants, expression graph, integer identifiers/delayed substitutions/parallel arrays | Design 121; Implementation 151 | Evaluation 189–191; Related work 212 |
| Workload/control/ablation; source streams, ordering, fan-out/locality, preparation depth, exact duplicate reuse; uncertainty/repetitions; offered load/concurrency | Motivation 66–74; Evaluation 165–176 | Evaluation 179–191; Limitations 196 |
| Verus/VeruSAGE, Mathlib, Lean Kernel Arena, Z3, Kimina, Nanoclo/nanoclo-fortran, SOCK/SEUSS | Cited named systems and datasets in Introduction 28–30, Evaluation 165–167,191 and Related work 203–212 | Those same locations; standard names, not invented paper concepts |
| Ready-work width; resident work | Evaluation 191 only | Evaluation 191; findings below |

No system name is introduced, so the system-name macro rule finds no hardcoded system-name violation. No new mathematical notation or metric acronym requires reconciliation. The paper coins no unnecessary capitalized/core named concept; its main vocabulary is preparation, native behavior, branches and service resources.

## Raw findings

### Must-fix

None. The reader can follow the native-preparation/independent-execution distinction and all four RQs without learning an invented framework.

### Should-fix

**S1 — Evaluation, heterogeneous execution, line 191; J1/J3/C2.**
Quote: `Cost coverage, ready-work width, complete CPU/device comparisons and workload crossover.`
Problem: `ready-work width` is an undefined one-use compound inside a results placeholder. Its presence is not a missing-results defect; the wording itself leaves the eventual reported quantity unclear to a systems reader.
Concrete fix: replace only `ready-work width` with `amount of checking work simultaneously ready to execute`. Preserve the entire placeholder and every other requested result. This explains the existing quantity without coining a named metric or changing RQ4.

**S2 — Evaluation, heterogeneous execution, line 191; J5/C2.**
Quote: `We separate host representation construction, device setup, transfers, resident work, synchronization and fallback.`
Problem: `resident work` may mean resident-state preparation or operations with data already on the device. The latter appears to be intended because Design line 125 already separates such measurements from complete checking.
Concrete fix: replace only `resident work` with `checking with data already on the device`. Keep setup, transfer, synchronization and fallback accounting intact. If a different residency boundary is intended, retain the phrase until the root verifies it; do not silently alter its meaning.

### Consider

**C1 — Abstract line 19 / Introduction line 36; C2/J6.**
Quote: `native logical or serialized prepared-state reuse`.
Problem: The baseline classes are understandable after the REPL/backtracking/pickling discussion, but the abstract uses these classes before that explanation and a broader OSDI reader may not connect serialization to retained verification context.
Concrete fix: in the abstract only, use `native logical branching or reuse of serialized prepared states`; leave every competitor and the complete-verification scope intact. This is optional clarification, not a scientific reclassification.

## J/C/F/X and claim-tone results

| Check | Result |
|---|---|
| J0 frequency | prepared-state 9, proof-state 4, equal-resource 3, resource-bounded 3, fan-out 3; these earn their usage or are standard descriptive qualifiers. Single-use ready-work triggered S1. Hyphen regex fragments copy-on-write/end-to-end, so fragments are not treated as new concepts. |
| J1–J6 | Two localized readability ambiguities; standard native/runtime terminology is grounded. No project run IDs or script labels leak into prose. RQ meaning is protected. |
| C1–C7 | No material synonym or capitalization drift. `service frontier` and `resource frontier` refer back to the explicitly defined achievable latency/throughput/memory combinations. Captions use the same preparation/branch/history vocabulary as the body. C1 is an optional first-use clarity improvement. |
| F1–F9 | Main conceptual order is preparation versus history, established reuse, branch mechanism, fidelity, lifetime, placement, device qualification, then RQs. Each RQ has setup/procedure/metrics or explicit unanswered-result status. No reordering is required in this round. |
| X1–X7 | Abstract/intro/body/conclusion preserve the same operating scope. Repetition of complete-cost and behavior constraints serves claim scope and is not deletion material. Four contribution forward references are structured contribution pointers. |
| Claim tone / self-attacks | No apology or gratuitous weakness sentence warrants deletion. Resource-bounded behavior, unsupported boundaries, baseline strength, GPU scope and novelty comparisons are substantive scientific scope. In particular lines 101,105,151,194–196,203,209 must retain their technical substance. |

## Preservation, dispositions and handoff

All four RQ meanings, full Lean/SMT source-verification versus post-export scope, RTX 5090, strongest native/warm/cache competitors, failed/incomplete attempts, response/artifact fidelity, resource-bounded qualifiers and complete CPU/device costs remain untouched. No quantitative value or citation was changed. No results were invented. No substantive limitation or design decision was recommended for deletion as a self-attack.

Reviewer applied/rejected fixes: none, as mandated by read-only delegation. Root must record an explicit accepted/rejected disposition for S1, S2 and C1 after source review. Source changes, before/after evidence, compile/page evidence and verification belong to the root's completion of this serial round. No compilation claim is made here.

Alternative considered: adding formal definitions for one-use terms. Plain descriptions are preferable because the existing scientific concepts do not require new named labels.
Tree/memory change: only this report created; paper untouched. Remaining concern: root should confirm the intended residency boundary for S2. Next node: root disposition, minimal subsection-local fixes if accepted, compile/preservation check, then Round 9.

Summary: 0 Must-fix, 2 Should-fix, 1 Consider. The three useful improvements are describing simultaneously ready checking work, clarifying device residency, and making the abstract's serialized-state baseline explicit. No broader terminology overhaul is justified.

## Root disposition and completed round

2026-10-09T19:27:28.594075+00:00: S1 accepted, replacing only ready-work width with amount of checking work simultaneously ready to execute; S2 accepted after confirming Design separates resident operation cost from complete checking, replacing resident work with checking with data already on the device. C1 deferred: current abstract class wording matches the native logical/serialized baseline family used in the introduction and setup, already unpacked immediately in Background; another local compound substitution adds no necessary distinction. Scope, four exact RQs, all quantitative data, all 39 citation commands and all 12 placeholders preserved. Subsection-local reviewed patch only. Fresh make exit0, PDF8pages, complete round8-build.log. No scientific reclassification or new data. Round9 is next.
