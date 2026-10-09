# Round 0: macro structure review

Parent node: BOOTSTRAP step 0005, writing run 20261009T213300+0000. Reviewer: scoped read-only child, macro Level 1 only. Objective: independently compare the sole current paper with the full systems-paper structure without changing its scientific contract.

Started: 2026-10-09 21:34:06 UTC (first recorded clock observation, after initial instruction/source reads). Completed: 2026-10-09 21:34:39 UTC (review completed; report serialization follows). An earlier exact start was not instrumented and is not invented.

Entry baseline supplied by the parent: `5553bfc67409dd57cdc202ff53d61bf59bce4d40`. Input is the cumulative working paper including the parent's W1 LeanPolish/native-finalization additions. SHA-256 of reviewed `docs/paper/main.tex`: `758636ccc21195cbd2567123c13ed91abf56bc869bcd2bbfb9a12533cd0764fa`; of `docs/paper/references.bib`: `f55c6af75bd07eb090c76c243a82a703719be50e682edeea64f1be77fbd9ceb2`. No Git commands, stash operation, source checkout, native rerun, or paper edits were performed.

## Instructions and inputs read

Read `docs/user-instruction.md` first. Read the complete filesystem instructions in `/workspaces/.agent-state/codex/skills/check-paper-structure-flow/SKILL.md` and `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`. Read the applicable full-paper template `check-paper-structure-flow/references/full-paper-12p.md` and its referenced `rewrite-abstract-intro/references/abstract-intro-structure.md`. No Skill tool exists; these were actual filesystem reads. Read all of `docs/paper/main.tex`, recovering the middle span separately after combined-output truncation. Read the Makefile, citation annotation/key excerpts including the two W1 LeanPolish sources, and inspected existing `main.pdf` metadata/text. External source verification is outside this macro review.

Method: full main-text outline and section-role comparison; overview/architecture and design/implementation boundary inspection; explicit RQ count, mapping, and evidence-block inspection; approximate source-length and existing-PDF page checks. Full-paper/OSDI shape governs even though the current PDF has eight pages. BOOTSTRAP present-tense implementation prose is intentional; honest result placeholders and unanswered RQ endings are accepted. The four established RQ strings are read-only.

## Structural checks

| Check | Finding |
|---|---|
| Required sections and order | Pass: Introduction, Background, Motivation, Design, Implementation, Evaluation, Discussion, Related work, Conclusion occur in the full-paper order. |
| Background versus Motivation | Pass at macro level: separate sections. Background explains verification stages, admissions, native prefixes, runtime/resource properties; Motivation develops preparation/lifetime and scope/history costs. W1 finalization paragraph explains the existing verification boundary and has a load-bearing later use. |
| Introduction and abstract roles | Macro pass: context, problem, cause, established approaches, insight, challenges, system/method/results placeholder, and four concrete contributions occur in order. Detailed sentence counts and paragraph mechanics belong to later rounds. |
| Design opening | Pass: three explicitly numbered goals derive from Motivation; immutable preparation, independent branches and fallback form the overview. |
| Architecture and operation walkthrough | Pass: Figure 1 is present at the beginning of Design, with a prose candidate walkthrough. Visibility of ownership/cancellation could improve, as S1 below records. |
| Design versus Implementation | Pass: five design-decision subsections describe boundaries, behavior, lifetime, placement and heterogeneous semantics; three implementation subsections map them onto native adapters, Linux branching/resource handling and the device path. Concrete C++, Z3 native parser/context and NVIDIA details are in Implementation. |
| RQ count and organization | Pass: exactly four numbered RQs precede setup/results. Four primary blocks have descriptive noun-phrase titles, open with their associated RQ, and close with explicit unanswered conditions plus result placeholders. Setup and Limitations remain outside the RQ count. No orphan experiment block. |
| RQ mapping | Pass: RQ1 maps to opportunity characterization; RQ2 to behavior/isolation goals; RQ3 to equal-resource frontier; RQ4 to remaining heterogeneous benefit after reuse. No scientific rewording is requested. |
| Subsection balance | Pass: Background 2, Motivation 2, Design 5, Implementation 3, and Evaluation setup + 4 RQ blocks + Limitations. Primary RQ blocks have comparable lengths. |
| Related work | Pass: four topic groups. W1 LeanPolish paragraph belongs to persistent verification state, strengthening the established-reuse comparison without inventing a separate group. |
| Discussion and Conclusion | Pass: Discussion covers broader mechanism implications and extension; Conclusion restates the thesis and reserves an honest result slot. |
| Page budget | Current built PDF: eight pages, created 2026-10-09 21:33:33 UTC. Source token estimates: Introduction 672, Background 387, Motivation 287, Design 1049, Implementation 560, Evaluation 1168, Discussion 70, Related work 322, Conclusion 64. These are regex word-like counts including LaTeX, not exact prose counts. Design/Implementation dominate appropriately; result placeholders make the final empirical page budget indeterminate. No artificial prose expansion is requested. |

