# Round 7 — Language: word choice

Review started and completed on 2026-10-09 at 19:19 UTC; completion recorded at 19:19:41 UTC. Parent node: BOOTSTRAP step-0004-20261009T183603+0000, iter-refine-writing-20261009T190400+0000. Objective: read-only review of jargon inflation, nominalizations, vague referents, redundant hedging and verbose wording throughout the current paper.

Entry evidence revision: `docs/paper/main.tex` SHA-256 `8a3b63e6698902a19a2a4c3696eec06c03f9e9ebb432fb3b4f19aeb6b3f6e254`. No Git operation was performed. Sources read in full: `docs/user-instruction.md`, `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`, `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`, and `docs/paper/main.tex`. No Skill tool is available; actual skill files were read directly. The review treats BOOTSTRAP prose as the intended completed submission and accepts explicit result slots.

Method: sentence-by-sentence word-choice pass, with checks of each suggested replacement against surrounding definitions and protected technical scope. Existing terms such as prepared state, native execution history, copy-on-write, proportional memory, resource-bounded responses and the defined resource frontier are retained. Compound terms were inspected as a category rather than condemned by their number; no replacement of a necessary technical term is proposed. RQs, baselines, quantitative values, citations and missing-result slots are read-only.

## Must-fix

None. No word-choice defect was found that necessarily changes the reader's interpretation of the scientific contract.

## Should-fix

1. **Introduction, L30 — verbose nominal phrase.** “the unresolved comparison is whether separating native preparation from candidate execution history improves complete verification” uses an abstract noun where a direct question is clearer. Suggested local rewrite: “With these reuse mechanisms available, the unresolved question is whether separating native preparation from candidate execution history improves complete verification, cancellation and total memory across service processes at matched resources.” All comparison dimensions and the matched-resource scope remain intact.

2. **Design / Bounded placement and execution, L116 — metaphor obscures the cost relationship.** “Preparation sharing must pay for retained memory and branch mutation” makes sharing sound like an actor purchasing resources. Suggested rewrite: “The benefit of preparation sharing must offset the costs of retained memory and branch mutation.” This preserves both costs and the original requirement rather than asserting that it is already met.

3. **Implementation / Native adapters, L133 — unnecessary nominalization.** “only an adapter that passes interface qualification is admitted to prepared-state service execution” buries the service action in “is admitted” and “execution.” Suggested rewrite of this clause: “but the service executes prepared-state branches only with an adapter that passes interface qualification.” Retain the preceding sentence about diagnostic branching tests; rejected adapters remain usable only for diagnostics.

4. **Implementation / Process and resource handling, L145 — abstract disposal wording.** “These records establish disposal after native progress” is less direct than the preceding explicit account of reaping. Suggested rewrite of the complete sentence: “These records establish that the child was reaped after native progress, while interruption inside a check requires separate execution-phase evidence.” Reaping, native progress and the separate evidence required for interruption inside a check all remain explicit.

5. **Evaluation / Experimental setup, L165 — vague pronoun amid several recording objects.** “Affinity specifies permitted CPUs but alone does not provide CPU isolation, so we record it with topology and observations of competing work.” The antecedent is recoverable, but repeating the short noun avoids a needless backward lookup. Suggested rewrite: “Affinity specifies permitted CPUs but alone does not provide CPU isolation, so we record affinity with topology and observations of competing work.” Do not delete the distinction between affinity and isolation.

## Consider

1. **Design / Branch lifetime and cancellation, L111 — wordy policy test.** “The prepared parent remains available only while it passes the configured retention policy.” A policy is applied or satisfied rather than passed. Suggested rewrite: “The prepared parent remains available only while it satisfies the configured retention policy.” This retains the temporal and configured-policy restrictions. This is a diction preference, not a new retention rule.

2. **Related work / Heterogeneous checking, L212 — awkward modifier order.** “expensive remaining dynamic checking” requires the reader to rearrange three modifiers. Suggested local rewrite: “Our heterogeneous evaluation asks about the expensive dynamic checking that remains and complete verification costs, rather than extrapolating from input graph width.” Dynamic checking, remaining work, complete costs and the graph-width distinction all remain present.

## Preservation and disposition record

Raw findings total: 0 Must-fix, 5 Should-fix, 2 Consider. The most useful changes are the direct cost relationship in L116, explicit child reaping in L145, and active service admission wording in L133. No stacked hedges or stock verbose phrases such as “in order to,” “utilize,” or “due to the fact that” required a finding. Scope-bearing language about supported boundaries, requested artifacts, exact comparison boundaries, strongest measured CPU implementations, load-sensitive wall-time outcomes and unanswered RQs is intentionally retained.

No fixes were applied or rejected by this reviewer. The root agent owns disposition of every item, source changes, preservation checks, compilation and page-count evidence. Suggested before/after locations are listed above; source edits and compile results remain pending root execution. No paper source, evidence, Git state or memory file was changed; the only tree change is this report. Alternatives considered: broad simplification of established compound terms was rejected because those terms encode the mechanism or measurement boundary; deleting repeated qualifiers was rejected where it could weaken scope.

Remaining concerns: none within the word-choice scope beyond the reported items. Next node: root applies/dispositions findings, compiles and verifies preservation, then starts Round 8 terminology and claim tone.

Root disposition 2026-10-09T19:21:42.863677+00:00: appliedall5Should-fix andbothConsider by local sentence/clause replacements at listed locations: direct unresolvedquestion, literal benefit/costrelation, active qualified-adaptercondition, explicitreaping, repeatedaffinitynoun, retentionpolicy satisfaction and remainingdynamicwork modifierorder. No removal or newmechanism, no alteredscope/quantitativevalue. Fresh compile exit0/8pages(round7-build.log); reviewed diff preserves39citations/12slots/4RQstrings. Allfindings disposed,roundcomplete,nextRound8.
