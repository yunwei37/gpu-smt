# Round 7: word choice

Parent: `/root`, serial BOOTSTRAP step 0002, iter-refine-writing Round 7.
Started: 2026-10-08 01:15:53 UTC (actual clock).
Completed review: 2026-10-08 01:16:29 UTC (actual clock before report write).

Read directly: `docs/user-instruction.md`, `docs/questions-for-author.md`, the complete `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`, and all of current `docs/paper/main.tex` (207 lines). The initial combined read was output-truncated, so a second numbered read covered the complete paper. Procedure: reviewed every paragraph for word-level inflation, compounds, nominalizations, vague pronouns, stacked hedges and verbosity. Read-only review exception applies: this report is the sole authorized write; the parent applies edits and recompiles. No paper edits, build or Git operations performed.

## Must-fix

None found in this round's word-choice scope.

## Should-fix

1. **Implementation, L126**: “Adapter qualification compares both paths with the original verifier interface before measuring reuse.”
   Problem: “both paths” follows a description of SMT and Lean adapters, but the intended comparison appears to be fresh adapter and branched execution, not SMT against Lean. The pronoun masks the comparison's subjects.
   Concrete fix: “For each verifier, adapter qualification compares fresh adapter execution and branched execution with the original verifier interface before measuring reuse.”
   Alternative: “Adapter qualification compares fresh and branched execution with the corresponding original verifier interface before measuring reuse.”
   Uncertainty: verify intended subjects against the qualification protocol. If this sentence concerns only fresh interface qualification, use “Adapter qualification compares fresh adapter execution with the original verifier interface before measuring reuse.” Do not silently enlarge the test requirement.

2. **Design / Bounded placement and execution, L116**: “Placement favors states whose observed preparation work is reused often enough to offset creation and retention.”
   Problem: “creation and retention” hides what is created/retained and which costs the reuse offsets. This is unnecessary noun compression in the design's central cost criterion.
   Concrete fix: “Placement favors states whose observed preparation work is reused often enough to offset the costs of creating and retaining those states.”
   Alternative: “Placement favors states whose preparation savings offset their creation and retention costs.”
   Uncertainty: prefer the first fix, which preserves “observed” and “often enough”; the shorter alternative could obscure the observed-work criterion.

3. **Evaluation / Latency, throughput and memory, L172**: “Preparation creation, replacement and cache costs are charged to the measured service.”
   Problem: “preparation creation” is an awkward compound and leaves readers unsure whether creation refers to prepared states or preparation work.
   Concrete fix: “The measured service is charged for creating and replacing prepared states and for cache costs.”
   Alternative: “Prepared-state creation, replacement and cache costs are charged to the measured service.”
   Uncertainty: both preserve required costs; use the first if cache costs include mechanisms beyond the prepared-state cache.

## Consider

4. **Abstract L17 and Introduction L34**: “Realizing this separation requires ...”
   Problem: “Realizing” adds an abstract verb where the concrete implementation relation is available. This is a style preference, not missing meaning.
   Concrete fix at both locations: “Implementing this separation requires ...” Keep each sentence's existing requirements intact.
   Alternative: retain the original if the requirement is intended to apply to design as well as implementation.
   Uncertainty: low impact; no need to edit solely for variation.

5. **Design / Heterogeneous checking, L121**: “the input expression graph does not alone define dependencies”
   Problem: placement of “alone” interrupts the verb and makes the limitation slightly harder to parse.
   Concrete fix: “the input expression graph alone does not define dependencies”.
   Alternative: “dependencies are not defined by the input expression graph alone”.
   Uncertainty: first fix preserves the technical claim and active subject; no dependency or fidelity qualifier should be removed.

6. **Evaluation opening, L146**: “four paper-level questions”
   Problem: “paper-level” is an unnecessary compound because this is already the paper's evaluation.
   Concrete fix: “four research questions”.
   Alternative: “four questions”.
   Uncertainty: stylistic only. Preserve all four RQ exact strings at L148–151 and their scope.

## Protected wording and rejected changes

Kept established terms: quiescent boundaries, copy-on-write, resource frontier (defined at L34), native preparation, candidate suffix, fidelity, proportional memory, context-sensitive dependencies and adapter qualification. Their noun forms encode technical concepts; replacing all nominalizations mechanically would harm precision. No stacked redundant hedge was found. Kept scope-bearing “supported”, “requested”, “matched”, “strongest measured”, conditional “can”, “where they occur”, post-export limitations, UNKNOWN handling and source-native boundary qualifiers. Kept complete Lean and SMT coverage, RTX 5090, required setup/transfer/fallback/online-check costs, every citation and every number. Missing-result placeholders and intended present tense are permitted. No broad compound renaming or removal of fidelity caveats is proposed.

Summary: 0 Must-fix, 3 Should-fix, 3 Consider; 0 sentences changed. Most impactful: clarify “both paths”; spell out the placement cost criterion; replace “preparation creation”. Parent should resolve the L126 protocol uncertainty before editing, apply accepted minimal changes, check the diff, and compile.

## Root disposition/build/diff audit

Applied all3Should-fix and3Consider items. The ambiguous paths become the existing two-stage qualification: freshadapter versus original, then preparedbranches versus that reference, as already explicit in RQ2/nativeadapters. No extra scientificrequirement added. Placement retains observed/often-enough qualifiers; creation/replacement/cache costs retain completecharging. Implementing/graphalone/researchquestions are localwordchoice only. Root scope check preserves allnative/device/fallback/strongbaseline qualifiers, exact4RQstrings/12slots/citations34 and allquantities/bib. make exit0/PDF7pages; no fatal/undefinedreference errors, existing layoutwarnings. Diff inspected, SHA256 3a9cbf8b7e8ce503bf4178ae2e1d4cb61b450cc9b10b581a9981f5bc31a47c39. Completed 2026-10-08T01:17:25.918054+00:00. Next Round8 terminology/claimtone.
