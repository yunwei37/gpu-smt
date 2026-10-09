# Round 1 — Micro structure

Review timestamp: 2026-10-09T19:06:14+0000 (first recorded timestamp after source reads). Review completed: 2026-10-09T19:07:12+0000. Parent: BOOTSTRAP step-0004-20261009T183603+0000, serial iter-refine-writing run 20261009T190400+0000. Objective: read-only paragraph-role and internal-flow review of the intended completed submission; the root applies fixes and supplies compilation evidence afterward.

Entry source: `docs/paper/main.tex`, SHA-256 `2b3f44ef0a13df60073be93af758805601b1df0f09f06534b2a5bb78b0fe6672`. No Git operations were performed. No paper or evidence source was changed.

## Reads and method

Read `docs/user-instruction.md` first; then the full actual `iter-refine-writing/SKILL.md`, `check-paper-structure-flow/SKILL.md`, its `references/full-paper-12p.md`, and `rewrite-abstract-intro/references/abstract-intro-structure.md`, all under `/workspaces/.agent-state/codex/skills`. The abstract/intro reference is in rewrite-abstract-intro, as the full-paper template specifies; the similarly named path under check-paper-structure-flow does not exist. Read the complete current 217-line `docs/paper/main.tex`; re-read lines 70–110 separately because the aggregate tool output had truncated that interval. No Skill tool exists in this session; the full on-disk instructions were loaded directly instead of claiming a fictional tool invocation.

Mapped all introduction paragraphs and abstract sentences to required roles, checked topic sentences and one-idea progression throughout every section, and checked all four RQ blocks for explicit opening and honest unanswered closing. Reviewed as an intended completed BOOTSTRAP submission: present-tense system and implementation descriptions are valid. Missing empirical results remain placeholders; this review does not turn system descriptions into plans or invent results.

## Raw findings

### Must-fix

**M1 — MICRO, Abstract, lines 15 and 19.** The abstract has more than the prescribed 7–9 sentence slots: the existing-solutions role occupies two sentences, and the methodology role occupies two more. The underlying roles are present and in the right order; this is a sentence-role correspondence defect rather than a missing idea. Combine the two sentences at line 15 into one sentence retaining established reuse and the unresolved matched-resource comparison. Combine the two sentences at line 19 into one methodology sentence retaining Lean, SMT-backed candidate streams, competent bounded warm/cache services, native logical or serialized reuse, RTX 5090, and complete setup/transfer/fallback accounting. Keep the result placeholder as its own final slot. Do not delete device scope or competitor strength to shorten the abstract.

### Should-fix

**S1 — FLOW, Background / Prepared native state, line 57.** The paragraph moves from solver persistence to deterministic resource limits to operating-system branching without announcing their common subject. These are the native interface and runtime properties later qualification relies on, but the opening currently covers only the solver command interface. Add an opening/topic sentence identifying these interface and runtime properties, then preserve the existing cited explanations. Alternatively split persistence/resource limits and process branching into short paragraphs with explicit topic sentences; prefer the first option to avoid unnecessary fragmentation.

**S2 — MICRO, Motivation / Preparation and candidate lifetime, line 61.** The first paragraph introduces expensive preparation sharing, places its characterization placeholder, then switches to failed-attempt lifetime capacity. These are related but distinct measured costs. Make the topic sentence cover both preparation reuse and candidate lifetime, retaining the placeholder and the failed/incomplete/resource-exhausted cases. This improves one-idea coherence without moving evidence or inventing measurements.

**S3 — FLOW, Related work / Verification caching, line 204.** The topic label and first two sentences discuss fine-grained caching and competent warm services; the last two switch to incremental SMT execution history. The paragraph lacks a bridge explaining the relation. Add an explicit bridge that caching and session reuse retain different parts of verification work, then keep the native-interface citation and ordered-history distinction. Alternatively move those two sentences into the persistent-state group, preserving their citation; the bridge is the smaller change.

### Consider

**C1 — MICRO, Implementation / Process and resource handling, lines 144 and 148.** Cancellation tests and memory measurement are evaluation descriptions embedded among implementation mechanisms. They are relevant instrumentation, but their topic sentences currently announce tests/measurement rather than what the implementation records. Reframe the openings around instrumentation that records progress/reaping and parent/child memory/lifetimes, retaining every recorded quantity and the distinctions they enable. No need to move the content if this framing makes the implementation role clear.

