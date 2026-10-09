# Round 6 — Sentence structure

Started: 2026-10-09 23:41:50 UTC. Completed: 2026-10-09 23:43:06 UTC.

Parent: BOOTSTRAP step-0006-20261009T222500+0000, WRITE run iter-refine-writing-20261009T233309+0000. Reviewer: serial read-only subagent assigned by the root orchestrator. Objective: review complete current paper sentence mechanics without source or scientific changes.

Read in order: complete `docs/user-instruction.md`, complete root `iter-refine-writing/SKILL.md`, complete root `paper-writing-style/SKILL.md`, complete `docs/paper/main.tex` lines 1–238. Initial output was display-truncated; overlapping follow-up reads, including a separate read of lines 125–142, completed full coverage. Source SHA-256: `1ae91025434c984ec4088a9ae2cc1bf85028f6b7fc2493cb0cb9afada4d43abf`. No Skill invocation tool is exposed, so both full skill files were loaded directly. No Git operation occurred.

Method: reviewed every sentence against punctuation and structure rules and the eight quick self-edit questions, including semicolons, fragments, subject–verb distance, weak openings, unlabeled colons, dangling modifiers, passive actors, short-declarative runs, referents, topic/stress placement and protected hedges. Structured contributions, RQs, figure labels and result placeholders were distinguished from narrative sentences. BOOTSTRAP system descriptions retain intended-completed-system tense.

## Must-fix

None. No sentence-level clarity or logic defect requiring a scientific interpretation change was found.

## Should-fix

### S1 — Abstract, line 16

Quote: “Native scope, heuristics, runtime objects and resource counters make this tradeoff depend on execution history beyond the logical context, requiring separate arguments about observable verification behavior.”

Problem: the long compound subject postpones the main verb, while the final participial clause adds the implication to an already dense sentence.

Concrete fix: “This tradeoff depends on native execution history beyond the logical context, including scope, heuristics, runtime objects and resource counters. These properties require separate arguments about observable verification behavior.” All four properties and the separate behavior argument remain.

### S2 — Abstract, line 21

Quote: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse, then, after preparation reuse, assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.”

Problem: “then, after” packs two comparison boundaries into one sentence, leaving the second predicate far from its author subject.

Concrete fix: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse. After preparation reuse, we assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.” Baselines, sequence, complete-verification scope, hardware and all costs remain.

### S3 — Introduction, line 38

Quote: “Supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes address runtime compatibility and memory use, while unsupported boundaries use native execution.”

Problem: three technical noun phrases separate the subject opening from its verb by more than seven words.

Concrete fix: “The service addresses runtime compatibility and memory use through supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes. Unsupported boundaries use native execution.” Every mechanism and the native fallback remain.

## Consider

### C1 — Background, Verification stages and outcomes, line 50

Quote: “Lean source verification includes parsing, elaboration, proof construction and kernel checking. Imports prepare declaration environments before a candidate is elaborated. Kernel checking validates proof terms against the dependent type theory.”

Problem: three consecutive short declaratives read somewhat like stage notes. The current version is clear; this is optional polish.

Concrete fix: retain the first sentence and citation, then combine the next two: “Imports prepare declaration environments before a candidate is elaborated, while kernel checking validates proof terms against the dependent type theory~\cite{lean4}.” Retain the following post-export distinction and citations. This preserves every stage and its role.

## Checks with no further findings

No narrative semicolon joining independent clauses, em-dash, grammatical fragment, weak “It is/There are/This is” opening, dangling introductory modifier or unlabeled narrative colon was found. The numbered design-goal colon is permitted. Compact diagram labels are structured content. Parenthetical references and first-use abbreviations are permitted. Passive constructions have obvious methodological actors or foreground the outcome appropriately. Other referents and topic/stress positions were sufficiently clear for this round; word-choice-only changes are deferred.

No hardcoded proposed-system name violates the system-macro rule: the paper describes “the service” without introducing a named proposed system. Names of Lean, Z3 and cited competing systems must remain intact.

## Disposition and preservation

Raw findings: 0 Must-fix, 3 Should-fix, 1 Consider. Top changes: split the abstract comparison sentence, shorten the introduction mechanism subject, and separate the abstract native-history implication.

Applied fixes: none, under the read-only assignment. Rejected fixes: none; the caller evaluates each finding. Sentences changed: 0. Only this report was written. No paper/source, canonical, Git, build or native-execution change occurred. Compilation/page evidence was not collected; no build success is claimed. An attempted report write through `python` failed because that executable is absent; the report was then created with `apply_patch`.

Suggested fixes preserve all numbers, citations, four RQs, protected hedges, complete verification, cancellation, native warm/cache comparison, matched CPU/memory and RTX 5090 setup/transfer/fallback scope. Result placeholders remain explicit and unfilled. Wider paragraph rewrites were rejected in favor of targeted sentences. No scientific-contract defect is inferred by this review.

Next node: root orchestrator applies or explicitly dispositions these findings, performs its authorized compile and preservation checks, then launches serial Round 7.

Root disposition: all3Should clarity concerns applied with targeted sentence recasts. Proposed splitting both abstractsentences rejected as an applicationdetail because it breaks required9role/sentence correspondence; instead explicitnativehistory subject and conjunctive assessment remove dense subject/then-after construction within one sentence/role. S3 uses service as grammaticalsubject and retains allthree mechanisms plusunsupportedfallback inone sentence. Consider C1 accepted joiningimports andkernelrole, preserving both Lean citations. No scope/number/RQ/technicaldeletion; reviewed subsectiondiff,47cites/12slots retained. make exits0/build-round6.log;current9pages (checked buildlog), no venueclaim. NextRound7words.
