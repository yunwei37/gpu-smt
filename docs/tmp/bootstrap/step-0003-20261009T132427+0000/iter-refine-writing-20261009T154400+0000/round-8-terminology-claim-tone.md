# Round 8 — Terminology and claim tone

Parent node: bootstrap step-0003, iter-refine-writing-20261009T154400+0000. Read-only serial specialist review after root reported Round7 fixes, successful build and eight-page PDF. Root owns fixes, Git and builds.

Actual execution: full filesystem reads of docs/user-instruction.md, /workspaces/.agent-state/codex/skills/check-terminology-infoflow/SKILL.md, /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md, and entire current docs/paper/main.tex. These are actual filesystem skill invocation/adaptation, not Skill-tool calls. Exact start time was not captured; current review was active by 2026-10-09T17:48:26+00:00. Completion timestamp appears below. No interruption occurred during this Round8. Earlier Round7 recovery is documented separately and is not counted as Round8 work.

Entry main.tex SHA-256: b76c1d0e9c6a8f5a8cc8734dd97c30824739d5907fa2485561ff3bfaa5c26cb7. Counts: four numbered RQs; 12 result slots; 37 citation commands. Case-folded source lexical scan: 84 hyphenated tokens, 41 forms, including labels/placeholders. Leading compounds: prepared-state 9, end-to-end 5, SMT-backed 5, copy-on-write 5, proof-state 4. Leading ordinary vocabulary: native 74, preparation 55, candidate 55, verification 47, execution 42, state 42, service 40. Technical hyphens are not automatically invented jargon.

## Concept inventory and definition order

Core dependency order is candidate/context → ordered native preparation/prefix → supported boundary → independent branch and suffix → behavior qualification/isolation → bounded placement/resource frontier → heterogeneous checking. Core vocabulary is descriptive, not a collection of branded abstractions; no bold/emphasized coined core concepts occur. The effective core concepts are prepared native state, independent candidate branch, and supported native boundary. Resource frontier is a metric/tradeoff description, explicitly explained at L34. Native prefix is defined at L55, suffix at L99, boundary quiescence at L101, observable behavior at L104, proportional/fleet memory at L116, source/post-export boundary at L48. Abstract mentions descriptive preparation/branch concepts before these full definitions but communicates their roles. SMT is expanded independently in abstract and introduction; REPL is expanded at L30. Standard systems CPU/GPU/C++/API and solver status vocabulary do not need mechanical expansion. CLI is a neighboring interface abbreviation needing a first-use expansion (finding below).

The following occurrence inventory covers the technical concept families and their concrete vocabulary, including definitions and all source-line uses. Matching is case-insensitive substring matching, so broad families intentionally include compounds, labels and result slots. Proper-name literature terms remain names of cited work; they are not system-name hardcoding.

