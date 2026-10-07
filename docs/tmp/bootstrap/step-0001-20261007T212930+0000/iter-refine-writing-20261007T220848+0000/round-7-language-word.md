# Round7: language-word

Started 2026-10-07T22:19:59.842Z; reviewer returned 2026-10-07T22:21:04.366Z; root completed 2026-10-07T22:21:54.282802+00:00. Parent step0001 WRITE_GATE. Source diff baseline 7152e64a4e9dcad30933dcb85c9981c2e24929a2; original entry tree remains0cf6486e5a40cc0d7740462ddfb69d2e945144a5. Fresh read-only reviewer gpt-6.1-sol loaded full paper/bib and requested full skill sources through filesystem adaptation (no Skill tool). No reviewer edits/Git/build. Evidence/source journal rollout-2026-10-07T22-19-59-01a11873-b9df-7fc2-84d7-ac9054a6a57c.jsonl.

## Root dispositions and verification

Applied all10 Should-fix and5 Consider locally. Clarified observable-behavior argument, evaluator action, universal equality scope, integration/action, fresh-driver distinction, complete frontier mapping, generated-traffic limitation, competing-work observation, all-attempt locality and scope/history controls. Simplified comparison, removed redundant actually/actual adverbs while retaining measured costs/context availability, expanded integer IDs, and expressed terminal completeness as recorded outcomes.14 source lines modified;15 findings addressed because one line covers two fixes. Compound audit93 tokens58 forms is diagnostic, not paper evidence. Same reviewer completed an explicit late user-file wrapper check, finding no scope conflict; both returns retained below. No Must-fix/content/citation loss.

Root reviewed subsection-sized apply_patch edits and source diff. make -C docs/paper exits0. Pages:           7; citation commands 27, never decreased; four RQs match entry tree verbatim; no quantitative value invented or changed. Scope conditions and negative/mixed-result permission protected. Paper SHA256 a6d03339856c0f7368bd14f76ec7816035c04a3b6e74f98796445aca274d50ee. Intended incomplete submission, not final venue compliance or answered RQs. Next serial round after this full compile/check.

## Verbatim independent reviewer return

Read the complete `main.tex`, `references.bib`, and both requested skills. No edits, Git operations, or builds performed.

Compound audit: a case-sensitive source scan finds **93 hyphenated tokens across 58 distinct forms**, including one LaTeX label and text inside result placeholders. Frequent forms include `prepared-state` (7), `SMT-backed` (6), and `proof-state`, `equal-resource`, `end-to-end`, and `copy-on-write` (4 each). Most are useful technical compounds. The avoidable density comes from one-off forms such as `response-equality`, `complete-verification`, `generated-traffic`, and `competing-work`.

**Must-fix**

None. No unambiguous dangling pronoun, stacked hedge, or verbose stock phrase requires correction. Four exact RQs, quantitative values, citations, and scientific scope should remain unchanged.

**Should-fix**

1. **Abstract, L14 — compressed compound.**  
   “need separate observable-behavior arguments” makes the object of the argument unnecessarily abstract.  
   Fix: “need separate arguments about observable verification behavior.”

2. **Introduction, L36 — nominalization.**  
   “motivating assessment of heterogeneous checking” hides the evaluative action.  
   Fix the sentence locally: “Preparation reuse changes the remaining cost distribution, motivating us to assess heterogeneous checking on an RTX 5090 with setup, transfer and CPU fallback included in complete verification costs.”

3. **Design / Observable behavior, L106 — invented compound.**  
   “a universal response-equality assertion” adds terminology without precision.  
   Fix: “a universal assertion that responses remain equal.”  
   Retain the wall-time and changed-runtime qualifications.

4. **Implementation opening, L130 — inflated wording.**  
   “Integrations comprise” is stiff and nominal.  
   Fix: “The implementation integrates native SMT session evaluation, Lean context reuse and matched CPU/device execution on Linux.”

