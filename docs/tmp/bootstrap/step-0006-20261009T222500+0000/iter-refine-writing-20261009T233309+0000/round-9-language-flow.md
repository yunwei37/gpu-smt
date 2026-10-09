# Round 9 — Flow and polish

Started: 2026-10-09 23:50:12 UTC. Completed: 2026-10-09 23:50:53 UTC.

Parent: BOOTSTRAP step-0006-20261009T222500+0000; serial WRITE run iter-refine-writing-20261009T233309+0000. Root reports Round 8 fixes and a nine-page build completed before this assignment; the reviewer did not independently execute or inspect a build. Objective: read-only flow/polish review of the complete current paper.

Read `docs/user-instruction.md` first, then reread the complete actual root `paper-writing-style/SKILL.md`, followed by complete current `docs/paper/main.tex` in two untruncated spans, lines 1–116 and 117–238. The style skill contains no linked supporting reference file; its inline examples and full checklist were read. No Skill tool is exposed, so the complete file procedure was followed directly under its read-only-subagent exception. Root iter-refine-writing instructions remain loaded from preceding serial reviews. Source SHA-256: `7c3312b17f81e04156d7116961e58ce15957187014bf96d1eebbe03bd468213e`. Read-only source counting confirms 47 citation calls and 12 result slots.

Method: assessed every paragraph and sentence against the full style checklist, focusing on known-to-new progression, concrete topic subjects, stress position, paragraph transitions and academic register. Checked causal connections without supplying results or interpreting missing evidence. Contribution lists and the four explicit RQs are permitted structured exceptions. BOOTSTRAP system/implementation/contribution present tense is intentional and not flagged.

## Must-fix

None. No broken flow requires a scientific-contract change.

## Should-fix

### S1 — Background, Verification stages and outcomes, line 52

Quote: “Solver responses include SAT for satisfiable queries, UNSAT for unsatisfiable queries, and UNKNOWN when the solver does not decide the query, and clients can request models, proofs or unsatisfiable cores when the configured backend supports them~\cite{z3api}.”

Problem: the newly explicit response definitions make the second “and” carry a substantial topic switch from response status to optional artifacts. Readers must hold the three definitions while parsing the client request capability.

Concrete fix: “Solver responses include SAT for satisfiable queries, UNSAT for unsatisfiable queries, and UNKNOWN when the solver does not decide the query. Clients can also request models, proofs or unsatisfiable cores when the configured backend supports them~\cite{z3api}.” Keep the next sentence connecting these outcomes and artifacts to the behavior section. This preserves all three definitions, all requested artifact classes, the backend-support qualification and the single citation call.

## Consider

### C1 — Implementation, Native adapters, line 154

Quote: “The Lean adapter retains accepted context and keeps branch-local proof construction independent.”

Problem: the preceding paragraphs discuss the SMT adapter, its parser boundary and its frontend measurement scope. An explicit transition would make the return to the second verifier easier to follow.

Concrete fix: “For Lean, the adapter retains accepted context and keeps branch-local proof construction independent.” Retain the remaining sentences on source snapshots, runtime workers and separate qualification unchanged. The current concrete-subject opening is already clear; this is optional paragraph-transition polish.

### C2 — Evaluation, Heterogeneous execution, line 206

Quote: “We identify whether each complete measurement begins with source verification or post-export checking. Post-export results answer only the latter boundary.”

Problem: the second sentence links backwards through the abstract “latter boundary,” rather than naming the established checking boundary. Its restriction is correct and must remain.

Concrete fix for the second sentence only: “Results from post-export checking therefore apply only to that checking boundary.” This starts with the known result class and ends with its protected scope restriction. Preserve the first sentence and all later strongest-CPU, operation-qualification and complete-interval wording. The existing wording is understandable, so the change is optional.

## Negative checks and rationale

The abstract follows service workload, native-history constraint, existing reuse, separation argument, mechanism and comparison in order. Introduction paragraphs each carry a coherent role and link preparation, execution history and resource frontiers. Design proceeds from placement through boundaries, behavior, lifetimes, memory and device work; implementation retains adapter qualification before reuse. Evaluation opens each evidence block with its fixed RQ and closes with an explicit unanswered condition rather than invented findings. Discussion, related work and conclusion retain the same scoped story. No orphan script-style experiment, register break, artifact diary, dangling modifier, ungrammatical fragment, independent-clause semicolon or prose em-dash requires an additional finding. No gratuitous transition word was added merely to make paragraphs seem connected.

Full quick-check coverage included opening deletion, nominalization, subject–verb separation, stress/topic positions, adverb precision, measurement hedges and pronoun antecedents. Necessary technical process nouns and protected scope qualifiers remain. Paired short sentences from earlier fixes are allowed; residual short declaratives generally distinguish technical stages, outcomes or conditions clearly. No hardcoded proposed-system name exists; cited verifier and baseline names remain intact.

## Disposition and preservation

Raw findings: 0 Must-fix, 1 Should-fix, 2 Consider. Three proposed improvements are separating response definitions from artifact requests, marking the SMT-to-Lean transition, and making post-export scope explicit. Applied fixes: none. Rejected fixes: none; root evaluates every finding. Sentences changed: 0. Only this report was written. No paper/source/canonical/Git/build/experiment changes occurred.

All recommendations preserve numbers, four RQ meanings, 47 citation calls, 12 explicit unfilled result slots, full verification, native warm/cache and strong CPU competitors, qualification, cancellation, matched CPU/memory, RTX 5090 and setup/transfer/fallback accounting. Protected hedges remain intact. Wider paragraph rewriting was rejected because the flow is already coherent and targeted changes suffice. No compilation or page-count claim is made by this reviewer.

Next node: root dispositions and applies findings, performs authorized compilation/preservation checks, then proceeds to serial Round 10 citation gate. No additional scientific-contract defect was identified.

## Root completion

2026-10-09T23:51:36.529080+00:00 — S1 applied separating query responses/artifact requests, all definitions and optional-artifact qualification retained. C1 applied to mark SMT-to-Lean transition. C2 applied to explicitly restate post-export result scope. Three local paragraphs changed; no numerical/citation/technical/RQ drift. Reviewed each patch, citecalls47/resultslots12; build-round9.log exit0/pdfinfo9pages. Actual reviewer scope/changes conform to verbatim human objective; no intended-system downgrade or claims of unexecuted work. NextRound10 citation gate.

Root correction duringRound10: initial S1 patch accidentally retained old can, producing Clients can also can request. Citation reviewer spotted the grammatical typo; root corrected to Clients can also request and recompiled exit0 in build-round9-correction.log before Round10 handoff. No new semantic change or scientific finding.
