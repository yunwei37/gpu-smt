# Retained E025 whole-source result review

Observed 2026-10-14T21:57:45.846383+00:00

Root performed the raw recomputation and review directly. This is historical capture evidence, separate from the fresh repaired capture currently running.

| Condition | Stock whole seconds | Method whole seconds | Extra elapsed time | Native basic outcomes matched |
|---|---:|---:|---:|---:|
| rep0-branch | 1233.397 | 1539.324 | 24.80% | 3566/3566 |
| rep0-logical | 1233.397 | 1541.669 | 24.99% | 3566/3566 |
| rep1-branch | 1225.625 | 1499.149 | 22.32% | 3566/3566 |
| rep1-logical | 1225.625 | 1535.896 | 25.32% | 3566/3566 |
| rep2-logical | 1202.296 | 1538.394 | 27.95% | 3566/3566 |

All eight terminal primary cells cover the original 3,566 saved source candidates. Each has 190 successful exits, 3,359 verification failures and 17 syntax/compiler exits. The five stock comparisons above preserve the analyzed basic native results and artifacts, with no reported identity or mechanism defects. They demonstrate no whole-source throughput improvement from either reuse path under this historical protocol.

Branch reuse is 22.32–24.80% slower than stock over two complete repetitions. Logical reuse is 24.99–27.95% slower over three complete repetitions. Branch is only 0.15% and 2.39% faster than logical in the two completed trios, while both lose to stock. Rep2-branch has only 1,513 outcomes; its whole elapsed time and performance comparison are invalid. All three resource profiles are absent: no memory superiority claim.

Mechanism receipts distinguish 2,789 branch sessions per complete branch cell from only 473 logical branch sessions and 2,317 stock routes per logical cell. Preparation wall sums are approximately 6.5–6.7 seconds. These nested observations do not establish a disjoint cost attribution or prove which overhead causes the roughly 274–336 second whole-run penalty. The capture includes service, transport and native verification work; finer attribution remains open.

The workload is released AutoVerus/VeruSAGE saved sources in source-sort order, not a complete model generation/arrival trace. It has one retained parent and unlimited earlier finite history; results are conditional on that recorded execution. The old capture had SHA startup/archive gates, now forward-repaired in current development. This changes archival checking cost, so old clocks are never stitched into the fresh full-repaired1 matrix or used as identical-protocol controls.

Machine-readable raw recomputation: [analysis](full1/current-analysis-20261014T2126.json). Raw source comparisons: [compressed source analysis](full1/current-analysis-20261014T2126-sources.jsonl.gz). Failed/partial original receipts remain untouched.

Research decision: retain these negative whole-source results; do not promote branch/logical reuse as an acceleration contribution. Lean remains the priority. Complete the already admitted Lean full matrices and the fresh SMT matching matrix before updating paper performance claims.
