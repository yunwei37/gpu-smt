# Round1: micro structure

Started after Round0 completion; completed 2026-10-07T22:12:48.107637+00:00. Parent WRITE_GATE step0001; exact entry tree recorded in Round0. Fresh reviewer writing_round1 read complete current paper/bib, main writing skill, structure-flow/full-paper and abstract-intro-structure references through disclosed filesystem adaptation. Applied Levels2–3 roles/internal-flow checks; no edits/Git/build by reviewer.

Must-fix: Abstract methodology names RTX5090 and setup/transfer/fallback while corresponding Intro system paragraph lacks them. Applied existing methodology to Intro paragraph; result placeholder unchanged. Should-fix: heterogeneous Design mixes selection/static-graph dependencies, adapter paragraph mixes mechanics/baselines, process paragraph mixes memory/affinity, device paragraph mixes semantic/cost boundaries. Applied splits and exact moves: two native-baseline/export sentences now Experimental setup; affinity sentence now setup methodology. Consider: Intro example consequence could be clearer—defer to required Round4 full opening rebuild; motivation lifetime split deferred until actual characterization expands short paragraph; Discussion workload/deployment/GPU distinct scopes split without removing any limitation.

Root inspected subsection edits and cumulative git diff; original text moved, not deleted. Current RQ strings match entry tree exactly; citations27 unchanged; only pre-existing RTX5090 value repeated in Intro, no value altered. make exits0, pdfinfo seven pages. No result values invented; all final RQs unanswered. Next Round2 conventions.

Reviewer session started 2026-10-07T22:11:30.728Z; final return 2026-10-07T22:12:03.176Z. Source-native journal rollout-2026-10-07T22-11-30-01a1186b-f525-75b0-91c2-3cf04e925074.jsonl.

## Verbatim independent reviewer return

Read the complete paper and bibliography, plus all requested skill/helper sources. No Skill tool is available; I followed the actual filesystem sources as the adaptation. No edits, Git operations, or builds performed.

**Must-fix**

- **MICRO — Abstract ↔ Introduction, lines 19 and 36:** The abstract methodology sentence introduces RTX 5090, heterogeneous checking, and inclusion of setup, transfer, and fallback costs. The corresponding introduction system/evaluation paragraph names neither the device nor these cost boundaries; its placeholder mentions only “device benefit.” This violates the required correspondence. **Fix:** Add a methodology sentence to introduction ¶6 naming the existing RTX 5090 comparison and complete cost accounting, using the scope already established in Evaluation. Preserve the result placeholder.

**Should-fix**

- **FLOW — Design / Heterogeneous checking, line 121:** One paragraph mixes selection of costly operations with the separate reason static expression graphs do not expose available parallel work. That interrupts the progression from opportunity to mechanism. **Fix:** Keep the first two sentences as the residual-cost/selection paragraph; begin a separate paragraph with the expression-graph dependency issue and retain its dynamic-work conclusion.
- **MICRO — Implementation / Native adapters, line 131:** The paragraph begins with Lean adapter mechanics but ends with baseline selection and evaluation-boundary qualification. These are separate roles. **Fix:** Retain the first two sentences as adapter mechanics; move the baseline and post-export measurement sentences to Experimental setup, preserving their content and references.
- **FLOW — Implementation / Process and resource handling, line 136:** Retention bounds, memory accounting, and CPU-affinity methodology occupy one paragraph. The affinity sentence introduces a distinct measurement concern. **Fix:** Keep retention and memory accounting together; move the affinity statement intact to the hardware/methodology setup paragraph.
- **MICRO — Design / Heterogeneous checking, line 123:** The paragraph combines semantic preservation with end-to-end measurement accounting. **Fix:** Separate the matched-output/native-checking and CPU-fallback guarantee from the initialization/transfer/queueing accounting. Preserve the distinction between resident primitive speedup and complete checking.

**Consider**

- **MICRO — Introduction ¶2, line 26:** The concrete example states two simultaneous needs but leaves their practical consequence implicit. **Fix:** Tie it directly to the already named resource growth or cancellation issue in the example sentence; do not add an unmeasured performance claim.
- **FLOW — Motivation / Preparation and candidate lifetime, line 61:** Preparation opportunity and failed-attempt lifetime cost are two linked ideas sharing a short paragraph. **Fix:** Consider a separate paragraph beginning with failed/incomplete attempts if the final characterization expands this subsection.
- **FLOW — Discussion and limitations, line 180:** Workload external validity, backend deployment scope, and GPU workload distinctions share one paragraph. **Fix:** Separate replay/corpus validity, supported-runtime deployment scope, and GPU boundary interpretation into short paragraphs while retaining every limitation.

The introduction otherwise has the required distinct background, problem, root-cause, existing-solutions, insight, challenges, system, and contribution roles. Its three challenges are answered by the system paragraph. Subsection titles are descriptive noun phrases. All four RQ evidence blocks explicitly open with their RQ and close with an honest unanswered statement plus evidence TODO. Present-tense intended-system descriptions and missing empirical results are appropriate for this BOOTSTRAP review; honest scope statements should remain.
