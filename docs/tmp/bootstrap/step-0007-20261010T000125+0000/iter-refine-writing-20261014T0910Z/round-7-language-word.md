# Round 7 — Word choice

Started: 2026-10-14T09:10:53.923476+00:00
Completed: 2026-10-14T09:10:55.019082+00:00
Parent: BOOTSTRAP step0007 WRITE_GATE. Entry HEAD582132d969286899e35c72ad74643aaa58bf30da, dirty paper source.

## Objective and method
Checked nominalizations, vague referents, jargon inflation and verbose phrases throughout. Should-fix: Implementation opens with the abstract phrase 'maps the design onto', while its subject is the system that implements the design. Replace with 'implements the design through' without changing the adapter/process/service list. Consider replacing 'resource frontier' was rejected: the introduction explicitly defines the existing latency/throughput/memory meaning and a new synonym would obscure that mapping. No branded supporting term is introduced.

Sources read: entire docs/paper/main.tex, references.bib, original entry source in root memory, docs/user-instruction.md, docs/evaluation.md and the designated writing skill/reference.
Raw subagent findings: none. Human explicitly forbids delegation; these are root self-review findings, not independent review.

## Applied changes
Location: Implementation / opening sentence

Before:
> The implementation maps the design onto native verifier adapters, process branches and a bounded service.

After:
> The system implements the design through native verifier adapters, process branches and a bounded service.


## Preservation, alternatives and remaining work
The native adapter, independent branch and bounded service mechanisms remain the same. This is an expression edit only; it does not change implemented coverage or claim performance. All protected scopes and citations retained.
No invented results, numerical edits, scope removal or RQ changes were applied. No citations were removed. No memory files changed. Reviewer independence remains unavailable; complete research evidence remains open.
Compile exit: 0; pages: 9. Full output is retained beside this report.
Next node: Round8 terminology and claim tone.
