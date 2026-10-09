# Round 6 — sentence structure, read-only

Started 2026-10-09T21:55:16+0000; review completed 2026-10-09T21:55:31+0000; report completed 2026-10-09T21:56:49+0000. Parent: BOOTSTRAP step-0005-20261009T194100+0000 / iter-refine-writing-20261009T213300+0000.

Objective: review sentence mechanics while keeping scientific meaning fixed. Entry and completion main.tex SHA-256: `faaa4edacea11d857ff39521e2aa921626bbb5a0332c9e6355e2b4b579dc05ae`. No Git operation or evidence revision inspection was performed under the assignment's restrictions.

Sources read in order: docs/user-instruction.md; full actual filesystem /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md; full actual filesystem /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md; all 236 lines of docs/paper/main.tex. Truncated whole-file output was recovered by rereading lines 1–139, including the omitted lifetime/placement paragraphs. No old reviews, code, canon or evidence sources were read.

Method: examine every prose paragraph and caption for clause punctuation, fragments, modifier attachment, weak openings, subject/verb proximity, passive actors and three-or-more short declaratives. Diagram labels, explicit numbered goals/RQs and contribution lists retain their appropriate label/list status. Completed-system present tense and all twelve result placeholders are authorized; missing measurements are not findings. No word-choice or scientific revisions are proposed.

## Must-fix

None. No fragment, dangling modifier or material sentence-level ambiguity was found.

## Should-fix

### S1 — Design architecture caption, L105

Quote: “Normal completion releases private state after returning native responses; unsupported boundaries use native execution.”

Problem: semicolon joins independent clauses.

Fix: “Normal completion releases private state after returning native responses. Unsupported boundaries use native execution.”

### S2 — Design / Observable behavior, L117

Quote: “This preparation retains the candidate's accepted context without inserting preceding alternative-candidate suffixes; history within the candidate's own native session remains part of its suffix.”

Problem: semicolon joins independent clauses.

Fix: “This preparation retains the candidate's accepted context without inserting preceding alternative-candidate suffixes. History within the candidate's own native session remains part of its suffix.” Preserve exclusion of other candidate history and inclusion of within-candidate history.

### S3 — Evaluation / Experimental setup, L182

Quote: “Lean outcomes include unfinished proof obligations and admissions as well as frontend diagnostics; a successful tactic screen requires the enclosing declaration or source checking stage before it counts as an accepted proof.”

Problem: semicolon joins independent clauses.

Fix: “Lean outcomes include unfinished proof obligations and admissions as well as frontend diagnostics. A successful tactic screen requires the enclosing declaration or source checking stage before it counts as an accepted proof.” Preserve the tactic-screen/declaration/source distinction.

### S4 — Related work / Persistent verification state, L220

Quote: “These existing mechanisms strengthen the native-reuse comparison; failure collection and saved-state execution are not service novelty.”

Problem: semicolon joins independent clauses.

Fix: “These existing mechanisms strengthen the native-reuse comparison. Failure collection and saved-state execution are not service novelty.”

### S5 — Design / Heterogeneous checking, L138

Quote: “A speedup for a checking operation with its data already on the device is reported separately from complete checking.”

Problem: thirteen words separate subject head “speedup” from finite verb “is.” The qualifier must remain, but two intervening modifiers delay the verb.

Fix: “We report a checking-operation speedup separately from complete checking when the operation's data is already on the device.” The on-device condition still scopes the operation measurement.

### S6 — Design overview, L109

Quote: “A candidate first selects a prepared state approved by the service and a supported native boundary (Figure~\ref{fig:architecture}). The parent owns the immutable preparation, while each branch owns candidate mutation and its lifetime. A supported branch executes on CPU, with supported device operations where available. An unsupported boundary uses native execution.”

Problem: four short declaratives give connected ownership/dispatch decisions a note-like rhythm.

Fix: retain the first sentence, then use “The parent owns the immutable preparation, while each branch owns candidate mutation and its lifetime and executes on CPU with supported device operations where available. An unsupported boundary uses native execution.” Do not imply unsupported boundaries create branches.

