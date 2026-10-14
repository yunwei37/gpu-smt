# Round 9 — Language flow

Started: 2026-10-14T09:11:25.523272+00:00
Completed: 2026-10-14T09:11:26.583026+00:00
Parent: BOOTSTRAP step0007 WRITE_GATE. Entry HEAD582132d969286899e35c72ad74643aaa58bf30da, dirty paper source.

## Objective and method
Checked old-to-new information flow, topic/stress positions, transitions and register across every section. Should-fix: the RQ4 decomposition paragraph switches from 'separate costs' to 'these complete CPU/device paths' before explaining why that accounting matters. State the full-path comparison as the subject and then connect it to RQ3. Keep the causal implication that an operation-only gain cannot establish a service-frontier gain. Existing related-work groups each end in a comparison consequence; no reordering is justified.

Sources read: entire docs/paper/main.tex, references.bib, original entry source in root memory, docs/user-instruction.md, docs/evaluation.md and the designated writing skill/reference.
Raw subagent findings: none. Human explicitly forbids delegation; these are root self-review findings, not independent review.

## Applied changes
Location: Evaluation / Heterogeneous execution, cost-decomposition paragraph

Before:
> These complete CPU/device paths use the service accounting and matched workload boundary of RQ3, so improving a checking operation alone does not establish an improvement in the service frontier.

After:
> The complete CPU/device comparison uses the service accounting and matched workload boundary of RQ3. An improvement in a checking operation alone therefore does not establish an improvement in the service frontier.


## Preservation, alternatives and remaining work
Same accounting boundary, RQ3 relationship and operation-versus-service distinction retained. No new hypothesis or changed quantitative conclusion. All qualifiers and citation keys remain.
No invented results, numerical edits, scope removal or RQ changes were applied. No citations were removed. No memory files changed. Reviewer independence remains unavailable; complete research evidence remains open.
Compile exit: 0; pages: 9. Full output is retained beside this report.
Next node: Round10 citations.
