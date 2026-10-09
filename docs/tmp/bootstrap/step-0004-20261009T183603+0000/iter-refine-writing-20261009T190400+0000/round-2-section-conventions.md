# Round 2 — Section conventions

Started: 2026-10-09T19:08:49+0000 (first recorded clock observation during review). Completed review: 2026-10-09T19:09:10+0000. Parent: BOOTSTRAP step-0004-20261009T183603+0000, WRITE serial iter-refine-writing-20261009T190400+0000. Objective: read-only review of section-specific full-paper conventions. Entry paper SHA-256: b8063e3afc591cad70fc6a210f116d68b541316a675081c0af24ffaefa1c4743. No Git operation was used; root owns revision and baseline records.

## Sources and method

Read docs/user-instruction.md; complete iter-refine-writing/SKILL.md; complete check-paper-structure-flow/SKILL.md; its references/full-paper-12p.md; rewrite-abstract-intro/references/abstract-intro-structure.md; and the entire current docs/paper/main.tex. The first attempted abstract-reference path under check-paper-structure-flow did not exist; the full-paper reference points to rewrite-abstract-intro, which was subsequently read. No Skill tool is available, so these are actual filesystem reads rather than a claimed Skill invocation. The initial full-paper output was supplemented with targeted reads covering the otherwise truncated Design segment. Whitespace-token count of the abstract is 230, including its result placeholder. The unavailable `python` executable was replaced with `python3` for this count.

Reviewed sentence/paragraph roles against the full-paper template; followed all four RQs from overview to evidence closure; checked background/motivation separation, design goals and implementation boundary, related-work grouping, and conclusion. Accepted intended completed-system prose and explicit missing-result placeholders in BOOTSTRAP. No external search or empirical judgment was needed for this writing-only round.

## Raw findings

### Must-fix

None. No missing section role, missing RQ evidence block, orphan experiment, or conclusion structural defect was found.

### Should-fix

1. MICRO — Background, Verification stages and outcomes, main.tex:52. The first two sentences neutrally explain admissions and verification outcomes, but the final sentence, “Counting accepted commands alone does not determine fidelity between verification paths,” turns into an argument about an inadequate comparison. Concrete fix: retain the technical content and replace the final sentence with a neutral connection to the later interface definition, such as “These outcomes form part of the Lean interface comparison in Section~\\ref{sec:behavior}.” The preceding sentence already preserves the reason accepted commands alone are insufficient; alternatively relocate the exact argument to Motivation if root judges it independently necessary. Keep the `sorry` admission concept and existing citation.

2. MICRO — Background, Prepared native state, main.tex:57. The subsection ends on runtime details without the template's explicit connection to the later design that needs them. Concrete fix: append a short neutral sentence, “Section~\\ref{sec:design} uses these native-state and process properties to define preparation boundaries.” Preserve timers, descriptors, runtime threads, copy-on-write, and resource-counter distinctions. This is a local explanatory bridge, not a new scientific claim.

### Consider

1. MICRO — Introduction, This paper paragraph, main.tex:31. Its mechanisms, method and missing findings occupy approximately eight sentences, above the typical full-paper 3–5-sentence paragraph range. The role itself is complete: runtime boundary, resources and bounded lifetime each answer the challenges paragraph. Consider tightening adjacent system-description sentences while preserving branch-owned communication, inherited resource state, native fallback, matched strong baselines, RTX 5090 and full device costs. This is optional; retaining explicit scientific scope outweighs the approximate sentence guideline. Do not split or remove an RQ or result placeholder merely to shorten it.

## Positive convention checks

| Area | Finding |
|---|---|
| Abstract | One paragraph, 230 whitespace words, within 200–300. Nine sentence-role units including the explicit result placeholder: background, problem, cause, reuse alternatives, insight, challenges, system, method, results. Each maps to the corresponding intro role; the placeholder is accepted rather than treated as invented evidence. |
| Introduction | Eight role paragraphs: background, problem with a concurrent-cancellation example, native-history cause, established reuse and unresolved comparison, separable insight, three challenges, system/method/results, four concrete contribution items. Required roles remain distinct. No demand to invent prior-work weaknesses where the contract states an unresolved comparison. |
| Background / Motivation | Separate sections; technical stages/native state are load-bearing. Motivation contains explicit characterization placeholders and the scope/history argument, then ends in a Design bridge. Apart from the local background sentence above, the distinction is sound. |
| Design | Opens with three explicitly numbered goals and overview, includes an architecture figure and operation walkthrough, then five design-decision subsections. Goals map to RQ2/RQ3 and RQ4's frontier assessment. No concrete adapter API leaked into Design. |
| Implementation | Separate section mapping native adapters, process/resource handling and device path onto the design, with language/platform/integration closing paragraph. |
| Evaluation | Complete unchanged four-question overview; Setup and Limitations outside RQ count. Each of four descriptive noun-phrase evidence blocks opens explicitly with its RQ and closes with “RQn remains unanswered” plus required evidence. All stream controls, behavior checks, frontier ablations and CPU/device measurements are subordinate to these RQs. |
| Baselines and boundaries | Competent bounded warm services and native logical/serialized reuse remain explicit. Lean and SMT source paths are retained; post-export checker results are narrower. RTX 5090 and setup/representation/transfer/synchronization/fallback costs remain explicit. |
| Related work | Four topic groups with comparative narrative: persistent state, verification caching, prepared execution, heterogeneous checking. No per-paper list structure. |
| Conclusion | One paragraph restating separation thesis, behavioral/resource criterion, and placeholder for all four RQ findings. No new mechanism or future-work proposal. |

## Decisions, verification and handoff

This subagent applied no paper fixes and rejected none. Root must record acceptance/rejection and before/after locations for both Should-fix items and the Consider item, then compile and check page/error evidence before Round 3. No compilation or page evidence is claimed in this read-only report. Quantitative values and all RQ wording/meaning were read-only; no changes were made to either. No citations, technical content, result values, baselines or scope qualifiers were removed. Only this report was written; no memory or Git state was changed. Remaining evidence placeholders are intentional BOOTSTRAP scientific work, not Round 2 writing failures. Next node: root applies/logs review decisions and compilation, then serial Round 3 logic-flow review.

Root disposition 2026-10-09T19:10:40.457657+00:00: applied both Should-fix locally. Background admissions paragraph now neutrally connects to interface comparison; the exact accepted-count insufficiency sentence is relocated intact to Design/Observable behavior, so no protected technical assertion disappears. Added the native-state subsection’s neutral Design bridge. Consider intro tightening deferred to mandatory Round4 rebuild, which owns that exact paragraph procedure; no scope compressed here. Fresh compile exit0/8pages (round2-build.log); reviewed diff preserves39citation commands, all numbers, exact4RQ/12resultslots. No scientific-contract change. Round complete,nextRound3.
