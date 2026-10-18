# RQ4 common native-submission control — root plan/self-review

RQ4: After preparation reuse, when does heterogeneous execution improve complete verification over the strongest measured CPU path?

## Admission
The current arithmetic collector submits125separate arrays of8 and waits for each complete array. The complete pooled native trace has1241.38seconds of summed task windows and3039.56seconds of task service; only30.61%of8candidate-slot time is occupied. This is notCPUidle or a reclamation metric. An unchanged-duration rolling simulation is only admission evidence and ignores changed contention; it is not executed performance.

The upstream pinned Kimina REPL already implements mode='parrallel',buckets=N: one array is split intoNsequential queues that execute concurrently. This can keep each queue running across candidate completions and remove collector-created wave barriers at the same maximum8active commands, same4CPU eligibility and native root preparation. It is not a new runtime constructor, fork mechanism, parser or novelty claim. A stronger common native baseline could change the earlier GPU interpretation and is the highest-value alternative to another unqualified narrow LP solver variant.

## Comparison and protocol
Role: supporting causal/common-baseline qualification within the existing RQ4 experiment, not another baseline family or tuning grid. Test only the existing wave8 submission versus the source-native8queue interface. Native reference and CPU AST-oracle both use the same protocol in each row. No GPU run is admitted until the native/CPU path engages and native outcome parity passes; any GPU continuation uses the same queue count and4CPU eligibility.

Same original first24sources,original array order,width8,CPU8–11,48GiB,original CPU hybrid and the existing row11/minimum2GPU model. Source-native8queues partition the array into8contiguous subsequences and preserve response-array order. No input reorder, added CPU allowance, memory exemption or custom scheduling interface.

Both modes use a private copy of the same pinned REPL source with one telemetry-only change: the existing candidateTimed wrapper is also applied in the upstream sequential queue path. Native algorithms/cancellation/GC remain unchanged; default binaries and the active full numerical-omission control are not overwritten. Exact source and build logs are retained.

## Completion boundaries and limitations
Wave8 keeps its existing300second per-array observation deadline. The one-array queue control has no added array-wide observation deadline, because that single response now spans the whole cohort; native retained command/heartbeat behavior is unchanged and48GiB still holds. There is no new per-command timeout setting. Consequently this comparison cannot claim equivalent timeout behavior for sources that touch the old array deadline. The selected arithmetic cohort's prior complete runs have no operational timeout and every source verdict/non-message response must still match. Failed or changed sources invalidate a performance comparison, not count as gains.

Run fresh wave8(native,CPUoracle),then native8queues(native,CPUoracle) on the same private timing binary. Capture actual native JSON, task intervals, resources, full EOF/retirement and subprocess failures. Preflight success alone is not a full1,000-source result. A useful matched preflight and complete-cost rationale are required before a fresh full comparison; no concurrency grid is admitted.

Positive: strengthen all methods' common protocol and evaluate genuine GPU batches under that same protocol. Contradictory: keep the prior wave result scope and reject another full run. Inconclusive/fault: preserve evidence and repair only an actual source-native interface fault. This does not close the GPU route or establish a new paper contribution. Whole clocks and top1%/10%source intervals remain primary; no ideal-schedule simulation is substituted for measurement.

Root self-review: real upstream API, same max8candidates/4CPUs/48GiB and shared prepared native root; changed array observation boundary is disclosed. Neither generic batching nor source instrumentation is novelty. No independent reviewer,Agent,OMP or subagent is used.

Record time:2026-10-18UTC. User-authorized scope:「让批量真正形成：在总资源相同的前提下让多个候选并发跑，把同一时刻的 LP 合并成一批送 GPU，并在相同并发度下和强基线、CPU oracle 对比。」Native/CPU preflight is complete; the next finite existingRTX5090target usesall server/clientCPUs8–11 and retains its own UID-checked deletion/otherWorkspace restoration receipt.


## Full CPU/native admission after the real qualification —2026-10-18T08:00UTC
Actual24results are native29.552versus30.483wave seconds; CPUoracle23.476
versus27.223wave seconds,all24same outcomes/native non-message payload.
This admits one full original1000native+CPUoracle comparison through the
same upstream8queueAPI,not a fullnewGPUvariant. The earlier full8item-wave
benchmark is weaker than an available source-native submission protocol.
This comparison is necessary to fix the strongest common baseline before
attributing any further gain toGPU. Unchanged private timingREPL,maximum8
candidates,4eligibleCPUs0–3,48GiB,originalsourceorder/noarrayclientdeadline,
same root preparation,default whole-LP CPUoracle. Profile/answer-omission
processes have actuallyclosed beforelaunch. No freshmatrix/concurrencygrid,
noCPU/GPUclaim from preliminary24results. A complete full response/timing/
retirement record is required; close on all planned2000observations,not on
processhealth. GPU24qualifier's negative result remains negative; it is not
grounds to close theGPUroute. Independent-cancellation24also remains a
separate supporting mechanismqualification until real results justifyfull.
