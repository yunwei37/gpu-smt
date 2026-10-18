# Source-labelled batching and member cancellation: functional check only

2026-10-18 UTC. Root execution/self-review.

All24 native outcomes agree; no source-verdict or non-message changes.
All58 large-LP races now carry original source/call identities. Seven actual
two-request GPU submissions each contain **two distinct original candidates**,
verified against the retained1,000-source input. Request IDs, source indices,
proof IDs and LP dimensions are recorded in functional-summary.json.

cuOpt has whole-job cancellation. To stop GPU work for a withdrawn LP, the
proxy now cancels the joint job as soon as any member's CPU shadow wins.
After the cancelled job retires, surviving clients are requeued; their CPU
shadows continue throughout. The check exercises7 cancellation/requeue events
and a final dispatcher join with zero pending jobs. All58 winners in this
functional run are CPU (50 certificate,8 no-certificate). Rebatching/wasted
GPU work is retained and charged by the actual lifecycle, not assumed free.

This was mistakenly overlapped with our new width8 native pilot on CPU0--3.
Consequently **neither this run nor that pilot is a primary performance result**.
The overlapping lifecycle is04:51:18.989--04:51:59.521Z. Only source attribution,
outcome parity and cancellation behavior are qualified here. The pilot was
cancelled through its existing async cleanup; all four verified owned PIDs
retired. Its partial raw files are preserved in contended-native-partial.
A fresh same-config native full reference starts04:53:38Z, after the GPU Job
was deleted. The original CPU12--15 series, phase capture4--7 and prefix20--23
remain on their existing lifecycles. No other Workspace was stopped or changed.

The earlier unlabelled performance-qualified24-source pooled timing remains
21.122033613 s CPU and21.548805284 s GPU, with its own raw capture. It is not
replaced with this contended check or pooled into a speedup. No GPU route
closure or full-population result follows from these qualification captures.
