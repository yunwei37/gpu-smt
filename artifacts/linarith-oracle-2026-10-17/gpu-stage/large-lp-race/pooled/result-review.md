# Pooled native protocol qualification

2026-10-18 UTC. Owning-thread implementation/execution/self-review.

The idle-list of independent existing native daemon handles removes per-query
process creation from Lean. CPU-only wall is 21.122033613 s
and GPU race wall is 21.548805284 s. Both return24 complete,
zero operational failures, no source-verdict or non-message differences.
Prior width8 native31.486097491 s and original oracle22.051807059 s remain
separate frozen controls. These are qualification values, not full1000 results.

Waited-child system CPU falls to 1.763566 s
for CPU-only and 1.828193 s for GPU,
versus about10--11 s in the per-query-spawn integration. No cost was subtracted.
The matching runtime/source snapshots and raw records are retained.

There are 58 actual large-LP races, with winner counts
{'cpu-no-certificate': 8, 'cpu': 49, 'gpu': 1}. Submitted GPU batch sizes are {2: 4}.
The dispatcher retirement record explicitly follows cancellation, completion
and result deletion, before cell retirement. Client/server CPU0--3, width8,
48 GiB and minimum37 rows remain unchanged; the GPU server has been deleted.

These records prove simultaneous LP batching. They do not yet attach original
source identity to GPU batch membership, so the precise cross-candidate versus
cross-goal split remains unknown. Source/call labels are required on the full
experiment before that attribution is claimed.

The GPU route remains open. Its complete corrected-family phase profile is
still collecting; no full-population ceiling or final best-CPU/GPU threshold
decision is reported here. There is no independent audit.
