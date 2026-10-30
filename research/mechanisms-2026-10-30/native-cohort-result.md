# Fixed200 C-timing result: observed parity, little atomic-branch headroom

2026-10-30UTC;M;self-review. Six actual native processes,600/600 returns,
all exit0 and retired. Captures and frozen source/runner copies remain on
PVC outside Git; local CSV/JSON retain all200 candidate comparisons.

## Differential and observer cost

|Comparator vs stock|Same error flag|Same diagnostics|Same InfoTree|Different raw allocation-HB|
|---|---:|---:|---:|---:|
|Version-matched relink,callback off|200/200|200/200|200/200|63/200|
|Version-matched relink,C callback on|200/200|200/200|200/200|62/200|

Classifications in all cells:31 no-error,19 ordinary Lean errors,150
diagnostic-budget interruptions. These are InfoTree-enabled frontend flags,
not the production accepted/sorry policy. Strict heartbeat equality is not
established despite observed decision/diagnostic equality. C callback code
does not allocate Lean objects,but this does not prove complete replay or
budget semantics. The relink and shared runtime expose the same68613 Lean
C symbols; the relink has only4 additional measurement FFI exports. Symbol
surface equality is not bit identity or per-call dispatch proof.

Own body CPU totals:stock827.301816s,off839.965435s,on838.669501s. Own body
wall:827.525068s,840.188200s,838.914357s. Whole-process wall sums:stock
1023.378439s,off1029.925766s,on1028.648512s. Import,collector,InfoTree
serialization and flushing costs remain charged in whole-process receipts;
body-only values are not end-to-end service speedups. One ordered pass with
reversed cell order in the other disjoint shard does not identify causal
instrumentation overhead or runtime variance. No negative/free tracing-cost
claim from on being slightly faster than off.

Maximum1s sampled own-tree RSS8,659,439,616bytes (~8.06GiB),below M16GiB.
This is sampled RSS,not a hard RSS quota. No external signals sent. Each
native cell finishes within its1500s internal bound; complete matrix is a
serial set of finite cells,not a new persistent service.

## Work/span evidence at the stated diagnostic point

On-cell body CPU838.669501s; exclusive eqRefl CPU781.383626s (~93.17%).
Other exclusive leaders:simp11.037798s,nlinarith8.813244s,simpAll7.399740s,
normNum4.984502s,linarith4.790941s. C trees are complete for all200 sources.

The sum over candidates of each candidate's largest indivisible C leaf is
812.899512s. Therefore,under unchanged recorded work and leaf-call granularity,
aggregate W/sum(span) cannot exceed838.669501/812.899512=1.031701x. This
optimistic bound ignores dependencies between different leaf calls; adding
such dependencies cannot create headroom. It does not cover splitting a
closed computation inside eqRefl,changing algorithms,early termination or
removing work. It is not a measured parallel execution or a complete DAG.

The ancestry-qualified allGoals model finds one multi-goal split and saves
0.015943s,ratio1.000019x. It leaves unsupported constructs serial and does
not establish safe merging of names,messages,caches or hidden state. Independent
have/case/first counts are not promoted into runnable jobs. Full merge-safe
critical path and complete DAG average remain unknown.

Important population limit:minif2f-4544 spends721.618421s body CPU here,with
one720.249942s eqRefl leaf. The retained historical service stops that request
at300s. Diagnostic maxHeartbeats3000 is not a per-request300s wall deadline.
Consequently neither the93.17% share nor1.031701x bound can be applied to the
original7808 service denominator. Other diagnostic limits and allocation
settings also differ. No cross-run rescaling or global Amdahl claim.

## Mechanism assessment

This diagnostic sample does not support investing in coarse independent
branch speculation as the main speedup: even a dependency-free fixed-leaf
model has little headroom. General production feasibility remains unmeasured
under matched deadlines. Closed-computation representation/checking remains
a different direction; the prior digits certificate is actual small evidence,
not a general extraction engine. Software PC sampling proceeds after retirement
to distinguish runtime/interpreter/kernel residence without PMU.
