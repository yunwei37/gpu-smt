# Device-batched LP support search with independent cancellation

Root sole executor/self-review. This addresses the original arithmetic/GPU RQ:
can useful cross-candidate numerical search improve complete Lean verification
over the strongest native and CPU oracle interfaces? FourRQs and novelty remain.

The full current-family diagnostic cannot exclude1.5x:LP/product intervals
occupy75.53%of oracleelapsed,with substantial exact-LP overlap. Existing
cuOptjoint jobs have actual batching but cancellation discards siblings and
kills/restarts workers. Independent cuOpt jobs isolate cancellation but pay
per-job/context overhead;the accurate Barrier implementation actually fails
its async allocator under the preserved48GiB setup. Two loader repairs failed.
Do not repeat solver flag grids or infer healthy-performance impossibility.

Implement one persistent GPU provider using ordinary cudaMalloc,whose tiny
allocation works under48GiB. Use standard dense phase-I primal simplex with
Bland entering/tie rules in one cooperative thread block per LP. A single
launch may contain multiple simultaneously ready real LPs. Each LP has its own
mapped cancellation/completion state and hint vector;CPU completion withdraws
only that LP,without destroying a CUDA context or discarding sibling progress.
The floating search is not trusted. Unchanged CPU support repair and Lean proof
certificate checking remain the only acceptance path. A numerical failure
returns no hint and the CPU exact shadow/native fallback continues. No new
iteration/time budget;CPU cancellation bounds speculative work by the actual
native attempt. Device allocation/free/synchronization/preparation/network/
packing/proxy/queue/retirement belong to the measured GPU path.

Reuse the existing FP-first dispatch:cheap CPUfloating search first,only row11
or larger FP-failed LPs speculate. Max8candidate tasks,eight native contiguous
queues,four CPU eligibility0-3(or8-11for qualification),48GiB,zero cores,
same source bodies/imports/heartbeats. The same finite Job identity and RTX5090
device-plugin path carries this temporary measured provider. No new service,
Workspace,controller,scheduler,driver or persistent runtime configuration.

First qualify on the retained LP-heavy10 sources against the actual native/
CPU/HiGHS controls. Also compare every returned hint with exact repair and
native verdicts;preserve no-certificate/failed attempts. Verify actual batched
launch sizes,distinctsourceownership,independent cancellation,all-model/
kernel/context retirement and full cold lifecycle. Single launches are not
called multi-LP batches. Exact thresholds are numerical implementation details,
not proof trust or configurable tuning grids.

Only beneficial complete-cost qualification admits one fresh matched full1000
native/CPU strongest/GPU comparison. A negative variant bounds this implementation;
the overallGPUdecision still follows the applicable bound/user criterion.
CPU HiGHS may independently improve the full cohort but is prior-art baseline,
not a novel systems contribution. The selected10 diagnostic is inspected and
not final/repeated evidence. This implementation tests a different mechanism
from per-job cuOpt launching,rather than another narrowkernel proxy.

## Observed numerical algorithm repair
The first real five-batch preflight reaches up to16,745Bland pivots beforeCPU
cancellation and three numerical declines,while CPUHiGHS is18.13s vsGPU37.98s.
Before any full run,apply standard row/column infinity-norm equilibration and
largest-negative-reduced-cost pricing (lowest-index ties),then unscale hints.
This changes the floating numerical search,not native acceptance. It directly
addresses observed degeneracy/conditioning;no tolerance/iteration/time grid
or additional workload selection is admitted. CPU cancellation remains the
termination boundary for a cycling numerical attempt. Retain original source
and results separately,and rerun the same selected10only once for this repair.
