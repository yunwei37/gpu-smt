# Round 6 — language: sentence structure

Parent: /root. Reviewer: /root/step2_writing6.
Actual start clock: 2026-10-08 01:12:52 UTC. Actual final pre-write clock: 2026-10-08 01:13:44 UTC.
Read method: complete, untruncated shell cat of docs/paper/main.tex; numbered inspection plus separate lines 65–104 read. Complete actual /workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md read. Its directory contains only SKILL.md and it names no required external references. Resolved the nonexistent shorthand docs/user-instruction/questions to docs/user-instruction.md and docs/questions-for-author.md, both read fully before findings. No Skill tool used.

Read-only sentence review throughout abstract, every section, caption, contributions and exact four RQ strings. Report creation alone is authorized; root applies changes and builds. No paper/canonical/Git edits. All claims, numbers, citations, scope-bearing qualifiers, supported/native boundaries, CPU/GPU/native costs, fallback, baseline strength, RQ strings and missing-result markers are protected. Intended completed-study present tense is permitted. No scientific critique or reframing.

## Must-fix

1. Design / Heterogeneous checking, L123: “while enclosing native verification checks its resulting proof or requested artifact.”
Problem: “its” can refer to qualification, outputs or enclosing verification. Explicitly name the checked result.
Fix: replace only “its resulting” with “the resulting”. Full sentence: “Device qualification compares operation outputs with matched CPU references before admission, while enclosing native verification checks the resulting proof or requested artifact.”
Alternative: none needed; this smallest edit preserves qualification/online-check distinctions.

## Should-fix

2. Design / Heterogeneous checking, L123: “Required online checks are charged to complete verification; qualification does not imply a second full CPU replay on every request.”
Problem: independent clauses joined by semicolon.
Fix: “Required online checks are charged to complete verification. Qualification does not imply a second full CPU replay on every request.”
Alternative: use “, and qualification”; prefer two sentences for the explicit protected-cost statement.

3. Introduction, L24: “Verifiers backed by satisfiability modulo theories (SMT) solvers translate program obligations into solver requests.”
Problem: noun head “Verifiers” and predicate “translate” are separated by a nine-word modifier including abbreviation.
Fix: “SMT-backed verifiers translate program obligations into solver requests.” The abstract already expands SMT.
Alternative if section-local expansion is required: “Verifiers translate program obligations into requests to satisfiability modulo theories (SMT) solvers.” Preserve backend and translation meaning.

4. Evaluation / Preparation sharing, L162: “Reuse of results for exact duplicate attempts, sharing of ordered native prefixes and sharing of native environments are analyzed separately.”
Problem: long coordinated subject delays the predicate and burdens the three-boundary comparison.
Fix: “We separately analyze result reuse for exact duplicate attempts, sharing of ordered native prefixes and sharing of native environments.”
Alternative: “We analyze three forms of reuse separately: (1) results for exact duplicate attempts, (2) ordered native prefixes, and (3) native environments.” Prefer first for minimal narrative change.

5. Implementation / Device path, L141: “Expression layouts with integer identifiers and delayed substitution are existing checker techniques…”
Problem: seven-word modifier separates noun head “layouts” from predicate “are”; active subject-first framing shortens the parse.
Fix: “Existing checker techniques include expression layouts with integer identifiers and delayed substitution~\cite{nanoclo,nanocloFortran}, so their use does not establish a new checking algorithm.”
Alternative: retain original; borderline distance rather than unequivocal violation. Preserve attribution and algorithm qualifier exactly; no novelty reassessment.

## Consider

6. Abstract, L19: long sentence combines complete baseline comparison with device assessment; second verb “assess” arrives far after “We”.
Fix: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse. We assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.”
Alternative: retain original if abstract flow favors one sentence. Drop no costs or baseline qualifiers.

7. Background / Verification stages and outcomes, L48: “Imports prepare declaration environments before a candidate is elaborated. Kernel checking validates proof terms against the dependent type theory. Post-export checker replay begins after the source frontend has already run.”
Problem: three short declaratives create mild note-like rhythm.
Fix: “Imports prepare declaration environments before candidate elaboration, while kernel checking validates proof terms against the dependent type theory. Post-export checker replay begins after the source frontend has already run.”
Alternative: retain original because distinct stage definitions are useful. Never blur post-export and source boundaries.

8. Design / Observable behavior, L108: “Fallback follows interface compatibility, rather than treating every UNKNOWN response as a detector of divergence.”
Problem: abstract “Fallback” becomes the implied actor of “treating”; meaning is recoverable but actor could be clearer.
Fix: “The service chooses fallback according to interface compatibility, rather than treating every UNKNOWN response as a detector of divergence.”
Alternative: retain the concise original. Preserve distinction from response-triggered fallback.

## Remaining concerns and complete checks

Only one independent-clause semicolon found, item 2. Design colon introduces explicit (1), (2), (3) goals and is permitted. Result-marker macro colon is non-narrative syntax. No weak “It is”, “There is/are” or “This is” sentence openings. “This paper makes four contributions” has a concrete subject. No narrative fragments; contribution fragments and figure labels are structured exceptions. No unequivocal dangling modifier found. Remaining long coordinated subjects are understandable and do not justify blanket rewriting. No narrative em-dashes. Citation/abbreviation parentheses and figure references are allowed. Exact RQ strings and corresponding subsection formulations should remain untouched.

Totals: 1 Must-fix, 4 Should-fix, 3 Consider. Top three: disambiguate L123 result referent; split L123 semicolon; place the L162 analysis actor before the long comparison list. Root should evaluate every suggested alternative, record retained wording, diff-check all protected content and build. No sentences changed or build claimed by reviewer.

## Root disposition/build/diff audit

Applied Must-fix1 resulting-result referent; all4Should-fix: splitsemicolon, shorten translation subject via suggested variant retaining SMTbody expansion, make reuse-analysis subject active, make existing-techniques subject active with samecitations/noveltyscope. Consider6 abstract split rejected: one methodology unit preserves strict opening role correspondence and allresource/baseline/devicecost clauses; Consider7 retain distinct neutral stage definitions for technical boundary clarity, not rhythmic merging. Applied Consider8 serviceactor fallback clarification. Root self-check additionally restores verbatim existing supported-device semantic-preservation claim as its own sentence, so Round5 validation-role clarification does not implicitly weaken that intended property. No new algorithm/certification/evidence invented; canonical says fullservice unfinished. Paragraph/subsection changes inspected. Initial apply_patch matched an inline sentence as a wholeline and failed before any mutation; corrected wholeparagraph context and allrequested edits applied. make exit0/PDF7pages; no fatal/undefinedreference errors, existing layoutwarnings. 4RQstrings/12slots/citations34/bib/numbers unchanged; sourceSHA256 be622c0ebc3d0027aca46705e1e23b039e7c50f917353965f782a285c1801d5b. Completed 2026-10-08T01:15:42.698470+00:00. Next serial Round7 wordchoice.
