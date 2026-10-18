# E1065 — retain the strong CPU oracle while adding GPU speculation

Root only,2026-10-18; RQ4, BOOTSTRAP. Correct an experimentally exposed
composition defect, not a new kernel/solver/worker/buffer grid. Previous GPU
conditions replaced the external HiGHS contender with CUDA while retaining only
the native hybrid CPU contender. That is a valid alternative composition, but
does not preserve the strongest measured CPU portfolio when adding GPU work.
Same LP163x435: HiGHS search0.001639s in its fresh CPU record, GPU block lifetime
about9.78s until native-no-certificate cancellation. Actual cross-group overlap
now works, yet repaired GPU43.069316s is slower than CPU37.779115s on original64.

Mechanism: preserve BOTH CPU contenders (native hybrid and external HiGHS with
exact support/negative-ray repair) and add the device contender. Each child
returns a fully exact-checked positive certificate or exact negative evidence;
the coordinator rechecks and selects first valid evidence. Cancel and wait all
losers. Preserve source IDs, input order, Lean checker and native fallback.
Label CPU-HiGHS and GPU winners separately; no crediting CPU work as device gain.
No guarantee of zero overhead: host competition, two proxy lifecycles and GPU
context costs must be charged and can still make this composition slower.

Use private Rust build, reuse unchanged frozen Lean modules/checker and unchanged
VMM/final-drain device implementation. Existing full29,750 tree and common
collector/proxy remain frozen. The extra CPU numeric proxy is a finite process
inside the same requested benchmark, using the existing HiGHS implementation,
same4CPU8–11/48GiB and32maximum candidates; no new persistent service, quota,
scheduler, endpoint exposure or infrastructure setting. Actual GPU groups still
require two ready original LPs; individually cancelled survivors may be single.

First qualify original64 with fresh CPU/native controls at identical width32 and
CPU eligibility. Include proxy start/retirement, every exact check, transport,
fallback, queueing and cleanup. Report GPU group/model/timer engagement, actual
CPU/GPU wins, all source outcomes, non-message fidelity, failed/partial data and
cold lifecycle. No fullGPUadmission unless this real preflight beats CPU oracle
with actual GPU contribution; ordinary CPU restoration is not systems novelty.
Failure of this composition still cannot establish universal GPU impossibility
without an applicable end-to-end opportunity bound. All four RQs retained.
Review is self-review. Existing healthy full/population/prefix captures continue.