| Term/family | All use lines |
|---|---|
| native | 14, 15, 16, 17, 18, 19, 28, 30, 32, 34, 36, 41, 42, 50, 54, 55, 63, 66, 71, 77, 81, 82, 84, 90, 96, 101, 104, 106, 108, 113, 118, 123, 128, 130, 131, 135, 137, 140, 142, 149, 154, 155, 161, 163, 168, 170, 173, 185, 188, 193, 197, 200, 203, 209 |
| preparation | 13, 16, 26, 30, 32, 36, 40, 41, 43, 60, 61, 63, 68, 71, 92, 96, 98, 99, 104, 106, 113, 116, 118, 121, 144, 154, 157, 163, 165, 167, 168, 170, 180, 183, 193, 197, 203, 209 |
| candidate | 12, 13, 16, 17, 19, 24, 26, 30, 32, 36, 41, 48, 60, 61, 66, 68, 71, 77, 86, 92, 96, 99, 101, 104, 106, 111, 113, 118, 128, 140, 154, 155, 161, 163, 165, 168, 173, 190, 193, 209 |
| prepared state | 18, 36, 71, 96, 116, 173, 178, 203 |
| prepared-state | 19, 36, 79, 133, 144, 156, 163, 178 |
| prefix | 55, 84, 92, 168, 180 |
| suffix | 36, 92, 99, 104, 106, 140, 173 |
| branch | 6, 17, 18, 30, 32, 34, 36, 41, 42, 57, 66, 71, 86, 92, 96, 101, 104, 106, 110, 111, 113, 116, 128, 133, 137, 140, 144, 155, 156, 163, 173, 178, 180, 197, 209 |
| parent | 36, 92, 96, 99, 111, 113, 140, 144 |
| quiescen | 17, 34, 36, 101, 137, 140 |
| scope | 14, 28, 36, 55, 65, 66, 68, 99, 106, 131, 142, 173, 175, 188, 209 |
| history | 16, 28, 30, 32, 65, 66, 68, 106, 173, 175, 200, 209 |
| resource frontier | 34 |
| warm | 15, 19, 30, 36, 106, 156, 163, 178, 180, 183, 197, 200, 209 |
| persistent | 15, 24, 30, 55, 63, 196, 197 |
| snapshot | 15, 30, 55, 63, 197 |
| admission | 52, 104, 123, 163, 175 |
| admitted | 52, 96, 133 |
| qualification | 123, 128, 133, 142, 193 |
| fallback | 19, 36, 108, 147, 185 |
| artifact | 50, 68, 90, 104, 108, 123, 131, 155, 163, 173, 175, 200 |
| diagnostic | 52, 104, 133 |
| proof obligation | 52, 104 |
| proportional | 116, 144, 165, 180 |
| dirty | 116, 144, 180 |
| fleet | 116, 165, 180, 193, 197 |
| copy-on-write | 57, 116, 118, 140, 203 |
| elaboration | 30, 48, 165, 197 |
| kernel | 48, 161, 163, 206 |
| post-export | 48, 183 |
| source verification | 48, 135, 183 |
| heterogeneous | 19, 36, 43, 120, 152, 157, 163, 182, 183, 205, 206, 209 |
| device | 36, 88, 96, 123, 125, 146, 147, 149, 185 |
| reduction | 121, 185 |
| binder | 121 |
| substitution | 147, 206 |
| expression | 121, 147 |
| SAT | 19, 24, 50, 104, 108, 175 |
| UNSAT | 50, 104, 108, 175 |
| UNKNOWN | 50, 104, 108, 123, 175 |
| SMT | 19, 24, 36, 50, 55, 61, 104, 128, 131, 135, 149, 161, 175, 200 |
| REPL | 24, 26, 28, 30, 34, 48, 52, 55, 63, 99, 118, 123, 135, 144, 163, 178, 180, 190, 193, 197 |
| CLI | 28, 50, 61, 108, 131 |
| CPU | 19, 34, 36, 61, 71, 88, 96, 106, 116, 121, 123, 125, 140, 147, 149, 157, 163, 165, 168, 178, 180, 183, 185, 206 |
| GPU | 121, 147, 190, 206 |
| RTX | 19, 36, 147, 183 |
| Z3 | 28, 50, 57, 128, 200 |
| Lean | 19, 24, 26, 28, 30, 36, 48, 52, 55, 61, 63, 104, 121, 128, 137, 149, 161, 163, 175, 190, 197 |
| Verus | 161 |
| Mathlib | 161 |
| Nanoclo | 121, 147, 185, 206 |
| SOCK | 203 |
| SEUSS | 203 |
| latency | 20, 34, 36, 71, 156, 165, 177, 178, 180 |
| throughput | 20, 34, 36, 71, 113, 156, 165, 177, 178, 180 |
| makespan | 165 |
| affinity | 165 |
| locality | 118, 161, 168 |
| fan-out | 61, 116, 190 |
| placement | 79, 115, 116, 144, 180 |
| retention | 111, 118, 144, 180 |
| cancellation | 13, 26, 30, 36, 42, 63, 110, 111, 113, 140, 155, 173, 175, 180, 193, 197 |
| cache | 15, 30, 163, 178, 200 |

## Must-fix

None. No factual or conceptual contradiction, changed scientific question, undefined indispensable invented abstraction, or unjustified universal behavior claim was found within this terminology-infoflow review.

## Should-fix