## Must-fix

None identified within this macro-writing scope. No missing section, missing architecture, merged design/implementation, or missing/misorganized RQ set was found.

## Should-fix

**S1 — MACRO, Design overview/Figure 1 (main.tex lines 76–104).** The architecture shows the forward execution path, but does not visually expose the ownership and cancellation boundary central to contribution 2 and RQ2. The caption identifies the parent, while the graphic only labels an “Immutable native prefix”; candidate mutation and lifetime ownership remain in surrounding prose. Concrete fix: relabel that box “Prepared parent: immutable native prefix”; label the child group “Independent branches: candidate mutation and lifetime”; add a simple cancellation arrow into an individual branch, with termination/reaping indicated. Keep the existing native-fallback path and CPU/device path. This is an illustration of already stated semantics, not a new mechanism or guarantee. Root should individually assess whether the extra labels remain legible in one column.

## Consider

**C1 — MACRO, final empirical page allocation.** The existing eight-page draft has compressed Discussion/Related work and no numerical result figures yet. Preserve the current outline, and reassess the 12–14-page template allocation after inserting actual RQ evidence; expand only load-bearing comparisons or implications that the completed evidence requires. This is a later layout check, not a BOOTSTRAP defect or demand for invented results.

## Preservation, disposition, and validation boundary

No proposed edit changes the four RQ strings, quantitative values, citations, supported-boundary scope, resource-limit qualifications, complete-verification versus tactic-screen boundary, or CPU/device measurement boundary. Intended system prose remains present tense. The two source-grounded W1 additions fit their current sections.

Applied/rejected fixes: none by this reviewer; the root owns all paper changes and will append individual S1/C1 dispositions, before/after locations, round diff, compilation evidence and remaining concerns. Existing PDF metadata was inspected; no compilation was run by this read-only reviewer. One inspection command initially used unavailable `python`; it was corrected to `python3` without changing files.

Tree/memory changes: only this authorized round report; no paper, canon or Git mutation. Next node: root dispositions and verification, followed serially by Round 1 paragraph-role/micro-flow review.

## Root disposition and completed verification

2026-10-09T21:40:34.736728+00:00: S1 accepted: existing architecture becomes native TikZ with prepared parent ownership, branch-private mutation/lifetime, selected cancellation control and explicit private-state release. Unsupported native execution has its own responses rather than falsely flowing through branch teardown. Parent no-verification qualifier remains after selected boundary. Actual paper-figures/design-diagrams fullinstructions read; diagram stays at Design abstraction, no Linux API/security guarantee or measured number added. C1 deferred until final result slots are filled, no invented layout expansion. All prior factual paragraphs/citations/numbers/RQ meanings retained. Native fallback, CPU/device and bounded placement remain.

Initial round-0-build.log fails missing tikz.sty; old PDF is recognized as stale, not validated. Actual texlive-pictures restoration exits0 (installlog retained); first normal remake retains latexmk previous-error state, also preserved. Forced latexmk -g exits0; label wrapping repaired locally and round-0-build-complete.log exits0/8pages, final main.log has no undefined/overfull warning. Figure page3 rendered/viewed; clear ownership/cancellation and fallback path fit one column. gitdiff inspected: only existingfigure/requiredTikZpackage changes after W1, no technical deletion; 44citecommands/23annotatedkeys,12resultslots/fourRQ unchanged. Root alone edits paper, no stash or Git mutation. Next serialRound1.
