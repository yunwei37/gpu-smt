# Final-drain repair: completed original64 qualification

Root execution/self-review,2026-10-18. Same numerical kernel, actual-size VMM,
original sources, capacity32/equalfourCPUs8–11/48GiB. Only the final model scan
after positive kernel-completion observation changes.

| Same qualification block | Whole pipeline seconds |
|---|---:|
| Native Fast/hybrid |71.640609056|
| CPU two-sided oracle |37.779115328|
| GPU two-sided oracle, repaired final drain |43.069316313|

GPU/CPU=1.140029774, or14.003%more elapsed.
All64nativeverdicts/non-messagefields agree,63complete/1rejected/0operational.
GPUmessage-onlychanges are5;
observerreaderrors=28.
Every source span maps. Cold lifetime is separately retained in the cleanup
receipt. These short sequential observations are not a full-cohort threshold
score, confidence interval or global CPU frontier.

Actual20nonemptygroups/36models,
36device samples,missing=[].
Cross-group overlapping model pairs=29,
peakdistinctgroups=4.
All launch groups retired=True. Final APIprobe
reports0liveallocations/
0livebytes,
peak60817408bytes.
The actual final scan fixes lost-result attribution. GPU executing overlapping
batches still does not beat the CPU oracle here.

Disposition: passed-restored for real functional progress, not performance
admission. No fullGPUmatrix, new pool/buffer/worker or numerical tuning grid
from this candidate. Whole GPU direction remains unresolved under the user's
applicable-bound rule. Continue complete original-workload/component evidence
and select mechanisms from residual cost, not more variants of this kernel.
Existing full29,750 and prefix captures remain untouched.
