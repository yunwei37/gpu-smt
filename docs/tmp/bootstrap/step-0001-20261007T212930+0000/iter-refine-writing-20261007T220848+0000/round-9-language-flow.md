# Round9: language-flow

Started 2026-10-07T22:24:42.556Z; reviewer returned 2026-10-07T22:25:09.330Z; root completed 2026-10-07T22:25:35.305016+00:00. Parent step0001 WRITE_GATE. Source diff baseline 21e90993225e3d3e39b0faec55f0b1d67466167e; original entry tree remains0cf6486e5a40cc0d7740462ddfb69d2e945144a5. Fresh read-only reviewer gpt-6.1-sol loaded full paper/bib and requested full skill sources through filesystem adaptation (no Skill tool). No reviewer edits/Git/build. Evidence/source journal rollout-2026-10-07T22-24-42-01a11878-0a39-7990-925d-8017b40beddf.jsonl.

## Root dispositions and verification

Applied both Should-fix: balanced abstract Lean/SMT comparison and explicit dependency paragraph link to selected checking operations. Applied Consider affinity thread with isolation qualifier and topology/competing work intact.3 local source sentence constructions changed; no scope change or content deletion. Allothertopic/register checks pass, direct-user file wrapper loaded.

Root reviewed subsection-sized apply_patch edits and source diff. make -C docs/paper exits0. Pages:           7; citation commands 27, never decreased; four RQs match entry tree verbatim; no quantitative value invented or changed. Scope conditions and negative/mixed-result permission protected. Paper SHA256 8a153211eb5db912a06d088da2552ef85bfdcf544ef7309074c6d4c64d7f3065. Intended incomplete submission, not final venue compliance or answered RQs. Next serial round after this full compile/check.

## Verbatim independent reviewer return

Read-only Round 9 completed. Reviewed the full paper, bibliography, author instructions and both writing skills using filesystem access. No edits, Git operations or builds performed.

**Must-fix:** None.

**Should-fix**

1. **Abstract, L19 — unbalanced coordination obscures the comparison.**  
   Quote: “We compare complete Lean and verification backed by satisfiability modulo theories (SMT) solvers…”  
   Problem: “Lean” and “verification” occupy parallel positions but name different kinds of objects. The reader must reconstruct the intended shared noun before following the evaluation clause.  
   Concrete fix: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against established bounded warm and branching services, and assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.”

2. **Design / Heterogeneous checking, L123 — weak transition from operation selection to dependency analysis.**  
   Quote: “The input expression graph does not alone define checking dependencies, because reduction depends on binder environments and instantiated constants.”  
   Problem: The preceding paragraph introduces supported operations selected from profiles; the next paragraph abruptly introduces an expression graph without connecting it to those operations.  
   Concrete fix: “For these checking operations, the input expression graph does not alone define dependencies, because reduction depends on binder environments and instantiated constants.” Preserve the following sentence about actual dynamic work, representations and synchronization.

**Consider**

3. **Evaluation / Experimental setup, L159 — the affinity qualification reads as two detached notes.**  
   Quote: “Affinity specifies permitted CPUs and is recorded with topology and observations of competing work. Affinity alone is not CPU isolation.”  
   Problem: The final short sentence breaks the thread between recorded machine conditions and the limitation of affinity.  
   Concrete fix: “Affinity specifies permitted CPUs but alone does not provide CPU isolation, so we record it with topology and observations of competing work.” This preserves the explicit negative and all recorded conditions.

Total: **0 Must-fix, 2 Should-fix, 1 Consider**. The most useful changes are clarifying the abstract’s comparison, connecting operation selection to dependency analysis, and integrating the affinity qualification. The remaining sections have acceptable topic progression and register; the four RQs, placeholders, honest unanswered statements, scientific scope and limitations require no flow-driven changes.
