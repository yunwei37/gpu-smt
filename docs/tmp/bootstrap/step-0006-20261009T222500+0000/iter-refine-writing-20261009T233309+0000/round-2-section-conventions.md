# Round2 — section conventions

Started 2026-10-09T23:35:24+00:00; completed 2026-10-09T23:35:51+00:00. Parent: BOOTSTRAP step0006 WRITE_GATE / serial iter-refine-writing Round2, after root Round1 patches/compile. Objective: section-specific full-paper conventions, preserving intended completed-system tense, all four fixed RQs and all result slots.

Provenance and method: read `docs/user-instruction.md` first, then the complete current `docs/paper/main.tex` in two sequential source ranges, with the small truncated subsection fragment recovered by a separate 125–138 read. Reapplied the actual complete filesystem `check-paper-structure-flow/SKILL.md` and `references/full-paper-12p.md` read during Round0, and the linked complete `rewrite-abstract-intro/references/abstract-intro-structure.md` read during Round1. No Skill-tool invocation is claimed because this session has no such tool. Read-only Python counted abstract words/sentence endings from the current source; no native verifier, build, Git action or paper edit occurred. This is a section-convention review, not a claim of completed scientific results or submission readiness.

## Must-fix

None.

- **Abstract (main.tex:13–23):** one paragraph, 232 whitespace-delimited words including visible result-slot text, nine sentence-ending periods. This falls within the full-paper reference's 200–300-word and 7–9-sentence conventions. Sentence roles track the introduction's background/problem/cause/existing-solutions/insight/challenges/system/method/results order. The last sentence is an honest result placeholder, not an invented finding.
- **Introduction (25–46):** all required roles are separate and ordered. Optional root-cause and challenges paragraphs are appropriate because the insight answers a native-history cause and realization has runtime/resource/memory obligations. The system paragraph answers the challenges and retains methodology/results coverage. Four contribution items describe deliverables with section references; characterization-first order follows the causal opportunity-to-mechanism story and is not grounds to reorder or reinterpret the scientific contract.
- **Background and Motivation (48–72):** Background explains existing verification stages, outcomes and native-state machinery without claiming it as invented design. Motivation makes the preparation/lifetime and scope/history costs explicit with appropriate open characterization evidence slots, then links to Design. Missing final measurements are preserved as BOOTSTRAP slots rather than repaired with historical or fabricated values.
- **Design (74 onward):** opening names three goals linked to Motivation; architecture and operation walkthrough precede decision subsections. Preparation safety, observable behavior, candidate lifetime, bounded placement and heterogeneous checking each have need-before-mechanism content. The Round1 division now separates native reference definition from outcome/artifact comparison without losing the qualifications.
- **Implementation:** opens by mapping design to adapters/processes/service; concrete native parser/C++/Linux/container mechanisms are separate from Design. Platform and integration modes are stated in the closing paragraph. Code-size or further engineering facts cannot be supplied by writing refinement, and none is invented or required as a new scientific task here.
- **Evaluation:** the numbered overview contains exactly four established RQs; Setup and Limitations remain outside that count. Preparation sharing, Behavior and isolation, Latency/throughput/memory and Heterogeneous execution each state the corresponding RQ, describe its evidence/controls and retain an explicit unanswered closure with a result slot. Baselines, ablations and workload controls are subordinate to those questions; no orphan experiment or extra RQ was found. Four blocks remain open consistently with the current evidence contract.
- **Discussion, Related work, Conclusion:** Discussion concerns implications/extensions rather than duplicating the Limitations list. Related work has four topic groups, explains existing mechanisms and connects them to the matched comparison without claiming snapshot/fork/representation novelty. Conclusion is one paragraph, restates preparation/history separation and intended service effect, retains its result slot, and introduces no new mechanism or future-work agenda.

## Should-fix

None. No section-convention defect requiring a paper change was identified after the Round1 edits.

## Consider

None requiring a new change in this round. Prior optional architecture/page-budget issues belong to the root's Round0 disposition and are not reopened here. Further abstract shortening, paragraph polish or claim-tone changes belong to their scheduled later rounds, not this convention review.

Preservation and ownership: no change to RQ wording/meaning, quantitative values, scope hedges, baseline strength, native qualification, complete-verification boundaries or RTX5090 scope requested. No paper/canonical edits, baseline changes or builds. Root owns any disposition, diff/compilation evidence and next serial round; only this Round2 report was written.

Root disposition: no findings to apply; independently checked abstract/intro/design/evaluation grouping and protected native/complete/GPU scope. No paperchange;47citations/4RQ/12slots,8pages preserved. make exits0 (build-round2.log). Section conventions do not qualify missing experiments; fullambitiouscontract staysunfrozen. NextfreshRound3logicreview.
