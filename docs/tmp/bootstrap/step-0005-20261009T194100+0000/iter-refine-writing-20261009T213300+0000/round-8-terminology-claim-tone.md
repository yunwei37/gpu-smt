# Round 8: terminology and claim tone

Read-only reviewer: `/root/step5_writing_round8`, Codex GPT-6.1 sol session identity inherited from the parent; no separate model override. Parent: `/root`, BOOTSTRAP step 0005, writing cycle `iter-refine-writing-20261009T213300+0000`. Review started 2026-10-09 21:59 UTC (first read; seconds not captured). Completed 2026-10-09 22:00:47 UTC.

Objective: fresh whole-paper terminology/infoflow and claim-tone review, without changing scientific meaning. The only written artifact is this report. No paper, bibliography, code, canon, Git, build, native execution, or other agent activity was performed.

## Inputs and method

Read `docs/user-instruction.md` first, then the complete actual filesystem skills `check-terminology-infoflow/SKILL.md`, `paper-writing-style/SKILL.md`, and `iter-refine-writing/SKILL.md`. Applied terminology-infoflow scope only, in J → C → F → X order, followed by sentence-level self-attack and claim-tone mechanics. Read the sole complete `docs/paper/main.tex` (236 lines) and complete `docs/paper/references.bib`. No old reviews or expected fixes were read. Bib annotations informed whether neighboring-field terminology belonged to established work; this is not external citation verification.

Entry SHA-256: main.tex `33f266676f1a83ea0687c15252767fd0bd70173aa26a5f594b0962c17e2767e9`; references.bib `f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2`. No Git revision was queried under the parent prohibition. The initial `python` inventory command was unavailable; reran successfully with `python3`.

## Must-fix

None. No invented branded core concept, undefined central mechanism, hardcoded system name, or cross-section conceptual contradiction found. The service has no declared system name, so the macro rule does not require inventing one.

## Should-fix

1. **Implementation / Native adapters, L146 — adapter/driver synonym drift.** Quote: “Qualification compares fresh driver execution with the matched standalone executable”. The implementation introduced the native SMT command **adapter**, but never introduces a distinct driver. This leaves the reader to infer whether qualification applies to another component. Minimal fix: “Qualification compares fresh adapter execution with the matched standalone executable”. Keep the rest of the sentence, build-metadata distinction, observed differences, diagnostic-only rejected paths and qualification requirement intact. This is a terminology clarification, not a proposal to merge actual implementation components.

2. **Implementation / Native adapters, L148 — first-use acronym.** Quote: “to distinguish parser EOF effects from branch effects.” EOF first appears here without expansion. Its meaning is familiar to many systems readers but the phrase supplies a mechanism distinction that should be immediately readable. Minimal fix: “to distinguish parser end-of-input effects from branch effects.” Alternatively use “end-of-file (EOF)” if literal end-of-file behavior is technically necessary. Preserve the three compared cases and retained native command context.

## Consider

1. **Related work / Persistent verification state, L220 — defensive novelty aside.** Quote: “Failure collection and saved-state execution are not service novelty.” The sentence correctly marks established capabilities, but its negative formulation reads as author self-attack after the paragraph already explains the strengthened baseline. Preserve its factual substance with “Failure collection and saved-state execution are established baseline capabilities.” Keep the preceding LeanPolish native mechanisms, failed alternatives and screen/source boundary distinction unchanged. Do not delete the sentence without retaining its baseline classification.

2. **Related work / Prepared execution, L226 — reviewer-directed prerequisite tone.** Quote: “A contribution beyond these prepared-execution systems requires more than specialization to verification.” The substance belongs in the comparison, but the sentence sounds like instructions to the authors rather than explanation to the reader. A minimal positive formulation is “The comparison with these prepared-execution systems tests the verification-specific requirements of native behavior and bounded shared preparation.” This overlaps with the following sentence; the parent may instead retain the current text to avoid unnecessary redundancy or weakening the novelty boundary. No new novelty claim is authorized.

## Concept inventory and definition order

The paper introduces no branded abstraction or new named ledger. Prepared native state, original preparation, candidate suffix, native behavior, and fleet memory are explained in ordinary language. Core terms remain stable. Technical vocabulary below lists actual use lines (case-insensitive literal substring inventory, so closely related forms are included); generic CPU/GPU and native/process vocabulary are community-standard. The list covers the reader-facing mechanism, accounting, outcome, baseline and device terms rather than LaTeX/style commands.