5. **Implementation / Native adapters, L133 — compound nominalization.**  
   “Fresh-driver comparison separates interface incompatibility from branch-induced differences.”  
   Fix: “Comparing fresh driver execution separates interface incompatibility from differences caused by branching.”

6. **Evaluation opening, L146 — compound accumulation.**  
   “that complete-verification frontier” adds a second compound to the already compressed “equal-resource service frontier.”  
   Fix only the last sentence: “RQ4 tests whether heterogeneous execution improves that frontier for complete verification after reuse.”

7. **Evaluation / Experimental setup, L155 — opaque compound.**  
   “They do not supply generated-traffic locality.” The antecedent is clear, but “supply locality” obscures the intended distinction between controls and traffic evidence.  
   Fix: “These controls do not establish locality in generated candidate traffic.”

8. **Evaluation / Experimental setup, L159 — opaque compound.**  
   “competing-work observations” makes an ordinary measurement sound like a named technique.  
   Fix: “observations of competing work.”  
   Full local wording: “Affinity specifies permitted CPUs and is recorded with topology and observations of competing work.”

9. **Evaluation / Preparation sharing, L162 — awkward compound and metaphor.**  
   “a successful-proof subset cannot manufacture locality” uses an adversarial metaphor in methodology prose.  
   Fix: “The characterization includes failed and incomplete attempts, so locality is measured across all attempts rather than only successful proofs.”  
   This preserves the substantive exclusion of selection-induced locality.

10. **Evaluation / Behavior and isolation, L167 — inflated verb and compounds.**  
    “Native scope/history controls discriminate solver-mode changes from cross-candidate interference.”  
    Fix: “Native scope and history controls distinguish changes in solver mode from cross-candidate interference.”

**Consider**

1. **Abstract, L15 — indirect nominalization.**  
   “requiring a matched equal-resource comparison after their existing savings” is difficult to parse.  
   Suggested local ending: “requiring a matched comparison at equal resources that accounts for their existing savings.”

2. **Design / Preparation boundaries, L99 — unnecessary adverb.**  
   “every assigned candidate actually has available” → “every assigned candidate has available.”  
   “Actually” contributes little because availability is already an explicit requirement.

3. **Implementation / Device path, L143 — compressed compound.**  
   “Integer-ID expression layouts” → “expression layouts with integer identifiers.”  
   Preserve the citation and explicit acknowledgment that these are existing techniques.

4. **Evaluation / Preparation sharing, L162 — unnecessary adverb.**  
   “measure the actual preparation CPU time” → “measure preparation CPU time.”  
   The contrast with text bytes and declaration counts remains explicit in the next paragraph.

5. **Evaluation / Behavior and isolation, L169 — procedural jargon.**  
   “every planned behavior comparison reaches terminal status” → “every planned behavior comparison finishes with a recorded outcome.”  
   Retain “RQ2 remains unanswered” and the requirement that residual differences be explained.

Summary: **0 Must-fix, 10 Should-fix, 5 Consider**. The most useful changes clarify generated-traffic locality, remove the “response-equality” compound, and replace the selection/locality metaphor with explicit methodology. Honest negatives, limitation statements, BOOTSTRAP present tense, and missing-result markers are protected.

Read the actual authoritative files `docs/user-instruction.md` and `docs/questions-for-author.md` in full.

**Must-fix:** None. The Round7 findings preserve the user’s Lean and SMT performance research, investigation of GPU Lean verification, RTX 5090 as the only authorized GPU family, `gpt-6.1-sol` execution preference, and the complete OSDI-level research process with experiments and RQs. No finding proposes another GPU, model, scheduler, scientific scope, or RQ change.

**Should-fix:** None added by this authority check.

**Consider:** None added. The earlier 15 word-choice findings remain valid. Honest negative results, limitations, CPU comparisons and fallback costs support the requested research rigor and should remain explicit. No conflict between the direct-user instructions and prior review inputs or findings was identified.
