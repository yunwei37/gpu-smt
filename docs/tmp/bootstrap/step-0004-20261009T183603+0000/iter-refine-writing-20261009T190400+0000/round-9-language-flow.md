# Round 9: language flow and polish

Started: 2026-10-09T19:26:00Z. Completed: 2026-10-09T19:27:51Z.

Parent node: BOOTSTRAP step-0004-20261009T183603+0000, WRITE refinement run iter-refine-writing-20261009T190400+0000. Reviewer: fresh read-only Round 9 subagent. Objective: sentence topic/stress placement, old-to-new information threading, paragraph transitions, and consistent academic register.

## Entry and sources read

Read the complete `docs/user-instruction.md`, complete `/workspaces/.agent-state/codex/skills/iter-refine-writing/SKILL.md`, complete `/workspaces/.agent-state/codex/skills/paper-writing-style/SKILL.md`, and complete numbered `docs/paper/main.tex` (219 lines). The entry revision is the current working paper supplied by the parent after Round 8; no Git operation or paper snapshot was performed. The review uses the actual skill instructions directly because no Skill tool is available.

## Method

Examined every prose paragraph sentence by sentence, tracing each opening to established context and each ending to its principal new information. Checked transitions within and between paragraphs and sections, including the abstract, mechanism exposition, four evaluation blocks, related work, and conclusion. Distinguished necessary scientific scope from removable prose friction. Protected exact RQ text, all numerical values and citations, baseline families, native resource inheritance versus separate service accounting, source-verification versus post-export boundaries, qualification versus online checks, and supported versus unsupported execution. Intended completed-system prose and explicit result placeholders were accepted as instructed.

## Raw findings

No Must-fix issue was found. Three Should-fix suggestions and one Consider suggestion follow.

### Should-fix 1: Abstract, L19

Quoted text: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse, and assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.”

Problem: One sentence carries the complete service comparison and then shifts to the heterogeneous comparison. The device clause receives the stress position while the equally central baseline comparison is buried in the middle. Separating the comparisons gives each its own endpoint and makes the transition from retained preparation to remaining work easier to follow.

Concrete suggestion: “We compare complete verification in Lean and systems backed by satisfiability modulo theories (SMT) solvers on public candidate streams against competent bounded warm services and native logical or serialized prepared-state reuse. After preparation reuse, we assess remaining heterogeneous checking on an RTX 5090 with full setup, transfer and CPU fallback costs.” Preserve every comparison family, hardware value, and cost component.

### Should-fix 2: Design / Bounded placement and execution, L116

Quoted text: “The service admits prepared states within a memory budget and accounts for proportional shared memory and private dirty pages. ... Proportional memory attributes each shared page across the processes sharing it~\\cite{procMemory}, and fleet memory sums these attributed amounts across service processes.”

Problem: The accounting definition arrives only after two intervening sentences about placement and concurrency. The paragraph switches from accounting to placement and back to accounting, weakening its information thread.

Concrete suggestion: Move the final sentence, unchanged and with its citation intact, immediately after the sentence beginning “The service admits prepared states”. The paragraph then develops memory accounting before moving to placement and concurrency. No metric, resource scope, or mechanism needs rewriting.

### Should-fix 3: Implementation / Process and resource handling, L144

Quoted text: “Cancellation instrumentation records the native progress reached before termination and whether the child was reaped before later work. These records establish that the child was reaped after native progress, while interruption inside a check requires separate execution-phase evidence.”

Problem: The second sentence reintroduces “records” as a vague topic and repeats the reaping event in a different temporal relationship. A backward link through the instrumentation itself lets the sentence emphasize the distinction between demonstrated progress and evidence of interruption inside a check.

Concrete suggestion: “Cancellation instrumentation records the native progress reached before termination and whether the child was reaped before later work. The instrumentation establishes reaping after native progress, while evidence of interruption inside a check requires separate execution-phase records.” Preserve the first sentence unchanged and retain the explicit limitation concerning in-check interruption.

### Consider 1: Implementation / Device path, L151

Quoted text: “Complete verification includes CPU fallback and device/runtime costs. For checker representation, existing techniques include expression layouts with integer identifiers and delayed substitution~\\cite{nanoclo,nanocloFortran}, so their use does not establish a new checking algorithm.”

Problem: The paragraph moves directly from measurement accounting to representation provenance. The transition is grammatical but somewhat abrupt because the opening phrase introduces a new topic without naming its relationship to the device path.

Concrete suggestion: Replace only “For checker representation,” with “The device path draws on existing checker representations, whose techniques include”. The complete sentence would read: “The device path draws on existing checker representations, whose techniques include expression layouts with integer identifiers and delayed substitution~\\cite{nanoclo,nanocloFortran}, so their use does not establish a new checking algorithm.” Apply only if the parent confirms that “draws on” describes the intended implementation rather than merely related techniques. Otherwise retain the original; avoiding a new implementation claim takes precedence over this optional transition.

## Preservation checks and applied/rejected fixes

This reviewer changed zero paper sentences and applied no findings. The paper remains read-only. All four RQs at L158–161, all quantities, citations, baseline families, semantic boundaries, and resource scopes remain untouched. No technical content was proposed for deletion. The abstract split preserves the full comparison; the memory-definition move preserves exact text; the cancellation rewrite retains both temporal relationships and the in-check evidence requirement. The optional device transition is explicitly conditional because its wording could add an implementation claim.

No build, compilation, page-count check, code modification, Git operation, or external source lookup was performed. Those actions are outside this read-only review and belong to the parent. Only this report was created; no memory file was changed.

## Alternatives and decision

Prefer small sentence and ordering changes to paragraph rewrites. Do not replace exact RQ wording with more conversational summaries. Do not smooth explicit unanswered-result statements into asserted findings or treat placeholders as writing defects. Do not remove limitations about timing, unsupported runtime boundaries, admissions, UNKNOWN, artifacts, or full measurement costs. Register is otherwise consistently formal and claim-oriented; broader rewrites would bring little benefit after the prior rounds.

## Remaining concerns and handoff

Remaining concerns are local prose flow, not scientific-contract defects. The three most useful changes are separating the abstract's two comparisons, placing the memory definition adjacent to its first use in the placement paragraph, and clarifying the instrumentation sentence. Parent should apply or explicitly disposition all three Should-fix findings, evaluate the conditional Consider finding, compile, verify citation/number/scope preservation, and advance to Round 10's citation gate. This review reports findings only and does not claim that fixes or compilation have occurred.

## Root dispositions and verification

2026-10-09T19:29:29.250901+00:00: S1 accepted, splitting the abstract comparison sentence into service and remaining-device comparisons while preserving all families/costs; abstract now10sentence units including missing-results slot, no omitted role. S2 accepted, moving the exact proportional-memory definition with its citation adjacent to first use. S3 accepted, linking instrumentation to progress/reaping without implying in-check interruption. C1 rejected because draws-on would assert an implementation dependency stronger than the existing representation provenance statement. All fixes local reviewed edits; all39citations/12slots/four exactRQstrings/data intact. Fresh make exit0, PDF8pages, round9-build.log nonempty. No contract change; nextRound10.
