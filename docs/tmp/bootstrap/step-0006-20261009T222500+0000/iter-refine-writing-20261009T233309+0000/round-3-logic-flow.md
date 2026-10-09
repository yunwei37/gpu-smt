# Round 3: Logic flow

Started: 2026-10-09 23:36:52 UTC. Completed: 2026-10-09 23:38:00 UTC.
Parent: BOOTSTRAP step-0006-20261009T222500+0000 / iter-refine-writing-20261009T233309+0000.
Objective: independent complete-paper writing review of argument coherence, preserving science, numbers and four established RQs.

Read docs/user-instruction.md first, then the complete /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md, complete docs/paper/main.tex (separately rereading lines 125–140), and complete docs/paper/references.bib. No external search or native execution: this is writing-only Round 3. Entry Git revision: 9e0663444b7e7e1d6f1798819883b7d24eefc954. Reviewed working-tree SHA-256: main.tex 438e7d5a7b7042e2ca5a3d57c9da52702ddebfcb4562beaf63c07feb96cfddd7; references.bib 97cae70d34ddd11566b9ef9d18c63488d79fc9a9956cb5643035a1d174e552e3. Git revision does not imply a clean tree.

Method: traced preparation sharing → independent lifetime → native-interface qualification → equal-resource service comparison → residual heterogeneous checking; compared each RQ evidence block with design and conclusion. Present-tense implementation is treated as intended completed submission. Missing results remain explicit placeholders.

## Must-fix

None found. The paper coherently distinguishes ordered preparation from logical equality, adapter qualification from branch qualification, source verification from post-export checking, and operation speedups from complete verification. Four RQ meanings are consistent.

## Should-fix

1. **Design / RQ2, main.tex lines 119–123, 128, 196–198.** Fidelity comparisons cover native outcomes, while cancellation can terminate before such an outcome and return a service failure. The distinction is implicit in separate instrumentation but not connected to RQ2's comparison. **Fix:** explicitly state in the RQ2 evidence block that completed attempts are compared for native responses/artifacts, while externally cancelled attempts are compared for termination/progress, cleanup and independence of surviving attempts. Preserve all raw outcome records and RQ wording.

2. **Architecture / bounded placement, lines 87–109, 130–133.** The figure's only explicit native-execution edge is an unsupported boundary, but placement also chooses native execution when locality is low or preparation cheap. **Fix:** add one overview sentence explaining that bounded placement may select native execution before qualification when retaining preparation is not worthwhile; boundary qualification separately governs whether a selected prepared state supports branching. This connects existing policy to existing diagram rather than adding an algorithm.

3. **Device design / Implementation / RQ4, lines 138, 166, 206–208.** Design separates pre-admission CPU qualification from required online checks. Later output-identity/reference-comparison language could imply compulsory CPU duplication of each GPU request. **Fix:** qualify later reference comparisons as device-qualification comparisons and cross-reference the design's online checking/accounting distinction. Preserve CPU fallback, semantic fidelity and all actual complete-path costs.

## Consider

1. **Discussion, line 216.** The fourth RQ's connection to the central argument stops at Evaluation. **Fix:** optionally add one sentence explaining that heterogeneous checking is assessed on the complete path remaining after preparation reuse under the same behavior and resource accounting. Assert no positive GPU finding.

2. **Implementation / setup / metrics, lines 152, 182, 186.** Measurement boundaries are clear individually but dispersed. **Fix:** optionally cross-reference the source-native and post-export boundary definitions from the metrics paragraph. Include costs only where they occur at the stated boundary.

## Disposition and preservation

No paper fixes applied: findings are returned to the parent for individual disposition and subsection-sized edits. No claims, numbers, citations, RQs or technical content changed. Only this report was written; no source/canonical/Git/memory edits, builds or native execution. Compilation/page checks belong to the parent after accepted fixes. The first report-write attempt used unavailable python and failed before writing; this report was then written with a shell heredoc.

Remaining concerns are explicit setup/result placeholders, outside this writing review. No invented values, future-tense implementation downgrades or scientific changes proposed. Next: parent applies/disposes of findings, checks preservation and compilation, then Round 4 abstract/intro rebuild.

Root disposition: all3Should accepted. Overview connects existing cheap/lowlocality native policy to boundary selection; RQ2 distinguishes completed-response comparisons from external cancellation's progress/cleanup/surviving-independence checks; implementation/RQ4 explicitly distinguish device qualification from charged required online checks. These are expressions of existing design, not new experiments/contract. Consider discussionGPU repetition deferred: RQ4 already states complete remaining-path/resource accounting and discussion refers matchedaccounting; no independent conclusion added. Consider metricscrossref deferred: setup boundaries/sourcepostexport distinctions already clear; avoids extraIOU. Subsection-sized reviewed patches, no numbers/citations/hedges/RQ removed;47cites/12slots remain. make exits0/build-round3.log,8pages. User goal and complete evaluationpromise unchanged; rootRound4 next.
