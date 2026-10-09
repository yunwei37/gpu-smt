# Round 3 — Logic flow

Started: 2026-10-09 19:10:55 UTC. Completed: 2026-10-09 19:11:54 UTC.

Parent node: BOOTSTRAP step-0004-20261009T183603+0000, serial writing run iter-refine-writing-20261009T190400+0000. Objective: read the complete current paper and review claim support, argument links and the same story from introduction through conclusion without changing the scientific contract.

Entry revision: HEAD `3b035d29182f676ccfe2eaba8a483af5aa9cd0b3`, with current working-tree modifications to `docs/paper/main.tex` and `docs/paper/main.pdf`. This review assesses the complete working-tree source, not HEAD or a diff. Sources read completely: `docs/user-instruction.md`, `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`, and all 219 lines of `docs/paper/main.tex`. A numbered reread supplied finding locations. No external sources or novelty review were used.

Method: trace preparation opportunity → native behavior/history distinction → supported branch boundary → independent lifetime/bounded placement → qualification → four RQ evidence blocks → discussion/conclusion. Treat completed-system prose as intended submission prose and result placeholders as deliberate missing evidence. Check specifically for hidden claims of successful acceleration, universal resource-bounded equivalence, cold-only comparisons, and conflation of source verification with exported checking.

## Raw findings

### Must-fix

None. No scientific-contract defect requiring a change to RQ meaning, scope, numerical results, or protected qualifiers was identified.

### Should-fix

**S1 — Evaluation / Preparation sharing, lines 174–176; Design / Preparation boundaries, line 99.** The characterization separates exact-result reuse, ordered-prefix sharing and native-environment sharing, but does not explicitly connect these categories to the design's stricter branch-eligibility rule. A reader can carry environment-level reuse directly into “aggregate achievable sharing,” although an equivalent environment alone does not establish the matching native preparation required earlier. Concrete suggestion: add a short bridge after the reuse taxonomy: “Environment-level reuse characterizes the established reuse opportunity; branch-eligible sharing additionally requires the preparation and boundary conditions in Section [Preparation boundaries].” Add a subsection label if needed. This clarifies existing distinctions; do not change the RQ or introduce a new eligibility policy.

**S2 — Evaluation / Behavior and isolation, line 181; Design / Observable behavior, line 108; Implementation / Native adapters, line 133.** The design makes supported-path residual mismatch invalidate fidelity and the implementation excludes adapters failing qualification, while the RQ2 closing condition asks only that residual differences be “explained.” Explanation is necessary but should not read as sufficient to admit a divergent path to the service frontier. Concrete suggestion: append a clause stating that the results identify the qualified supported paths and preserve mismatches from excluded paths, with fidelity assessed under Section [Observable behavior]. Keep the honest unanswered placeholder and the native wall-time qualification. Do not claim zero mismatches or alter the existing rejection rule.

### Consider

**C1 — Implementation / Device path, line 151; Design / Observable behavior, line 104.** “Preserve output identity” refers to a matched checking operation, whereas native artifact fidelity permits different valid representations. These are compatible comparisons, but the levels can be confused during the move from qualification to complete verification. Concrete suggestion: qualify the operation comparison as “operation-level output identity,” or add a short reference to the separate interface-level artifact criterion. This is a local clarification, not a request to demand byte-identical native models or proofs.

## Argument assessment and preservation checks

The paper maintains a coherent bounded claim: native preparation may be worth sharing, independent candidate execution may preserve native behavior and improve the service frontier, and heterogeneous execution must improve remaining complete work after reuse. The conclusion does not claim an established win before results exist. Preparation/history motivation is reflected in untouched suffixes, no added scopes, qualification controls and the RQ2 matrix. Memory motivation is reflected in retained-state budgets, proportional fleet memory and dirty-page/lifetime explanations in RQ3. The device motivation is reflected in profile-selected dynamic operations, strongest CPU comparisons, explicit source/post-export boundaries and all device/fallback costs in RQ4.

All four numbered RQs remain read-only and unchanged. Lean and SMT-backed complete verification, RTX 5090, strong bounded warm services, native logical/serialized reuse, full frontend/setup/transfer/fallback costs, failed attempts and honest result placeholders remain intact. No claim that universal wall-time response equivalence follows from inherited counters was found. No scientific-contract intervention is requested.

## Applied/rejected fixes, validation and handoff

This reviewer made no paper edits, so no applied or rejected source fixes, before/after source changes, citation-count changes or numerical changes exist in this review. The only filesystem change is this report. No Git mutation, compilation, external search, memory-file change or branch operation was performed. Root owns decisions on S1, S2 and C1, source patches, round diff, citation/number checks and compilation/page evidence. Those application records can be appended here by root.

Alternative considered: interpreting incomplete result placeholders or intended present-tense implementation statements as defects. Rejected because the active BOOTSTRAP writing contract requires completed submission prose and explicit missing evidence rather than fabricated results or future-tense plans.

Remaining concerns: result support is intentionally absent and explicitly marked; it must be supplied by the experiment/evidence workflow, not this writing review. Next node: root applies accepted Round 3 clarifications, compiles and validates, then executes the complete Round 4 abstract/intro rebuild procedure serially.

Root disposition 2026-10-09T19:13:12.870274+00:00: appliedS1 with existing preparation-subsection label and a local environment-sharing versus supported-branch bridge inRQ1. AppliedS2 by retaining residual explanation and explicitly retaining divergent-path exclusion inRQ2closing. AcceptedC1 with local reference from operation-output comparison to separate native-artifact fidelity. These express existing distinctions; no new eligibility policy, altered artifact oracle or RQ meaning. Fresh compile exit0/8pages(round3-build.log); source diff preserves all numbers,39citations,12resultslots and4RQstrings. No data/claim invented. Round complete,nextRound4 full rewrite procedure.
