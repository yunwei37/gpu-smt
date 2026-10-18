# Large-LP racing and cross-candidate GPU batches

2026-10-18 UTC. Owning Codex thread executes and self-reviews all work.
The user explicitly requested large-LP CPU/GPU racing and genuine concurrent
batches. This is the next decisive RQ4 heterogeneous-execution mechanism, with matched RQ3 service costs, not a new research direction.

Hypothesis: replacing serial GPU waiting with speculation can exploit GPU LP
parallelism while the original CPU hybrid continues to solve the same LP.
The actual endpoint is complete native verification wall, including native
preparation, packing, RPC, exact support repair, Lean checking, fallback,
cancellation and reaping. GPU failure alone cannot suppress a valid CPU result.

For large LPs, dispatch the existing pinned CPU hybrid and the GPU hint/repair
path as two cancellable child processes **before either LP search**. A GPU child
returns only an exactly repaired and verified coefficient certificate. The
parent re-verifies coefficients, selects the first valid certificate (or the
CPU exact no-certificate answer), terminates and waits for the loser. Parent
death terminates children. This uses no detached solver thread or persistent
worker. Small direct hints may still decline to the unchanged Lean fallback.

The prototype uses two simultaneously live device-ready LPs as the GPU batch
minimum. Partial batches wait without an arbitrary timer; their CPU shadows
keep running, so a singleton can finish on CPU. Owner cancellation wakes the
queue. Ready LPs are merged block-diagonally and retain phase-I PDLP/crossover
as in the recorded prior implementation. This is a deliberate batching policy
whose queue cost and missed singleton opportunities are included, not a claim
of universal optimal scheduling.

Qualification freezes width8 and CPU0–3 for native, original CPU oracle,
CPU-only same-large-LP mechanism ablation and GPU racing. The cuOpt server is
also confined to CPU0–3 in the existing finite RTX5090 Job; this is shared CPU
eligibility, not additional cores or exclusive reservations. All captures keep
48 GiB and default300 s native request/finalization. There is no numerical warmup.
No other Workspace is stopped or changed.

For qualification only, minimum rows37 is median36+1 from the corrected-family
24-source native profile. It is provisional, not the final full-population
median. The complete original1,000-source profile will supply its row split,
LP wall share and applicable optimistic bound; do not extrapolate this small
qualification's distribution to all1,000 sources.

Compare against the fastest valid matched CPU/native result. Qualification
must retain all24 source verdicts with no non-message differences. It must
show actual jointly submitted live GPU requests, not just a width argument or
a synthetic replay. Admission to a full paired original1,000-source comparison
requires an executable parity-qualified path and a paper-relevant opportunity
under the corrected profile. A failed qualification bounds this version; it
does not close the GPU route unless the user's ceiling criterion is met.

One earlier CPU-only fallback-race staging version was checked on24 sources
before moving race dispatch ahead of the entire LP search. Its raw results
and source/binaries are retained separately. It is not pooled with the new
version or presented as GPU evidence.

Self-review: ordinary racing alone is not a novelty claim; the experiment
decides performance feasibility. CPU/GPU contention and cancellation can
make racing slower, so no 'never slower' guarantee is assumed. The final1.5x
criterion applies to the better valid CPU/GPU result. No independent review
has occurred, and no OSDI acceptance claim is made.

## Native protocol reuse after first completed qualification

The first real GPU run formed five size2 batches with matching outcomes, but
per-query spawn from the large Lean process incurred about10--11 s of child
system CPU. Replace only that integration with an idle-list of independent
existing daemon handles. Borrow/return holds a mutex briefly; all solving and
line I/O occur outside it. There is no global solver mutex, extra thread pool,
fixed daemon cap or persistent external service. Idle handles exist only for
this native REPL and close on its process exit. Failed handles are killed and
waited, not returned. CPU-only and GPU variants share these exact Lean modules.

Use a separate pooled build root; preserve all first-version code/raw results.
Repeat real24-source CPU/GPU qualification at the same width8,CPU0--3,48GiB,
row eligibility37 and GPU minimum2. The proxy now joins the GPU dispatcher after
cancelling abandoned work, so WaitForCompletion and result deletion finish
before cell retirement. First-version all5 jobs already had result records
before retirement; this repair addresses future in-flight cancellation cases.