## Consider

### C1 — Implementation / Process and resource handling, L155

Quote: “The parent stays quiescent and never executes candidate suffixes. Branch communication uses separate descriptors, and the service reaps children after response, cancellation or failure. Native solver resource counters are distinguished from service elapsed and CPU accounting.”

Problem: these three short declaratives follow another short implementation statement; the paragraph has a note-like rhythm.

Option: “The parent stays quiescent and never executes candidate suffixes, while branch communication uses separate descriptors. The service reaps children after response, cancellation or failure and distinguishes native solver resource counters from service elapsed and CPU accounting.” Keep the copy-on-write sentence/citation intact. Optional because the second sentence becomes longer.

### C2 — Implementation / Device path, L164

Quote: “A CPU reference and GPU implementation consume the same identified input and preserve output identity for each supported checking operation. Native artifact fidelity follows Section~\ref{sec:behavior}. Complete verification includes CPU fallback and device/runtime costs.”

Problem: three clear but consecutive short declaratives.

Option: retain the first, then use “Native artifact fidelity follows Section~\ref{sec:behavior}, and complete verification includes CPU fallback and device/runtime costs.” Do not infer causality between fidelity and cost accounting.

### C3 — Related work / Persistent verification state, L218

Quote: “Persistent Lean environments and native proof-state snapshotting retain elaborated context across attempts~\cite{repl,leanSnapshot}. Stock Lean also saves full elaboration or post-import snapshots~\cite{leanIncremental}. Kimina provides bounded warm verification with environment reuse~\cite{kimina,kiminaPaper}. These mechanisms provide the direct comparison for preparation reuse.”

Problem: four consecutive short declaratives read like a catalog; separate citations and explicit competitors also justify the existing structure.

Option: combine only the middle pair: “Stock Lean also saves full elaboration or post-import snapshots~\cite{leanIncremental}, while Kimina provides bounded warm verification with environment reuse~\cite{kimina,kiminaPaper}.” Preserve all citations and the bounded-warm competitor.

## Disposition, preservation, limits and next node

Raw findings: 0 Must-fix, 6 Should-fix, 3 Consider. No fixes applied or rejected by this read-only subagent; parent records each disposition. Top three changes: L117 clause split, L182 clause split and L138 subject/verb repair. Period splits are the least invasive punctuation alternative. Numbered design-goal colon is valid. Diagram-label colons and the imperative separator “End branch; release private state” are not narrative independent-clause issues.

No weak “It is / There are” opening, inappropriate narrative colon or dangling modifier was found. Obvious-actor methodology passives remain. Distinct scope-bearing statements were not automatically merged.

All numbers, four RQ meanings, native resource/service accounting, responses/artifacts, fallback, wall-time qualifiers, full-source/post-export/tactic-screening distinctions, strong native warm-cache and CPU comparisons and RTX 5090 are protected. All proposed changes preserve them and all twelve placeholders. No scientific-contract defect is asserted.

Only this report was written; paper/source/canon/code/memory are unchanged. No builds, native reruns, compilation or page-count check were performed. Parent must apply accepted fixes, diff-check numerical/citation/technical preservation, compile and verify before serial Round 7. A first report-writing command failed because `python` was unavailable and changed no file; the report was then written using a shell heredoc.

## Root disposition 2026-10-09T21:57:37.774183+00:00

Applied S1–S4 period splits retaining every clause; S5 concrete author subject preserves resident-device scope; S6 joins ownership with supported execution and retains separate unsupported fallback. Accepted C1 explicit reaping/accounting actor, C2 joins fidelity and full-cost clauses without causal inference, C3 combines stock snapshots/Kimina capability clauses with all citations retained. No technical deletions/quantitative changes. Source diff reviewed;44citecommands/23entries/12slots/fourRQ preserved. round-6-build.log exits0/eight pages. All9 findings individually accepted. Root retains native quiescence, lifetime/device cleanup, native counters vs service CPU and fullchecking boundaries. Next fresh Round7.
