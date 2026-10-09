# Round 3 — Logic flow

Started: 2026-10-09 15:52:16 UTC. Completed: 2026-10-09 15:53:03 UTC (final review observation; root to append fix/build evidence).
Parent: BOOTSTRAP step-0003-20261009T132427+0000; serial iter-refine-writing-20261009T154400+0000. Objective: review global argument, causal links and intro-to-conclusion scope without changing the scientific contract.

Entry revision: c62e4276df4f87c3e8fa81cd758e2c6e7dcffa1e, observed with read-only git rev-parse HEAD. Reviewed the current working-tree paper, including preceding root writing edits. Loaded sources: docs/user-instruction.md; complete /workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md; complete docs/paper/main.tex (211 lines); complete docs/paper/references.bib. The middle of the first paper read was output-truncated, so lines 118–235 were read separately to complete coverage. No previous round reports or reviewer verdicts were read. No external search or experiment critique was performed.

Method: trace preparation sharing → native history distinction → independent branching → compatibility and bounded resources → four RQs → scoped conclusion. Treat present-tense system descriptions as intended completed implementation. Explicit result slots and unanswered RQs are accepted BOOTSTRAP evidence boundaries. All quantities, RQ meanings, citations and scientific framing are protected.

## Raw findings

### Must-fix

None. The introduction, design, evaluation and conclusion tell the same scoped story: independent native branches are assessed against competent bounded reuse, with behavior fidelity, candidate lifetimes and aggregate resources jointly determining value. The heterogeneous path is consistently conditional on preparation reuse and complete boundary costs. Result placeholders do not create a writing defect in this phase.

### Should-fix

1. **Design, Heterogeneous checking, line 123.** The sentence “During execution, enclosing native verification checks the resulting proof or requested artifact” reads as a universal validation step, but the same paragraph explicitly includes UNKNOWN and responses without artifacts. The final reference to behavior fidelity protects scope, yet the reader must infer how the universal-sounding sentence applies when no proof or artifact exists. **Concrete fix:** qualify that sentence with “where a proof or requested artifact is produced,” preserving the following rule that response fidelity also applies to UNKNOWN and artifact-free responses. Do not imply a second full CPU replay or introduce a new validation method. This is a local scope repair, not a request for new evidence.

2. **Implementation, Process and resource handling, line 140, in relation to Observable behavior and the introduction.** The argument identifies process-created timer/descriptor changes as a compatibility hazard, then describes separate descriptors and native counter accounting in implementation without explicitly reconnecting timer handling to adapter qualification. A reader can mistake inherited solver counters for preservation of every native resource limit. **Concrete fix:** add a short cross-reference explaining that supported-boundary qualification covers native resource controls affected by process creation, while wall-time outcomes retain the measured operational scope stated in Observable behavior and Limitations. Retain the distinction between inherited native counters and fresh service accounting; do not assert timer equivalence or invent a reset/restoration mechanism.

### Consider

1. **Design, Branch lifetime and cancellation, line 105.** “Candidate mutation should not extend the shared parent's lifetime” is broader than the next sentence's configured retention policy: useful observed candidate traffic can rationally influence retention. The intended isolation claim is clear from the surrounding paragraph, but its causal object could be more precise. **Concrete fix:** say candidate mutation must not make the shared parent retain speculative candidate state, leaving parent lifetime under configured retention policy. Accept only if root confirms this wording preserves the intended lifetime claim; otherwise retain the existing wording. No new retention policy is requested.

## Preservation and disposition

No paper, bibliography, Git, experiment or memory edits were made by this reviewer. Only this report was created. No finding orders deletion of technical content, quantitative changes, citation removal, RQ changes, or adoption of a new novelty position. Claims about implementation completeness were not challenged. Root owns accepted/rejected fixes, before/after locations, source diff and citation-count checks, compilation/page evidence, alternatives and decisions, and remaining concerns. Next node: root applies or records dispositions for Round 3, builds and verifies, then proceeds serially to Round 4 abstract/intro rebuild.

Operational note: the first report-write attempt used unavailable `python` and exited before writing; this report was then written with a literal shell heredoc.

Root disposition: both Should-fix items applied locally: artifact checking explicitly applies where one is produced, preserving UNKNOWN/no-artifact fidelity and no mandatory second CPU replay; timer/resource qualification references the existing operational wall-time limit scope without inventing resets/equivalence. Consider accepted as clarification of the existing retention-policy lifetime: mutation must not force parent retention beyond configured policy; the original independent-candidate lifetime claim remains, rather than being replaced by only no-speculative-state retention. Source/cite/RQ/quantitative checks pass, build exit0/PDF8pages. Next root Round4 complete opening procedure.
