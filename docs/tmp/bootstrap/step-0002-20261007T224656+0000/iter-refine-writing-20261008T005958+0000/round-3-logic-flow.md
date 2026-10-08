# Round 3 — Logic flow

Started: 2026-10-08 01:05:57 UTC. Review completed: 2026-10-08 01:06:15 UTC. Report written after review.
Parent: BOOTSTRAP step-0002-20261007T224656+0000; iter-refine-writing-20261008T005958+0000. Objective: fresh complete-paper writing review of argument continuity and mechanism/challenge/contribution/evaluation consistency. Entry HEAD: d224cd2d991439940e5b4b108b55b53c6a1b8525; existing dirty sources retained.

Files read: docs/user-instruction.md; docs/questions-for-author.md; complete iter-refine-writing/SKILL.md; complete docs/paper/main.tex including architecture diagram/caption, evaluation, related work and conclusion; complete docs/paper/references.bib. The combined read truncated implementation/evaluation; subsequent numbered reads recovered those passages. Method: trace preparation/lifetime motivation through native history and existing reuse, boundary fidelity and independent branches, bounded placement, then all four evaluation questions and conclusion. BOOTSTRAP completed-system prose and explicit missing-result placeholders are accepted. No external scientific critique or research reframing was performed.

## Must-fix

None. The argument is continuous: preparation sharing addresses repeated preparation, interface qualification addresses native history, disposable children address lifetime/isolation, and equal-resource comparisons address bounded service value. Each RQ has a matching evidence block and explicit unanswered placeholder; conclusion returns to the same preparation/history and fidelity/resource tradeoff.

## Should-fix

1. **Preparation boundaries and figure caption — main.tex lines 92, 99; background and implementation line 131.** The caption says the parent performs no candidate verification, while background/design allow accepted commands and proof context in preparation. Line 99 correctly excludes suffix work after the selected boundary, but a reader can infer all earlier elaboration is excluded. **Concrete fix:** qualify the caption as no verification of candidate suffixes after the selected boundary. If needed, connect accepted context explicitly to preparation before that boundary. Preserve the exclusion of speculative suffix state and the rule against cancelled/incomplete attempts becoming parents. Preferred alternative: edit only the caption because line 99 is already precise.

2. **Heterogeneous checking to device implementation — lines 121–123, 139, 175.** Design describes native checking of the resulting proof/artifact, whereas implementation describes per-operation output identity. An internal reduction operation need not itself emit a proof/model artifact; the two validation layers are not connected. **Concrete fix:** connect CPU reference comparison of operation outputs to the enclosing verifier's applicable native proof/artifact checks. Do not imply every operation emits a certificate. If this does not match the existing validation contract, root must resolve the scientific detail rather than the reviewer inventing a correctness mechanism. A cross-reference alone would leave this distinction implicit.

## Consider

3. **Heterogeneous transition — line 121.** “Preparation reuse leaves a smaller verification path” reads as unconditional before opportunity/frontier evidence, despite the existing cheap-preparation/low-locality cases. **Concrete fix:** “When preparation reuse removes repeated work, it leaves a smaller verification path for an accelerator to improve.” This preserves RQ4 and negative-opportunity scope without claiming measured benefit.

4. **Placement connection — lines 116, 136, 171.** Design favors states whose reuse pays for retention, implementation describes bounding/accounting, and the placement ablation lacks an immediate pointer to that rule. **Concrete fix:** cross-reference the reuse-based placement rule in the implementation or placement ablation. Do not invent a threshold, score, admission algorithm or contribution.

## Preservation and disposition

All four RQ strings/meanings, citations, quantitative values, protected scope/resource qualifiers, native fallback, strongest matched service requirement and RTX 5090 scope remain unchanged. No fabricated results or missing-data objections. Retain the wall-time qualification; unconditional behavioral equivalence would contradict it. Scientific clarification for root: the device operation/output validation relationship in finding 2, if not already determined by the existing contract.

Raw findings are those listed above. Applied fixes: none, reviewer-only assignment. Rejected fixes: none; root must disposition each finding. Paper/canonical/Git edits: none. Tree change: authorized report only. Compilation/page evidence: not rerun by read-only reviewer; root must compile after accepted edits. Remaining concerns: none beyond the listed clarification opportunities. Next node: root disposition, subsection-sized fixes, compilation/preservation checks, then Round 4 abstract/intro rebuild.

## Root disposition/build/diff audit

Accepted both Should-fix findings: caption now explicitly excludes verification of post-boundary suffixes, preserving legitimate earlier accepted context; native artifact validation is explicitly at the enclosing verifier, separate from matched operation-output reference comparison. This expresses the existing contract without inventing per-operation certificates. Applied Consider3 conditional preparation-savings wording consistent with cheap/low-locality cases and Consider4 placement cross-reference using existing criterion only, no algorithm/threshold invented. Full user scope retained; no research RQ/claim replacement. make exit0/PDF7pages, no undefinedreferences/fatal errors, existing underfull-box warnings. Paragraph/subsection patches inspected;4RQstrings/12placeholders/citations34/bib/numbers preserved. PaperSHA256 165ea26de0ec183aa41cc1a62f55b51ae5cec32c4850c290b2011b6bf4c69b6f. Completed 2026-10-08T01:07:47.829446+00:00. Next Round4 mandatory complete root opening rebuild, no fork.
