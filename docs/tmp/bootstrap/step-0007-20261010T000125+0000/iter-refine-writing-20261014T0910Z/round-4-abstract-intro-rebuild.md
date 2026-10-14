# Round 4 — Abstract and introduction rebuild

Started: 2026-10-14T09:09:48.595223+00:00
Completed: 2026-10-14T09:09:49.675337+00:00
Parent: BOOTSTRAP step0007 WRITE_GATE. Entry HEAD582132d969286899e35c72ad74643aaa58bf30da, dirty paper source.

## Objective and method
Applied the complete root procedure from rewrite-abstract-intro: mapped P1 verification streams/context, P2 concrete preparation–lifetime tradeoff, P3 native-history root cause, P4 strongest prior reuse/gap, P5 thesis, P6 runtime/resource requirements, P7 system/evaluation promise, P8 contributions. Diagnosed the logic chain before editing: P2 must lead with the concrete competing costs and P5 must connect inherited preparation to independent histories. Reorganization plan: retain all eight roles and their order; rebuild P2 and P5 individually, retaining every substantive cost/example/qualifier. Other paragraphs already fill their intended role and are retained following explicit review. Derive the abstract opening last from P1, making the sharing subject explicit. No change to thesis, claims, scope or contributions is admitted.

Sources read: entire docs/paper/main.tex, references.bib, original entry source in root memory, docs/user-instruction.md, docs/evaluation.md and the designated writing skill/reference.
Raw subagent findings: none. Human explicitly forbids delegation; these are root self-review findings, not independent review.

## Applied changes
Location: Introduction / paragraph2

Before:
> Serving independent attempts trades repeated preparation against shared execution. Running a separate verifier for every candidate repeats imports and parsing and replicates resident objects, while retained workers and shared logical environments make resource growth, contention and cancellation depend on worker isolation. For example, concurrent attempts against one imported Lean context need both that context and independent lifetimes. Cancelling one attempt must release its speculative work without ending the others.

After:
> Serving independent attempts trades repeated preparation against shared execution. A separate verifier for each candidate repeats imports and parsing and replicates resident objects. Retained workers and shared logical environments avoid that repetition, but resource growth, contention and cancellation depend on worker isolation. Concurrent attempts against one imported Lean context illustrate the tradeoff: they need the same context and independent lifetimes. Cancelling one attempt must release its speculative work without ending the others.

Location: Introduction / paragraph5

Before:
> We argue that reusable verification state should retain preparation while separating each candidate's execution history and lifetime. Native preparation of a context precedes candidate evaluation and remains available to independent attempts. Each candidate inherits that state, so other candidates neither supply its solver history nor extend its lifetime. The value of this separation depends on context preparation cost, branch creation cost and the pages that each candidate modifies.

After:
> We argue that reusable verification state should retain preparation while separating each candidate's execution history and lifetime. A context is prepared before candidate evaluation, and that native state remains available to independent attempts. Each candidate inherits the prepared state, so other candidates neither supply its solver history nor extend its lifetime. The value of this separation depends on context preparation cost, branch creation cost and the pages that each candidate modifies.

Location: Abstract / first sentence, derived last from Introduction paragraph1

Before:
> Formal verification services check streams of program and proof candidates against formal specifications, sharing libraries, declarations and accepted context.

After:
> Formal verification services check streams of program and proof candidates against formal specifications; related candidates share libraries, declarations and accepted context.


## Preservation, alternatives and remaining work
The rebuilt paragraphs retain parsing/import replication, shared-worker contention and resource growth, cancellation example, inherited state/history separation and all three cost determinants. Existing citations in other introduction paragraphs are untouched. Abstract length remains within the original prescribed range and its missing-results sentence is preserved. No claim that the proposed design has already demonstrated speedup is inserted.
No invented results, numerical edits, scope removal or RQ changes were applied. No citations were removed. No memory files changed. Reviewer independence remains unavailable; complete research evidence remains open.
Compile exit: 0; pages: 9. Full output is retained beside this report.
Next node: Round5 consistency.