1. Implementation / Native adapters, L131, “CLI-owned command context.” Category C2/J6. CLI appears without expansion. Fix locally to “command-line interface's command context.” Preserve native configuration/manager/solver creation order and original sequence evaluation.
2. Background / Verification stages and outcomes, L52, “an admitted proof.” Category J6/F8. OSDI readers may read admitted as an accepted, fully checked proof, whereas the next sentence distinguishes admissions from complete verification. Fix locally to “an admitted proof, whose obligation is accepted without a proof term.” Retain the citation, unfinished-obligation checks and frontend diagnostics. Root should ensure the explanation matches the intended Lean admission mechanism before application; do not alter acceptance criteria.
3. Design opening sequence, L96, “an admitted prepared state.” Category J5/C1. Admitted here concerns service admission, unlike proof admission in Background. Fix to “a service-approved prepared state.” This only disambiguates the actor and leaves admission/retention policy unchanged.

## Consider

1. Design / Preparation boundaries, L101, “supported quiescent point.” Category J6/C2. Abstract/introduction use quiescent before its explanation here. A minimal clarification at Introduction L34 is “The branch boundary must be quiescent, with no pending candidate work or unresolved external effects, and safe for the verifier runtime.” The existing definition here is adequate for expert systems readers, so root may retain it without duplication.
2. Evaluation / Preparation sharing, L170, “source-native measurements.” Category J1/J3. This compressed descriptor appears in a placeholder and the unanswered conclusion. Fix only the narrative to “measurements of complete original candidate streams.” Preserve completeness, original ordering, CPU/state measurements and the unanswered status. Do not reinterpret this as exported-term checking.

## Claim tone, coherence and protected material

J→C→F→X review found stable terminology for parent/branch ownership, native/reference execution, source/post-export boundaries, fallback, requested artifacts and service versus native resource accounting. The architecture caption uses the same prefix/suffix/branch concepts as the body. No math notation with drifting meaning appears. Four introduction contribution references are useful anchors; no extra forward-reference finding is issued. Related work repeats comparator identities for credit and differentiation, not as redundant material to delete. RQ evidence blocks retain exact question wording, procedure, metric references and honest unanswered conclusions. Missing quantitative details remain explicit result slots, not invented results.

Claim-tone scan found no redundant hedge stack or apology requiring removal. The statements rejecting novelty for existing techniques, bounding behavior under wall-time limits, excluding unsupported boundaries, and retaining negative/mixed results carry scientific scope. Do not delete them as self-attack. BOOTSTRAP present-tense system descriptions are allowed; X4 does not authorize replacing them with future-tense plans. Native behavior preservation is qualified by qualification, interface scope and resource-bound measurement, so no universal equality rewrite is warranted.

All numbers, four exact RQs, 12 result slots and citations are protected. Strong warm baselines and native logical/serialized reuse remain; CPU alternatives remain; device setup, transfer, synchronization, qualification/online checks and CPU fallback costs remain. Source verification and post-export checking remain separate, as do full GPU Lean checking, metadata primitives and certificate proving. Direct-user Lean+SMT acceleration intent, RTX5090-only GPU preference, gpt-6.1-sol preference and full OSDI research loop are preserved. No idea skill or scientific reframing was invoked.

## Disposition and next node

0 Must-fix, 3 Should-fix, 2 Consider. Category counts: C2/J6 1, J6/F8 1, J5/C1 1, J6/C2 1, J1/J3 1. Top changes are disambiguating proof admission, service admission, and CLI. Root disposition is pending for every suggestion. No source sentences changed, no Git/build actions occurred, and no compilation/page-count claim is made by this reviewer. Only this report was written. Root should apply accepted targeted changes, record rejected suggestions with reasons, verify preserved counts and compile before serial Round9.

Completed: 2026-10-09T17:49:33.785024+00:00.

Root disposition —2026-10-09T17:50Z: S1 and S3 applied with ordinary descriptions rather than new abbreviations/compound labels. S2's explanation intent accepted but its literal “without a proof term” rejected: Lean sorry admission uses an axiom-containing term, so root clarifies an unproved obligation admitted using sorry without incorrectly denying term construction. Existing REPL admissions reference and completion checks remain. C1 deferred because Design already explains quiescence and duplicating it in Intro adds no meaning. C2 applied only to the narrative, preserving source/candidate/full-stream scope and the result slot verbatim. Four sentences changed in separate subsections. Compileexit0/PDF8pages, unchanged4RQ/12slot/37cite/bib. No unsupported semantics/performance entered; central contribution remains complete preparation/isolation/equal-resource/heterogeneous verification. Next Round9.
