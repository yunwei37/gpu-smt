# Round 5: paper consistency review

Started 2026-10-09T19:15:29+00:00. Parent Step0004/WRITE; objective: serial read-only consistency review of the complete current submission. Entry paper SHA-256: `8ce6cbefc39fa2618e8031f465662bbe1e147d98a17efdfdf3382e3473414083`; parent supplied base revision3b035d2, no Git operation performed by this reviewer.

Read docs/user-instruction.md first; then the complete actual iter-refine-writing/SKILL.md, check-terminology-infoflow/SKILL.md and references/paper-consistency.md; full docs/paper/main.tex including its inline architecture figure; docs/design.md, docs/implementation.md, docs/evaluation.md, docs/research-plan.md, docs/idea-story.md; current experiment005 result review and round4 report. Direct filesystem skill access was used; no unavailable Skill tool invocation is claimed. Review compared architectural ownership, qualification ordering, boundary semantics, accounting, evidence promises, RQ wording and figure paths. BOOTSTRAP completed-submission convention was enforced: unfinished implementation status does not invalidate present-tense system descriptions; explicit result placeholders remain unfilled. No absence claim about an experiment or artifact is made.

## 1. Inconsistencies found

- **Should-fix / minor — parser lifetime ambiguity (Implementation opening, L128 versus Native adapters L135).** The opening says the adapter “retains Z3's native command context and parser,” whereas L135 describes separate parser invocations with retained command context. Experiment005's independent source review states the parser is local to each invocation around an owned surviving context. Readers can interpret the opening as retaining the parser object across EOF, which is a different mechanism.
- **Should-fix / minor — cancellation observability overstatement (Process and resource handling, L144).** Recording “native progress reached before termination” and whether a child is reaped does not by itself establish whether termination occurs inside a solver check. The next sentence says “This distinguishes interruption during a check from disposal after its response.” Experiment005 explicitly supports disposal after native progress and excludes an in-solving conclusion. This is an instrumentation inference issue, not a complaint about unfinished service status.
- **Must-fix:** none.
- **Consider:** none requiring a paper edit. Historical docs/research-plan.md contains an older five-RQ transparent-runtime framing, whereas docs/idea-story.md explicitly owns the current four-RQ contract. Preserve the latter authority; do not import the legacy RQs or constraints into this writing pass.

## 2. Why each matters

Parser lifetime is load-bearing because split EOF qualification distinguishes parser effects from branch effects. The proposed minimal bridge preserves native parsing and configuration while correctly identifying the retained object.

Cancellation receipts establish termination and post-disposal sibling behavior, but native output can be buffered and a response can precede later artifacts or cleanup. Equating progress receipts with exact in-check interruption overstates what that measurement establishes. The paper should preserve cancellation as an evaluation obligation without implying these two recorded fields prove execution phase.

## 3. Exact fixes or replacement wording

1. **L128 only:** replace `The SMT adapter retains Z3's native command context and parser to evaluate ordered session state~\cite{z3api}.` with `The SMT adapter retains Z3's native command context across native parser invocations to evaluate ordered session state~\cite{z3api}.` This aligns the overview with L135 and the source-qualified mechanism without changing the scientific contract.
2. **L144 second sentence only:** replace `This distinguishes interruption during a check from disposal after its response.` with `These records distinguish disposal after an observed response from termination before a response is observed; establishing interruption inside a check requires execution-phase evidence.` This keeps native progress/reaping instrumentation and cancellation scope while avoiding a false phase inference. An equally minimal alternative is `These records establish disposal after native progress; interruption during a check requires separate execution-phase evidence.`

No paper edit was made. Root owns application/rejection of these findings and compilation. Both Should-fix recommendations are local and preserve all existing RQs, numerical values, citations, result slots and method scope.

## 4. Broader follow-up checks

Architecture passes: immutable parent does no candidate verification; branch owns candidate mutation/lifetime; original preparation retains accepted context; unsupported boundary goes to native execution; Figure1 depicts both supported and unsupported paths consistently. Qualification passes: original executable→fresh adapter→split parsing/branch, with rejected paths excluded from service evaluation. No UNKNOWN-only fallback or extra logical scope is introduced.

The four RQ strings match docs/idea-story.md and their evidence blocks retain their meanings. Contributions and goals map coherently to RQ1 sharing, RQ2 behavior/isolation, RQ3 matched frontier and RQ4 complete heterogeneous execution. Strong bounded warm/cache and native logical/serialized reuse remain explicit in abstract, intro, setup and related work. Lean and SMT scope, RTX5090, complete setup/transport/fallback costs, failed/incomplete attempts and fleet memory remain intact. No empirical speedup, response-count or memory number is promoted into the paper; final evidence slots are explicit. No unsupported closure of any RQ is asserted.

No conflicting math notation, unresolved component renaming, hardcoded system name, table metric mismatch or cross-reference target inconsistency was found. Figure1 is inline in main.tex and no separate figure file is needed. Paper-wide parser and cancellation wording should be reread after any accepted local fix; no global terminology substitution is warranted.

Applied fixes: none by this read-only reviewer. Rejected fixes: none; two Should-fix decisions await root. Alternatives: no broad rewrite, status downgrade or result filling, because each would exceed this diagnostic round. Tree changes: this report only; no memory, source, experiment or Git changes. Compilation/page evidence: parent Round4 records clean8pages; this reviewer changed no TeX and does not claim a fresh compile. Remaining concerns are the two local wording ambiguities above; missing final results are protected BOOTSTRAP placeholders, not writing defects. Next node: root applies/disposes findings, compiles and advances serial Round6.

Completed 2026-10-09T19:16:46.390879+00:00.

Root disposition 2026-10-09T19:17:33.837437+00:00: applied both Should-fix by two local sentence changes: retained native command context across parser invocations, and explicit distinction between disposal receipts and separate in-check execution-phase evidence. No cancellation evaluation obligation removed or technical timing claim invented. Legacy-plan Consider accepted as canonical housekeeping outsidepaper, preserving original historical text while marking its authority; not a new scientific contract. Fresh compile exit0/8pages(round5-build.log), diff preserves39citations/12resultslots/4RQstrings and numbers. Round complete,nextRound6.
