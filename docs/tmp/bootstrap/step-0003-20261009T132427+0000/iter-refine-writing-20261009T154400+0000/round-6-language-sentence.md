# Round 6 — Sentence structure

Observed start checkpoint: 2026-10-09 15:59:16 UTC (after first combined source read). The complete current paper was then reread separately because the combined output truncated its middle. Completion time is recorded below from the actual clock. Parent: BOOTSTRAP step-0003-20261009T132427+0000, WRITE gate, iter-refine-writing-20261009T154400+0000. Entry baseline supplied by root: c62e427; reviewed working revision is the completed Round 5 paper, whose abstract now says “modify branch-local state”. Root reports preceding build exit 0 and eight PDF pages; this review does not claim independent compilation.

Read scope: docs/user-instruction.md FIRST; full /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md; entire current docs/paper/main.tex, including inline figure/caption, four contributions, four RQs, all twelve result placeholders and conclusion. Method: sentence-by-sentence check of punctuation, grammatical subjects/verbs, modifiers, actor ownership, note-like runs, and clause length. Present-tense intended implementation and unanswered RQs are valid BOOTSTRAP writing. No new scientific facts, numerical changes, or hedge removal are proposed.

## Must-fix

None. No dangling modifier, fragment, semicolon-joined independent clause, or clear grammatical error was identified.

## Should-fix

### S1 — Abstract L15, subject–verb distance

Quote: “Established result caches, persistent environments, proof-state snapshots and bounded warm services recover substantial reuse”.

Problem: the long compound subject postpones “recover” past the seven-word subject–verb guideline. The rest of the sentence also packages the unresolved comparison as a trailing participle. This is central positioning prose, so a shorter grammatical subject would help.

Concrete suggestion: “Established reuse mechanisms recover substantial preparation through result caches, persistent environments, proof-state snapshots and bounded warm services. Their comparison with independent native execution at equal resources remains unresolved.” Keep all four mechanisms and the equal-resource qualification. Alternatively retain “substantial reuse” verbatim to avoid suggesting all cache benefits are preparation savings: “Established mechanisms recover substantial reuse through result caches, persistent environments, proof-state snapshots and bounded warm services. Their comparison with independent native execution at equal resources remains unresolved.” The second version is the safer exact-meaning choice.

### S2 — Abstract L19, overloaded coordinated predicates

Quote: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers ... and assess remaining heterogeneous checking ...”.

Problem: the second verb arrives after a long comparison object, workload phrase and two baseline classes. The sentence combines evaluation boundaries, competitors and device cost accounting in one long structure.

Concrete suggestion: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse. We assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.” Preserve the full competitor scope, workload boundary and all costs. This is a sentence split, not a narrower comparison.

### S3 — Implementation overview L128, elided second comparison verb

Quote: “For each verifier, qualification first compares fresh adapter execution with the original interface, then prepared branches with that reference, before measuring reuse.”

Problem: the second comparison drops “compares”; the resulting comma-separated steps read as compressed procedure notes. The final measuring participle also leaves the actor implicit.

Concrete suggestion: “For each verifier, qualification first compares fresh adapter execution with the original interface and then compares prepared branches with that reference. We measure reuse after these comparisons.” Preserve qualification ordering; do not replace the condition with a claim that every tested adapter passes.

## Consider

### C1 — Design, branch lifetime L113, four short declaratives

Quote: “The lifecycle separates retained preparation from speculative work. A cancelled or incomplete attempt cannot become a new prepared parent. Branch failure returns an explicit native or service failure and leaves other branches independent. The evaluation includes failed attempts and cancellation recovery rather than reporting only successful candidate throughput.”

Problem: the four concise sentences read slightly like notes, though each carries a useful separate invariant and the last moves to evaluation. A local conjunction can smooth the middle pair without dropping content.

Concrete suggestion: leave the first and last sentences intact, and combine only the middle two: “A cancelled or incomplete attempt cannot become a new prepared parent, and branch failure returns an explicit native or service failure while leaving other branches independent.” This adds no causal assertion. Retain the original if root judges the individual invariants clearer as separate sentences.

## Coverage, preservation and disposition

No semicolon or em-dash repair was needed. The design-goal colon introduces explicitly numbered goals and complies with the skill. Contribution lists and the explicitly numbered RQ description are permitted exceptions. Parentheses are abbreviation definitions or references. Passive accounting sentences identify the methodological object adequately; no actor-changing rewrite is justified. The four protected RQs require no sentence-mechanics edit.

Applied fixes: none; report-only subagent. Rejected fixes: none; root must explicitly dispose of all three Should-fix findings and the Consider item. Alternatives: S1's first proposed wording risks overgeneralizing cache savings, so prefer its second version; C1 is optional because short distinct invariants may already be sufficiently clear. No technical content, citation, quantitative value, scope-bearing hedge, placeholder, or RQ has been changed. No code, experiment, Git operation, or memory edit occurred. Only this report is created. Root owns compilation, page validation, and diff/citation preservation checks after any edits. Next node: root fixes/builds, then serial Round 7 word choice.

| Severity | Count |
| --- | ---: |
| Must-fix | 0 |
| Should-fix | 3 |
| Consider | 1 |

Top three changes: shorten the abstract's grammatical subject (S1), split its long comparison/device sentence (S2), and make the adapter-qualification sequence grammatically explicit (S3).

Observed completed-review checkpoint: 2026-10-09 16:00:09 UTC; report creation followed that clock observation.

Root disposition: S1's safer exact-meaning alternative, S2 and S3 applied as separate Abstract/Implementation subsection edits. No mechanism or comparison was removed. C1 deferred: separate sentences keep the two failure/lifetime invariants easier to inspect. Native qualification remains ordered, not a claim that an adapter already passed. Build exit0, PDF8pages; cumulative diff preserves4RQ meanings,12result placeholders and37cite expressions. No quantitative value changes. User scope remains real Lean/SMT verification and complete GPU assessment. Next: serial Round7.

Recovery qualification —2026-10-09T18:33Z: the retained round-6-build.log is actually zero bytes after recovery. Earlier root disposition records compileexit0/PDF8, but that empty log does not independently reconstruct its historical invocation. It remains preserved, not refilled or replaced with a fabricated old build. Current round-11-build.log independently validates the complete current source including these repairs (exit0/eightpages). No experiment/raw response or scientific claim depends on the missing old compile log. This is a historical validation-evidence limitation, not a new writing review or source change.
