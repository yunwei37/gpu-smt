# Complete native eight-queue CPU pair

This is root self-review of one complete pair on the original 1,000 released
arithmetic-heavy GoedelWorkbook candidates.

## Protocol and complete result

Both conditions use the same pinned Lean4.27/native compilation family,
prepared root, upstream eight sequential queues, at most eight candidate
tasks, CPUs0–3 and48GiB address-space allowance. Candidate input order is
unchanged. Whole time includes preparation, all native work, queueing and final
EOF/child retirement. The one-array API has no artificial300second client
deadline; native command/heartbeat behavior is retained. This does not prove
timeout equivalence for sources that would hit the older per-array deadline.

| Condition | Whole seconds | Native / condition |
| --- | ---: | ---: |
| Compiled native | 685.730742286 | 1.000000 |
| CPU AST arithmetic oracle | 537.312851014 | 1.276222486 |

Each condition returns992complete/eightrejected/zerooperational outcomes.
All1,000proofIDs,source verdicts and non-message native response fields agree.
The CPUoracle has88warning-only accepted-source differences. All1,000actual
candidate task spans are present and unambiguously mapped in each condition.
The paired analyzer retains native-selected and method-selected1%/10%tails.
This is one observation,not an estimate of repeatability or continuous service
capacity. There is no GPU execution in this pair.

## Strongest-baseline consequence

The earlier native eight-item-wave reference is1237.370439599seconds; its
CPUoracle is1037.849203905seconds. The new available native interface is
stronger. The queue API already exists upstream and is not a new runtime,
compilation or systems contribution. The first24qualification changes only
the submission interface on the same timingbinary; this full pair is a later
epoch,so the absolute difference is not a replicated isolated scheduling study.

The current full CPUoracle ratio1.27622x is below the user's more-than1.5x
continuation target. The earlier full GPU ratio1.21296x and answer-aware
omission1.59976x belong to the eight-item-wave protocol. They do not establish
heterogeneous gain or an opportunity ceiling against this stronger queue
baseline. A matched queue-family all-call profile must use its own reference
clock before making another zero-numerical-cost calculation.

GPU route closure is not justified by these timings alone. No fresh full GPU
variant is admitted from the adverse/small single-point qualifiers. All four
RQs,systems novelty and complete paper evidence remain open. This report is
self-review,not independent audit or a venue acceptance claim.

## Reproduction

The launch, completed-cells ledger, complete terminal JSON, both raw response
arrays, task timings and process resources are adjacent. Run the existing
analyze-batch.py with this directory and methods fast-hybrid oracle-hint.
All data are losslessly compressed. [Closed native reference detail](native-reference-review.md)
is retained as the earlier intermediate boundary; this report closes its
previously pending CPU counterpart.
