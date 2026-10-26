# New dynamic-resource7808 run — native complete,prepared ENOSPC partial

Actual source42659a8,both cells use original7808/all/no-reuse/300s,CPU8–11,
four1core leases,48GiB sampled actual RSS/no fixed AS. This record is not a
completed native/prepared pair. Native terminal is complete;prepared exits
during verification with ENOSPC,no terminal and0byte capture. All failed/
partial bytes remain;no fullpair speedup or prepared accepted-set claim.

[Closed native analysis](native-analysis/summary.json) validates exact complete
canonical Batch equality/order/7808unique finalresults/no cache or coalescing.
Counts:3013accepted/4665rejected/87timeout/41resource_exhausted/2backend_error.
Native lifecycle28464.813475s;external cell28466.132239s includes input through
shutdown/capture compression/compressor retirement,not whole controller cold
startup. No comparison to another resource point's wall clock is valid.

Compared only by status to historical2worker/24GiB-AS baseline:
3013of3014old acceptances remain;minif2f-3086was accepted with277.657785s reported
body,now times out after300.246640s attempt. No new accepted IDs.
Other changes:old42resource failures become41resource failures/1timeout;
2old rejected become native backend errors and2old rejected time out.
These resource/frontend/shared-host effects have not been causally isolated.
No transparent accepted-set equivalence is claimed.

There are44retried sources,44preempted first attempts and41exclusive total-
budget failures:85watchdog events. Physical journal says85cancelled outcomes;
engine finalclassification/retry history is authoritative. Peak of all monitor
admission/watchdog observations52,386,656,256B=48.788876GiB,847,048,704B above
configured budget. The1s sampled response is not a hardRSSquota. The thinned
retained JSONL maximum is52,220,346,368B;33of20866retained samples exceed48GiB.
Do not force the two sampling scopes to have the same maximum.
Max registered leaders4is not proof of4busycores. Attempt journal errors0;
no monitor/no-global-OOM conclusion is inferred from that field.

Native EOF faults2325/3209retain deep native simplex stacks in64KiB tails,
not a diagnosed exact crash cause. Their native-owned PIDs416819/425060 match
the newly generated retained core dumps. Core443290is from the prepared leg.
No frozenCPUoracle optimization or native-stack tuning is applied.

## Actual storage failure and repair

At09:33:55UTC driver reports No space left on device. Prepared physical journal
has2408complete attempt rows;RSS JSONL2226complete rows plus partial line2227.
Physical attempt rows are not finalconsumer outcomes. Driver exit code was not
recovered;it is unknown,not0or a guessed1. All registered native births and
declared REPL/host processes were retired at observation. Driver log/raw partial
files remain,with lossless gzip copies;empty capture stays visibly empty.

Workspace volume had0free;host/tmp filesystem had ~340GBfree. Thus removing
/tmp Rust buildcache would not repair this PVC. Reclaimed only17,814re-downloadable
Mathlib.ltar cache files after byte-exact copy to/tmp;no compiled modules changed.
Losslessly gzip-archived3closed failed-run core dumps,verified full decompressed
byte equality and retained both persistent archives and/tmp copies. Source/data/
runtime binaries/config/quotas/otherWorkspaces unchanged.
[Repair receipts](enospc-recovery/cache-reclamation.json),
[core archives/restore paths](enospc-recovery/core-archival.json).
Observed free afterrepair1,961,963,520B. Core contents were preserved,not discarded.
This is cache recovery/archival,not a persistent storage-capacity fix.

Complete native capture,terminal,compressed attempt/RSS originals,partial
prepared files and observed-failure.json are committed. Uncompressed source
journals are retained in the owning Workspace. No healthy capture was stopped;
this one had already failed. Next user sequence is42isolated retries,then71
timeout prototypes,then lean-mlir. Completing a valid prepared population
comparison remains outstanding,not silently waived or synthetically resumed.
All review is same-thread self-review.
