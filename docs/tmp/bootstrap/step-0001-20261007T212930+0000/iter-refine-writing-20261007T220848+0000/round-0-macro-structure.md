# Round 0: macro structure

Started 2026-10-07T22:08:48Z; completed 2026-10-07T22:11:15.022767+00:00. Parent step0001 WRITE_GATE. Entry HEAD f51434962c8f6934b2cde448dc04b399d1c131e5; paper entry tree 0cf6486e5a40cc0d7740462ddfb69d2e945144a5. Root staged only paper source/build files and used git write-tree, overriding the helper stash suggestion because user forbids stash and paper was untracked. No stash/ref/branch/source-copy operation. Round11 uses this exact tree baseline.

Fresh read-only reviewer writing_round0 loaded complete paper/bib, iter-refine-writing, check-paper-structure-flow and full-paper-12p through filesystem because no Skill tool exists. Intended full conference template applies; six-page seed is not workshop or venue-compliance evidence. Four established RQ meanings/values/scope protected.

## Findings and dispositions

No Must-fix. Should-fix 1: diagram omits native fallback/device path; add already-described decision/path and walkthrough. Applied to Design figure and following paragraph. Should-fix 2: implicit contribution/goal/RQ mapping; name existing goals and add mapping. Applied mapping at Evaluation opening, using existing ordinal goals instead of introducing additional labels/numbers. Should-fix 3: comparison procedure in Design and sparse Implementation. Moved exact startup/deeper-prefix/warm-worker comparison to RQ3. Retained behavioral/cost requirements; implementation expansion rejected because no additional established implementation facts support it. This is deferred scientific detail, not fabricated writing. Should-fix 4: undifferentiated related-work groups. Applied four parallel paragraph headings.

Consider 5: Motivation/Evaluation placeholders overlap. Rejected changing evidence placeholders in this macro pass: concise motivation and complete RQ blocks already have different rhetorical roles; no evidence removal warranted. Consider 6: implementation/related-work final conference balance. Deferred until implementation/results exist; page expansion without content would be padding. All mandatory sections/order, separate background/motivation, five design decisions, architecture, setup+four unanswered RQ blocks pass.

Edits applied subsection by subsection with apply_patch; two initial patch attempts failed atomically and changed nothing. Outline: retain section order, expand existing figure/walkthrough, move comparison into RQ3, mark four related-work groups. git diff against entry tree inspected: moved comparison retained verbatim, no scientific content removed; citations remain 27, RQs verbatim, no quantitative value changed. make -C docs/paper exits0; pdfinfo reports seven pages, unfinished figure/result budget remains. Honest limits override helper anti-limitations instructions. Next Round1 micro review.

Reviewer session started 2026-10-07T22:08:56.282Z; final return 2026-10-07T22:09:31.962Z. Source-native journal rollout-2026-10-07T22-08-56-01a11869-99d7-74e3-b4b2-18ea2ad8bfcf.jsonl.

## Verbatim independent reviewer return

Filesystem adaptation: read the full writing skill, macro-check skill, full-paper reference, `main.tex`, and `references.bib` directly because no Skill tool exists. No edits, Git operations, or builds performed.

1. **Should-fix — Architecture overview, lines 71–89.** Figure 1 provides an architecture diagram, but depicts only the preparation/branch path; readers cannot locate the native fallback or heterogeneous path discussed later. Extend the diagram with the already-described supported-boundary decision, native fallback, and CPU/device execution paths. Add a short walkthrough identifying parent-owned preparation and branch-owned candidate state.

2. **Should-fix — Goals/contributions/RQs, lines 38–43, 71, 135.** Evaluation says every RQ maps to a goal and contribution, but leaves those mappings implicit. Name the existing goals G1–G3 and add a compact mapping sentence or table: RQ1 tests sharing opportunity; RQ2 tests behavior and isolation; RQ3 tests the equal-resource frontier; RQ4 assesses the remaining heterogeneous opportunity. Preserve all four RQs verbatim and describe RQ4 as subordinate to complete-verification performance.

3. **Should-fix — Design/Implementation/Evaluation separation, lines 106, 111, 114–116, 119–132.** Top-level separation is correct, but several Design passages describe comparisons and measurement accounting rather than design decisions, while Implementation contains relatively little mechanism detail. Keep the behavioral requirements and complete-cost boundary in Design; move comparison/ablation procedure to the corresponding RQ blocks. Expand Implementation only from established implementation facts; mark missing adapter/resource/device details explicitly rather than inventing them.

4. **Should-fix — Related work navigation, lines 175–182.** Four topic groups already exist, but appear as an undifferentiated paragraph sequence. Add parallel noun-phrase headings for persistent verification state, verification caching, prepared execution, and heterogeneous checking. Preserve the substantive comparisons and qualifications.

5. **Consider — Motivation versus Evaluation, lines 61–66, 151–158.** Motivation and RQ1/RQ2 reserve overlapping evidence. Make Motivation’s placeholders request concise representative observations and point to the complete characterization in Evaluation. This avoids duplicating final result presentations without requesting additional experiments.

6. **Consider — Full-paper balance.** Design has five balanced decision subsections; Background has two; Evaluation has setup plus four balanced RQ blocks. Implementation and Related Work are currently compressed relative to the full-conference reference. As existing technical detail and results become available, allocate roughly 2–3 pages to Design, 1 to Implementation, 3–4 to Evaluation, and 1–1.5 to Related Work. Actual page balance cannot be verified without a build.

**Checklist conclusion:** All required sections are present in the expected order; Background and Motivation are separate; Design opens with three goals and an overview; an architecture diagram exists; Design and Implementation are separate; Evaluation explicitly lists four unchanged RQs and provides one evidence block per RQ, each ending with an honest unanswered placeholder. No macro **Must-fix** found for this bootstrap stage. Preserve “Discussion and limitations,” negative results, and scope qualifications: the user’s disclosure requirement overrides the helper’s prohibition on limitations.
