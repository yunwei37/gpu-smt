# Round 1 — micro structure review

Started: exact dispatch/review-start timestamp was not captured. Review and report-writing were observed underway by the clock reading 2026-10-09 15:49:06 UTC; the previous 15:49 minute label was an approximate reviewer observation, not a verified assignment time. Completed: 2026-10-09 15:49:06 UTC.

Parent: BOOTSTRAP step-0003-20261009T132427+0000 / iter-refine-writing-20261009T154400+0000. Reviewer: serial writing_structure subagent. Objective: complete-paper Levels 2–3 paragraph-role and within-paragraph flow review. Entry baseline supplied by root: `c62e4276df4f87c3e8fa81cd758e2c6e7dcffa1e`; current revision includes root's two native-adapter method clarifications and Round 0 Background/Motivation ownership cleanup. Root reports Round 0 build exit 0 and eight-page PDF. This reviewer performed no Git operation or build.

## Read scope and method

Read `docs/user-instruction.md` FIRST again, then the entire current `docs/paper/main.tex` (all sections, figure, four RQs and result placeholders). The complete iter-refine-writing and check-paper-structure-flow skills, full-paper-12p reference, linked abstract-intro-structure reference and bibliography were read in the preceding serial review and remain in context; they were not redundantly re-read. No Skill tool is available. Applied the loaded full checklist for paragraph roles, topic sentences, one idea per paragraph, why-before-what, old-to-new flow, subsection title conventions, abstract/intro correspondence and RQ opening/closing. Scope is the intended OSDI full paper, with BOOTSTRAP present-tense and result-placeholder preservation.

## Assessment and correspondence

Introduction roles are separately present in order: background; preparation/isolation problem; native-history root cause; established reuse and unresolved comparison; separable insight; three realization challenges; system/methods/results placeholder; contributions. The optional root-cause paragraph is justified because the insight separates preparation from history; the challenges paragraph is justified by runtime safety, resource handling and bounded memory. The system paragraph answers those challenges through supported boundaries, untouched suffixes, separate communication/accounting and bounded lifetimes.

Abstract sentences 1–8 map respectively to intro background, problem, cause, established reuse, insight, challenges, system, and methodology (the final two map to the system paragraph). Its final result placeholder maps to that paragraph's result placeholder. No concept debuts in the abstract. All four Evaluation evidence blocks repeat the established RQ meaning at their opening and end explicitly unanswered with an evidence TODO. No orphan experiment, silently answered RQ or scientific-contract defect was found. Subsection titles are parallel descriptive noun phrases. Topic sentences generally introduce the role of each paragraph; design subsections generally establish the reason before mechanism. No Must-fix micro defect was found.

## Raw findings

### Should-fix S1.1 — MICRO / FLOW: Design, Heterogeneous checking, second paragraph (main.tex:123)

Problem: the nine-sentence paragraph starts with semantic preservation and qualification, then switches after the response/artifact fidelity sentence to fallback and end-to-end cost accounting. These are distinct paragraph roles; the final timing-boundary distinction is harder to see within the long compatibility paragraph.

Concrete fix: split immediately before “Unsupported work returns to CPU execution”. Keep qualification, enclosing native verification, no mandatory second CPU replay, UNKNOWN and artifact scope in the first paragraph. Start the second paragraph with the existing unsupported-work sentence, then retain complete-cost components and the resident-device versus complete-checking distinction. The existing sentences already supply suitable topic sentences; no technical rewording or deletion is needed.

### Should-fix S1.2 — MICRO / FLOW: Implementation, Native adapters, first paragraph (main.tex:129)

Problem: the paragraph combines concrete native-driver construction (language, CLI-owned context and creation order, original commands) with a separate qualification procedure and diagnostic/admission policy. The eight-sentence block obscures that qualification is a second component of the method rather than another retained-context detail.

Concrete fix: split immediately before “Qualification compares fresh driver execution”. Preserve the first three construction sentences together and retain all five qualification/admission sentences as the second paragraph. In particular, retain same-source metadata discrimination, visibility of every response difference and the rule that rejected adapters are excluded from prepared-state service execution.

### Consider C1.1 — MICRO: Abstract final result placeholder (main.tex:20)

Problem: the abstract methods sentence includes heterogeneous checking, but its result placeholder names only service latency/throughput/memory/behavior, while the corresponding introduction placeholder also reserves measured device-benefit scope. This is a placeholder correspondence asymmetry, not a missing empirical result.

Concrete fix: add measured heterogeneous scope to the abstract's existing result placeholder, mirroring the introduction placeholder without introducing values, claiming benefit or modifying RQ4. Alternatively retain current wording until the eventual result sentence if root prefers minimal placeholder changes; record the choice.

## Preservation, alternatives and caller disposition

No paper, bibliography, citation, quantitative value, RQ wording, mechanism or claim was edited. Result placeholders and present-tense intended system description remain intact. No experiments, build, Git mutation or memory update occurred; only this report was written. Splitting the long system introduction paragraph into new role paragraphs was considered unnecessary because its system/method/result material belongs to the prescribed single role. No fabricated rewriting is recommended.

Root will append each finding's applied/rejected disposition, any before/after locations, compilation/page evidence and residual concerns. Recommended next node: Round 2 section conventions after root disposition/build.

Root disposition: both Should-fix paragraph splits applied exactly at the semantic boundaries without changing any sentence/value/citation/qualifier: device qualification vs full-cost accounting, native construction vs admission. Consider abstract placeholder expansion deferred: its methodology already states complete5090 costs and the corresponding intro resultslot includes measured device scope; final results will propagate then. Root compile exit0/PDF8pages; actual source splits verified. FourRQ wording/12slots/37cite expressions preserved. Next Round2.