| Term / family | Use locations |
|---|---|
| candidate | 14, 15, 18, 19, 21, 26, 28, 32, 34, 38, 43, 50, 64, 65, 70, 72, 75, 85, 90, 105, 109, 112, 114, 117, 119, 124, 126, 131, 141, 155, 171, 172, 178, 180, 184, 189, 191, 194, 211, 214, 232 |
| preparation | 15, 17, 18, 28, 32, 34, 36, 38, 42, 43, 45, 61, 64, 65, 67, 72, 75, 109, 111, 112, 117, 119, 126, 129, 131, 134, 148, 161, 171, 174, 180, 184, 188, 189, 191, 201, 204, 214, 218, 226, 232 |
| native | 16, 17, 19, 20, 21, 30, 32, 34, 36, 38, 43, 44, 52, 56, 58, 59, 61, 67, 70, 75, 85, 87, 88, 89, 93, 105, 109, 114, 117, 119, 121, 126, 131, 136, 141, 143, 144, 148, 150, 152, 155, 157, 159, 164, 166, 171, 172, 178, 180, 189, 194, 206, 209, 214, 218, 220, 223, 226, 232 |
| execution history | 16, 18, 30, 32, 34, 70, 223, 232 |
| accepted context | 14, 26, 112, 117, 152 |
| prepared state | 20, 38, 75, 109, 129, 194, 199, 226 |
| prefix | 59, 89, 105, 189, 201 |
| suffix | 38, 112, 117, 119, 155, 194 |
| quiescent | 19, 36, 38, 114, 155 |
| branch | 8, 19, 20, 32, 34, 36, 38, 43, 44, 61, 70, 75, 90, 91, 92, 94, 99, 100, 101, 105, 109, 114, 117, 119, 123, 124, 126, 129, 141, 146, 148, 152, 155, 161, 172, 173, 180, 189, 194, 199, 201, 218, 232 |
| cancellation | 15, 28, 32, 38, 44, 67, 123, 124, 126, 155, 157, 172, 194, 196, 201, 214, 218 |
| resource counters | 16, 30, 155 |
| service accounting | 20, 38, 124, 206 |
| resource frontier | 36 |
| frontier | 36, 169, 201, 206, 232 |
| SMT | 21, 26, 38, 52, 59, 65, 117, 141, 144, 150, 166, 178, 196, 223 |
| REPL | 26, 28, 30, 32, 36, 50, 54, 59, 67, 112, 131, 136, 150, 161, 180, 199, 201, 211, 214, 218 |
| SAT | 21, 26, 52, 117, 121, 124, 189, 196 |
| UNSAT | 52, 117, 121, 196 |
| UNKNOWN | 52, 117, 121, 136, 196 |
| artifact | 52, 72, 88, 93, 117, 121, 136, 144, 164, 172, 180, 194, 196, 223 |
| kernel | 50, 178, 180, 229 |
| elaboration | 32, 50, 184, 218 |
| tactic | 32, 56, 67, 182, 220 |
| admission | 54, 117, 136, 180, 182, 196 |
| copy-on-write | 61, 129, 131, 155, 226 |
| proportional memory | 129, 161, 184, 201 |
| fleet memory | 129, 214 |
| private dirty | 129, 161, 201 |
| qualification | 136, 141, 146, 148, 159, 214 |
| adapter | 114, 121, 141, 143, 144, 146, 150, 152, 166, 194 |
| driver | 146 |
| EOF | 16, 30, 72, 131, 148 |
| warm | 17, 21, 32, 38, 119, 173, 180, 199, 201, 204, 218, 223, 232 |
| cache | 17, 32, 180, 199, 223 |
| post-export | 50, 204 |
| source verification | 50, 150, 204, 220 |
| binder | 134 |
| reduction | 134, 206 |
| GPU | 134, 164, 211, 229 |
| CPU | 21, 36, 38, 65, 75, 92, 109, 119, 129, 134, 136, 138, 155, 164, 166, 174, 180, 184, 186, 189, 199, 201, 204, 206, 229 |
| RTX 5090 | 21, 38, 164, 204 |

Definitions and first-use checks: SMT expands at L21 and again L26; REPL expands at L32. Native execution history is motivated at L16 and concretized at L30 before design. Resource frontier is explicitly explained at L36 before evaluation; equal-resource/service/resource frontier are contextual shortened forms of the same achievable latency/throughput/memory combinations. Native prefix is explained at L59; suffix is explained at L112 before behavioral contract L117. Quiescent boundary appears at L19 in context of runtime safety and is concretized at L114 by no pending candidate work or unresolved external effects. Proportional/fleet memory are defined within L129 before measured usage. Qualification is operationally explained through comparisons at L136 and L141. SAT/UNSAT/UNKNOWN are standard SMT outcomes, with model/proof/core artifacts enumerated L52. EOF is the sole locally avoidable unexplained acronym reported above. Binder environments and instantiated constants are established neighboring-field mechanism words used to explain dynamic dependencies, not new named abstractions.

## Compound frequency and long-tail audit

