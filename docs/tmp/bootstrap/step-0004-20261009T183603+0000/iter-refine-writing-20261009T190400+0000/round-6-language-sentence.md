# Round 6 — Sentence mechanics

The read-only sentence review completed at 2026-10-09 19:18:02 UTC. The first recorded clock observation during this review was 2026-10-09 19:17:49 UTC; reading began before that observation, so an exact start time is not claimed. Parent node: BOOTSTRAP step-0004-20261009T183603+0000, iter-refine-writing-20261009T190400+0000. Next node: root applies or rejects the finding, compiles and records preservation evidence, then proceeds to Round 7.

## Objective and sources

Review the complete current `docs/paper/main.tex` for sentence mechanics, especially independent-clause semicolons, fragments, excessive subject–verb separation, weak openings, dangling modifiers and colons introducing unlabeled lists. Read `docs/user-instruction.md` first, then the complete actual `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md` and `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`, then the entire paper. Direct file reads loaded the instructions; no unavailable Skill tool invocation is claimed.

Entry paper SHA-256: `ef50704c08df3c12083c55c4843b2c9cb4de4b39e0c4ec8be308d99196148416`. No Git operation was performed. No evidence artifact was consulted or changed because this round concerns sentence mechanics. BOOTSTRAP present-tense intended system descriptions and explicit result placeholders were accepted.

The method was a sentence-by-sentence reading of every paragraph, with line-numbered source inspection. Scientific meaning, four RQs, both verifier families, RTX 5090, strong established reuse comparisons, complete costs, citations, numbers and operational scope were treated as protected. Clearly interpretable compound subjects were not flagged solely because their enumerations exceeded a mechanical word threshold.

## Raw findings

### Must-fix

None. No sentence fragments, dangling modifiers, weak “It is/There are/This is” openings, or independent-clause semicolons were found in narrative prose. The design-goal colon introduces explicitly numbered items and is acceptable. Figure labels and result-placeholder descriptions are intentionally labels rather than sentence fragments.

### Should-fix

**S1 — Introduction, line 36.**

> Supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes address runtime compatibility and memory use, with native execution for unsupported boundaries, while children inherit native resource state with branch-owned communication and separate service accounting.

Problem: the long compound subject postpones “address,” and the sentence then embeds fallback before introducing a second subject and another bundle of mechanisms. The insertion separates the compatibility statement from the child-resource statement and makes their relationship harder to follow.

Concrete fix suggestion:

> Supported quiescent boundaries address runtime compatibility together with untouched candidate suffixes and bounded prepared-state lifetimes, which also address memory use. Unsupported boundaries use native execution. Children inherit native resource state with branch-owned communication and separate service accounting.

An even more conservative alternative preserves the original first clause verbatim and merely splits the trailing material:

> Supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes address runtime compatibility and memory use. Unsupported boundaries use native execution. Children inherit native resource state with branch-owned communication and separate service accounting.

Prefer the conservative alternative: it removes the interrupting fallback phrase and the overloaded second clause without assigning a more specific design-goal role to each component than the original sentence does. Its compound subject remains long but is immediately interpretable.

### Consider

None. No additional edits are proposed merely to shorten already clear sentences.

## Decisions and verification boundary

One Should-fix, zero Must-fix and zero Consider findings. The main improvement is to separate the introduction's compatibility/fallback/resource-handling statements. No top-three list is manufactured for a single finding.

The read-only reviewer applied no paper fixes and rejected no root findings. The proposed conservative rewrite preserves all technical components and their original scope and introduces no citation or quantitative changes. Four RQs and their scientific wording remain untouched. Both Lean and SMT-backed verification, RTX 5090, baseline strength and complete-cost accounting remain untouched.

Compilation and page-count checks were not run by this reviewer and are not claimed. Root must log its actual applied/rejected decision, before/after location, source diff, citation/number preservation and compilation/page evidence after handling S1. Only this report was created; no paper, memory, implementation, evidence or Git state was changed.

Remaining concern: none beyond root's disposition of S1 and required post-fix verification. Alternatives were considered above, and the conservative split is recommended specifically to avoid a finer-grained attribution that could change meaning.

Root disposition 2026-10-09T19:19:22.738284+00:00: appliedS1 conservative sentence split, preserving compatibility/memory attribution, nativefallback and allchild communication/accounting components. This supersedes Round4 sentence-combination polish: approximate paragraph-length guidance cannot override clarity/content retention, and no re-review is added. Root also removed unnecessary new fallback-box width scalar, using existing linewidth; Round0’s added0.95 was layout only, not a scientific result, and cumulative finalnumeric tokens are unchanged. Fresh compile exit0/8pages(round6-build.log), reviewed diff preserves39citations/12slots/4RQstrings and scientific meaning. No otherfindings. Round complete,nextRound7.
