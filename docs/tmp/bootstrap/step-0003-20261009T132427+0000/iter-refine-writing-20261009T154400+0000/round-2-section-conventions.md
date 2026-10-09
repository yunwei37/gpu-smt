# Round 2 — section conventions

Timing: exact dispatch/review-start timestamp was not captured; the first clock observation after the complete read was 2026-10-09 15:50:25 UTC. Review completed at the observed clock reading 2026-10-09 15:50:44 UTC, before report serialization.

Parent: BOOTSTRAP step-0003-20261009T132427+0000 / iter-refine-writing-20261009T154400+0000. Reviewer: serial writing_structure subagent. Objective: complete-paper section-convention review. Entry baseline supplied by root: `c62e4276df4f87c3e8fa81cd758e2c6e7dcffa1e`. Current paper includes the native-adapter method clarifications, Round 0 Background/Motivation cleanup and Round 1 two paragraph splits with sentences unchanged. Root reports Round 1 build exit 0 and eight-page PDF. Root deferred abstract result-slot expansion to final-result propagation explicitly.

## Read scope and method

Read `docs/user-instruction.md` FIRST again, followed by the entire updated `docs/paper/main.tex`. Applied the complete loaded check-paper-structure-flow procedure, its full-paper-12p template and linked abstract-intro-structure reference, all read in full in Round 0 and retained in context. The complete iter-refine-writing skill and bibliography were also read in Round 0. No Skill tool exists; actual reads provide the procedure. A read-only Python count measured the abstract. No Git, experiment, build or paper edit was performed. BOOTSTRAP present-tense and placeholder policy remains in force; this is an intended OSDI full paper rather than an eight-page workshop.

## Complete convention checks

| Item | Finding |
|---|---|
| Abstract length and form | One paragraph; 214 whitespace-delimited words before the result slot, 227 including its rendered `[RESULT: ...]` marker and text. Both are within the 200–300 full-paper convention. Eight prose sentences plus one result placeholder follow the nine-slot structure with root cause and challenges included. |
| Abstract/introduction relationship | Context, problem, cause, existing reuse, insight, challenges, system and methods align with the corresponding introduction roles. Results remain explicit placeholders. The already logged Round 1 abstract/device-slot Consider remains deferred; no new duplicate finding is raised. |
| Introduction roles | Separate background, problem, root cause, existing solutions/unresolved comparison, insight, challenges, system/methods/results and four-item contributions are present in order. Root cause and challenges satisfy their inclusion conditions. No required roles are merged. |
| Background and Motivation | Background contains substrate prerequisites and Motivation holds the execution-history/fidelity inference after Round 0. Motivation ends by linking observations to Design. Explicit evidence placeholders reserve real characterization; none is misrepresented as measured data. |
| Design opening | Three named numbered goals derive from preparation/isolation and native-history motivation. Overview, architecture and a typical operation are present. Goals map to behavior/isolation and equal-resource evidence. |
| Design decisions | Five noun-phrase subsections cover boundaries, behavior, lifetimes, placement and heterogeneous checking. Mechanism-independent design is separated from concrete C++/Linux/NVIDIA implementation details. |
| Implementation | Opening maps design to adapters/processes/service; three component subsections realize native execution, lifetime/resource handling and device path. Final paragraph names Linux integration and C++ SMT implementation. No unsupported code-size value is invented to fill the optional engineering summary. |
| Evaluation overview | Exactly RQ1–RQ4, unchanged scientific meaning, listed before setup/results. Claim/contribution/design-goal mapping is explicit. Setup and Limitations are outside the count. |
| RQ evidence ownership | Exactly one primary subsection per RQ. Each opens with the RQ, describes experiments/controls, reserves results and closes explicitly unanswered with evidence TODO. No orphan experiment or misplaced primary evidence block. |
| Subsection titles | Descriptive noun phrases with parallel form; no question titles, verb instructions, claims or repeated system name. |
| Related work | Four topic groups; comparisons distinguish persistent state, caches, prepared execution and heterogeneous checking. Paragraphs are comparative rather than per-paper summaries. |
| Discussion | Broader connection of preparation sharing to resource use and requirements for another verifier; no displaced Limitations section. |
| Conclusion | One paragraph; restates thesis and mechanism/resource scope, reserves final findings across all four RQs, introduces no new information or future work. |

## Raw findings

**Must-fix:** none.

**Should-fix:** none.

**Consider:** no new actionable section-convention finding. Round 0 page-budget consideration and Round 1 abstract result-slot consideration remain recorded and explicitly deferred by root; repeating them as new findings would not improve the serial review.

No rewriting is recommended solely to demonstrate activity. Existing contributions place characterization before design; this is coherent with a preparation-opportunity characterization motivating the design and does not warrant mechanical reorder. Missing final results remain honest placeholders and are not treated as completed answers. Final-submission empirical completeness belongs to later research gates.

## Preservation and caller disposition

No paper, bibliography, citation, number, RQ, baseline or claim changed. Only this report and a Round 1 timing-provenance correction were written: the earlier approximate 15:49 start label is now explicitly an observation rather than a verified dispatch. No scientific content in that report changed. No Git mutation, build, experiment or memory update occurred. Root will append disposition (no new fixes), its compilation/page evidence, remaining concerns and next node. Recommended next node: Round 3 logic flow after root verification.

Root disposition: no new findings and no cosmetic edit manufactured. Build exit0/PDF8pages; source unchanged this round, so no claimed rewrite; fixed4RQs/12slots/37cite expressions retained. Abstract count is descriptive draft text, not experimental evidence. Next fresh Round3 logic reviewer.