**C2 — FLOW, Evaluation / Experimental setup, line 169.** The paragraph groups raw outcome retention, repeat-order control, performance metrics, cost coverage, throughput-versus-latency interpretation, CPU affinity/load and a setup placeholder. Each sentence is individually clear, but the topic sentence announces only outcome retention and comparison repetition. Split before the affinity sentence to give CPU placement/load its own paragraph, or broaden the opening to cover measurement and run controls. Preserve complete-cost coverage and uncertainty details.

## Passing checks

Introduction has eight distinct required/conditional roles: background (24), problem (26), structural cause (28), established solutions and unresolved comparison (30), independent insight (32), three realization challenges (34), system/method/result slot (36), and four concrete contributions (38–44). The structural-cause and challenges paragraphs are warranted by the mechanism paper. The system paragraph answers runtime safety with supported quiescence/fallback, resource handling with inheritance plus branch-owned communication/separate service accounting, and memory with bounded prepared-state lifetimes. No paragraph-role merger is needed. Existing-solutions prose appropriately presents strong reuse mechanisms without fabricating their inadequacy.

Design subsections generally open with the reason or interface property and then explain the mechanism. The preparation boundary, behavior contract, lifetime/cancellation, bounded placement and heterogeneous checking each maintain a coherent topic. Architecture walkthrough starts from a candidate and progresses through shared ownership, branch execution and fallback. Native behavior's Lean/SMT cases support the interface definition rather than introduce separate arguments.

All four evaluation evidence blocks explicitly begin `RQ1 asks`, `RQ2 asks`, `RQ3 asks`, and `RQ4 asks` and close with `RQn remains unanswered` plus the corresponding evidence requirement. The exact four numbered scientific questions remain intact. Setup and Limitations remain outside the RQ count. The unanswered closes are correct for BOOTSTRAP and should not be replaced with invented positive or negative answers. Conclusion restates preparation/history separation, independent lifetimes and matched service benefit, with a final four-RQ result placeholder; no new result is introduced.

## Meaning preservation and decisions

Recommended edits are role/transition/sentence-boundary changes only. Protect Lean and SMT source/session boundaries, RTX 5090, strong bounded native warm/cache and serialized-state competitors, matched CPU/memory resources, original ordered suffixes, response/artifact scope including UNKNOWN, deterministic-versus-wall-time distinction, fallback and all complete costs. Preserve every citation and result placeholder, all four RQ meanings, and all numeric values. No finding calls for removing scientific content, changing scientific claims, or converting completed-system prose into future work.

No fixes were applied or rejected by this read-only reviewer. Root should apply M1 and S1–S3 by default, record each decision on C1–C2, and append before/after locations, source diff/citation/number checks and compilation/page evidence. A bridge rather than paragraph relocation is recommended for S3 because it preserves surrounding topic-group balance with minimal change.

## Remaining concerns and next node

Empirical values and pinned configurations are still explicit result/setup placeholders, owned by the experiment workflow. They are not writing-round defects. This round makes no full empirical-submission readiness claim and performs no compile. Tree change consists only of this required report; no memory or Git changes were made.

Next: root applies these micro-structure fixes, compiles and verifies preservation, then launches serial Round 2 — section conventions. Round 2 should check abstract word count after M1, section-role boundaries, design goals, RQ overview and conclusion conventions.

Root fix/verification2026-10-09T19:08Z: appliedM1 by combining existing-solution sentences and methodology/device sentences while retaining every stated scope/cost/competitor and the result slot. AppliedS1/S2/S3 with local topic/bridge sentences in Background, Motivation and RelatedWork; no oldcontent removed. AcceptedC1 as instrumentation framing only, changing tests/measurement openings to instrumentation; acceptedC2 by splitting CPU affinity/load into its own setup paragraph. No subsection was rewritten wholesale, no numbers/citations/RQs/resultslots changed. Fresh compile exit0/8pages (round1-build.log); reviewed source diff,39citation commands/12resultslots and exact4RQ lines match baseline. AllShould/Consider findings explicitly disposed. Round complete,nextRound2.
