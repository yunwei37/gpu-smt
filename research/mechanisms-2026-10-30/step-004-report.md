# Step 004 — grid kernel cost and memory-scope analysis

2026-10-30 UTC; M branch; self-review.

## Grid certificate samples

GridCertificate.lean checks the implication m*n=2005 -> m+n=406 over bounded
rectangles, with ordinary stock-kernel decide. All five sampled block theorems
print no axioms. The native process exits 0 in 11.00675 s, uses 10.98106 CPU s,
and has leader kernel RSS high water 872,542,208 bytes.

| Block | Cells | Warm kernel declaration-recheck s | Linear 4,016,016-cell estimate s |
|---|---:|---:|---:|
| 32 x 32 | 1,024 | 0.104427 | 409.55 |
| 64 x 64 | 4,096 | 0.474051 | 464.79 |
| 128 x 128 | 16,384 | 2.108383 | 516.80 |
| Includes (5,401) | 1,024 | 0.104818 | 411.09 |
| Includes (401,5) | 1,024 | 0.102512 | 402.04 |

These are sampled warm checks and a linear estimate, not an executed full-grid
certificate or a proven upper bound. They exclude initial checking, proof
construction, block-coverage/equivalence lemmas and orchestration. Size effects
are visible: cost per cell increases with block size.

The optimized C numeric scan of that grid takes approximately 2.38 ms. This
large gap argues against treating GPU numeric evaluation alone as the solution:
a checker that redoes every arithmetic test remains expensive. A compact,
proved certificate or algebraic reduction is required. Reflection and
specialized evaluation are prior art; neither this observation nor the digits
prototype establishes a new generic compiler or service speedup.

## Memory/core feasibility

The existing 12-cell reservation simulation remains explicitly a model. The
new observed-trace envelope uses each run's own sample timestamps and denominator.

| Total / four cores GiB | Warm trace above threshold | Engine trace above threshold |
|---|---:|---:|
| 8 | 90.41% | 79.11% |
| 16 | 73.10% | 61.31% |
| 32 | 31.36% | 26.89% |
| 48 | 0.369% | 0.408% |

These are left-hold integrations of historical sampled RSS. They are not
throughput at smaller budgets. Changed admission/killing/retries would change
the trace and potentially which terminal results are returned. The actual
48-GiB watchdog is a sampled response, so short overshoots are visible.

The parent-scope audit covers 7,808 prepared child leader high-water reports.
For accepted/rejected attempts, median is 470.6 MB and p99 977.8 MB, versus
3,614.5 MB for the single observed prepared parent's peak. This supports
evaluating shared-parent admission for ordinary work. It does not justify
subtracting independently observed maxima or claiming per-source peak scalars
capture a simultaneous process tree. Descendant and inactive-process scope
remain explicit.

## Environment interruption

After all grid/digits processes retired, the Workspace Pod was replaced.
The new Pod was initially Pending with PVC-not-attached events, subsequently
Running with the same volume attached/healthy on phobos-vt. No M process was
running at replacement; all source and captures remained on PVC.

A new-container short child signal control still returns EACCES and exits
naturally. An in-process Lean alarm test terminated with SIGALRM (-14), not
the C control's intended _exit(124), after about 1.52 s. This qualifies bounded
internal alarm termination for that control, not external signaling and not a
hard deadline on uninterruptible disk I/O. Preserve both actual return codes.
The M line makes no host, security, permission, template or scheduling changes.

## Dependency-probe qualification
The earlier Mathlib control exposed genuinely independent constructor goals and coupled existential metavariables. After Pod replacement, a 90-second broad-import control expired before any candidate rows (exit124); the raw timeout is retained. A narrowed SDK-only control exits0 in103.86s, only0.946CPU s, with both example proofs accepted. Full trace/InfoTree kind sequences differ even on these controls: traces retain speculative and expansion steps absent from InfoTrees. A naive positional join is rejected. Full work/span remains unknown. Unique allGoals nodes with directly matching child counts offer a narrower, explicitly optimistic branch model; this does not establish name/message/cache merge semantics or have/case/first parallelism.