Raw hyphenated counts (including labels and placeholder text, which are not prose terminology findings): proof-state (4), branch-local (2), prepared-state (9), to-end (1), native-reuse (2), end-to-end (4), equal-resource (3), post-export (2), re-elaborating (1), copy-on-write (5), native-state (1), fan-out (3), resource-bounded (3), native-session (1), prepared-branch (1), scope-only (1), prior-history (1), branch-owned (1), cross-candidate (2), wall-time (2), command-line (1), execution-phase (1), preparation-reuse (1), warm-session (2), candidate-stream (2), repository-level (1), source-native (1), per-input (3), behavior-results (1), resource-limit (2), multi-check (1), offered-load (1), startup-only (1), context-sensitive (1), multi-user (1), post-import (1), proof-improvement (1), saved-state (1), prepared-execution (1), verification-specific (1), nanoclo-fortran (1), representation-only (1).

High-frequency compounds earn their roles: prepared-state (9), copy-on-write (5), proof-state (4), end-to-end (4). Low-frequency scope-bearing modifiers are retained where removing them would blur the experiment or behavior boundary: branch-local, cross-candidate, post-export, resource-bounded, resource-limit, context-sensitive, startup-only, scope-only, prior-history. Single-use standard/plain modifiers such as command-line, post-import, repository-level, multi-user and verification-specific impose no memorized concept. `source-native` occurs only in an explicit result placeholder, and `behavior-results` is a label. `nanoclo-fortran` is a cited checker name. No new definitions or names are needed for these long-tail forms.

## J → C → F → X results

J: section/RQ titles use readable systems vocabulary. No project paths, run IDs, internal ledger or named status gate leaked into narrative. Technical states are descriptions rather than branding. Candidate fan-out and locality are standard service/workload concepts used in context. The two local Should-fix terms above are the only actionable naming/expansion problems.

C: preparation, native prefix, retained environment, result reuse, and accepted context remain distinct. The paper does not collapse exact duplicate result caches into native preparation sharing. Adapter/driver drift is reported. Native/reference execution, source verification, tactic screen, and post-export checker replay retain different meanings. Fleet proportional memory is the measured shared-memory sum; private dirty memory remains an explanatory measurement, not a synonym. No notation or caption/body term mismatch was found.

F: topic sentences generally motivate preparation/isolation, then give mechanism and boundary. The example in L28 anchors independent lifetimes; design and evaluation continue that progression. RQ evidence paragraphs state the question before measurements. Definition clauses are adjacent to the terms they explain. No flow repair rose to Must/Should severity in this scope.

X: abstract, introduction, design, implementation, RQs, discussion and conclusion consistently distinguish immutable preparation from each candidate's mutable execution history and lifetime. Parent immutability refers to no candidate execution after the selected boundary, not an assertion that all verifier runtime objects are inherently immutable. Device operation qualification, enclosing artifact checks where artifacts exist, and complete CPU/device accounting remain separate concepts. The related-work considerations concern tone only.

## Protected content and review limits

Retain all meaningful boundary statements: own-session history versus preceding alternative suffixes (L117–119); native responses and requested artifacts including UNKNOWN and artifactless responses (L121,136); complete source versus solver-session and post-export boundaries (L50,150,180,204); tactic screening versus enclosing declaration acceptance and admissions (L54–56,182); strong warm/cache/native-reuse baselines and matched CPU/memory resources (L178–180,199–206); device/runtime/transfer/fallback/required online validation costs (L136–138,164,206); RTX 5090 references; all four RQs verbatim; every numeric value and result placeholder. Self-attack detection does not authorize deleting these scope protections. “Qualification does not imply a second full CPU replay” is an essential mechanism boundary, not defensive apology.

BOOTSTRAP completed-system present tense was accepted as authorized. Missing-result and unfinished-code defects were excluded. This report makes no claim of scientific acceptance, citation validity, implemented correctness, measured benefit, compilation, page count or 12-slot orchestration completion. No build was performed because this is a read-only round and the parent owns fixes/compilation.

## Disposition

Totals: 0 Must-fix, 2 Should-fix, 2 Consider. Most useful changes are adapter/driver consistency, plain-language parser end-of-input, and positive wording of the existing LeanPolish baseline boundary. Applied/rejected fixes: none by this reviewer; every item remains for parent adjudication. Sentences changed: 0. Next node: parent applies or records rejection of findings, compiles/verifies, and proceeds to serial Round 9.

## Root disposition 2026-10-09T22:01:17.757466+00:00

Accepted S1 adapter/driver wording and S2 parser end-of-input expansion; accepted C1 affirmative existing-baseline classification with no new novelty. C2 rejected because more-than-specialization is a scientific positioning boundary against SOCK/SEUSS, not an apology; the suggested replacement repeats the next sentence and weakens that necessary distinction. No conceptual/technical/number/RQ change;44citations/23entries/12slots preserved. round-8-build.log exits0/eight pages. Reviewer provenance correction: actual spawn explicitly requested gpt-6.1-sol with fork_turns none under human model instruction, contrary to the opening no-override/inherited wording. Skill filesystem sources were root versions, not historical nested copies. Next fresh Round9.
