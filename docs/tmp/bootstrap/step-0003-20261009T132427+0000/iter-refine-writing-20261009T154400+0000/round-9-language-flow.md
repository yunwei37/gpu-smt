# Round 9 — Language flow reviewer report

Parent: bootstrap step-0003 / iter-refine-writing-20261009T154400+0000. Serial reviewer after root reported Round8 fixes, build exit 0 and eight-page PDF. Objective: topic/stress positions, old-to-new sentence links, paragraph transitions and register consistency; scientific meaning is read-only.

Actual inputs read in full: docs/user-instruction.md; /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md; current entire docs/paper/main.tex. The combined output was truncated, so L38–106 was reread explicitly to cover the omitted middle. This is filesystem skill use, not a Skill-tool invocation. No interruption occurred during this review. Precise start timestamp was not captured; completion is recorded below.

Entry main.tex SHA-256: a93488097821a8eb972376e076a82e490166c9f1fc48c7324bff94aae1dd9a1a. Counts: 4 numbered RQs, 12 result slots, 37 citation commands.

Method: read every narrative paragraph and trace the backward link between consecutive sentences, identify the topic sentence and final stress position, and compare academic register across abstract, introduction, background, motivation, design, implementation, evaluation, limitations, discussion, related work and conclusion. Structural repetitions of the exact RQs and technical qualifications were treated as intentional anchors. No sentence was edited.

## Must-fix

None. No broken referent or missing logical connection makes the current argument unintelligible.

## Should-fix

1. Background / Verification stages and outcomes, L48: “Post-export checker replay begins after the source frontend has already run.” Problem: the paragraph moves from source verification stages to a narrower measurement boundary without an explicit contrast, although that distinction is important throughout the paper. Concrete fix: “By contrast, post-export checker replay begins after the source frontend has already run.” Preserve the following boundary sentence and both citations.
2. Evaluation / Preparation sharing, L170: “We compare original ordering with a control with unrelated work.” Problem: the repeated “with” interrupts the sentence's transition from original ordering to the control. Concrete fix: “We compare original ordering with a control containing unrelated work.” Preserve the preparation-depth clause, result slot and unanswered conclusion.

## Consider

1. Background / Prepared native state, L57: “Process branching shares existing memory through copy-on-write.” Problem: after persistent command state and resource limits, branching introduces a new subject without directly linking to retained state. Concrete fix: “Process branching shares this existing state through copy-on-write.” Preserve the separate handling of child timers, descriptors and runtime threads and the fork citation. The existing sentence is already understandable; root may prefer its explicit memory wording.
2. Implementation / Native adapters, L133: “Every observed response difference remains visible. This comparison separates interface incompatibility from differences caused by branching.” Problem: the outcome-retention sentence briefly interrupts the qualification comparison's explanation. Concrete fix: swap these two sentences, leaving their wording and all adjacent sentences unchanged. This puts comparison → diagnostic purpose → retained differences in sequence. Do not weaken the all-differences retention rule.
3. Implementation / Device path, L147: “Existing checker techniques include expression layouts with integer identifiers and delayed substitution...” Problem: this moves from included device/fallback costs to algorithmic novelty without a topic cue. Concrete fix: “For checker representation, existing techniques include expression layouts with integer identifiers and delayed substitution...” Preserve the citation and the explicit statement that their use does not establish a new checking algorithm.

## Preservation, dispositions and next node

Summary: 0 Must-fix, 2 Should-fix, 3 Consider. Most useful changes are the source/post-export transition, the ordering/control sentence, and the qualification sentence order. Register is otherwise consistent. A few short implementation sentences state discrete ownership and fidelity rules and should remain separate for precision. No additional paragraph reorganization or global rewrite is warranted.

All four exact RQs, 12 result slots, citation commands, numbers, scope-bearing hedges, honest unanswered findings, negative/mixed outcomes and limitations remain protected. Full source verification versus post-export checking, strongest warm and native logical/serialized baselines, solver UNKNOWN outcomes and artifacts, branch resource accounting, and all device setup/transfer/synchronization/online-check/CPU-fallback costs remain unchanged. BOOTSTRAP present-tense intended system descriptions remain allowed. Direct-user Lean+SMT acceleration, RTX 5090-only GPU choice, gpt-6.1-sol preference and full OSDI research intent are preserved. No idea skill or scientific reframing was invoked.

Every suggestion awaits root disposition; zero source sentences were changed. Only this report was written. No Git operations, builds or independent PDF/page claims occurred. Root should apply accepted subsection-local fixes, record decisions on every finding, compile and check protected content before serial Round10 citation review.

Completed: 2026-10-09T17:51:08.729175+00:00

Root disposition —2026-10-09T17:51Z: both Should-fix applied; C2 sentence order and C3 representation cue accepted. C1 deferred because explicit memory sharing is more precise than sharing generic state, which includes noninherited timers/descriptors needing separate handling. Three sentences locally rephrased and two reordered with all content retained. Buildexit0/PDF8pages; four exactRQ/12result slots/37cite expressions/bib unchanged. No quantitative or scientific claim changed. User scope preserved. Next serial Round10citation gap pass.
