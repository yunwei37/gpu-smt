# Plan — real32 measured-sibling memory development comparison

RQ3:How does prepared-state branching change end-to-end latency,throughput and
memory at equal resources compared with established warm-session reuse?

This supporting load-layer experiment asks whether existing TaskMemory(Fifo)
reduces redundant preemption/retry sufficiently to outweigh conservative
reservations on real queued heavy/ordinary siblings. It is not prepared-vs-warm
superiority or novelty by itself. Positive result justifies broader method
evaluation;negative/mixed result bounds this policy. No threshold or closure.

Use the existing selected32originals in
artifacts/engine-resource-profile-2026-10-25/task-memory-preflight-20261027.
The fixed outcome-informed selection gives16prioraccepted/7rejected/9resource
failures across four tasks:first8each,restored global order. Prior labels are
not injected into the method. This is development evidence,not unbiased final
population,arrival distribution or hindsight scheduling. No new model fitting,
parameter grid,baseline family or external system reproduction.

Both fresh native REPL conditions use same original Lean4.9rc1/Mathlib,source/
task/timeout/reuse/order,48GiB actualRSS,noAScap,CPU8–11,four one-core leases,
same new frozen releaseCLI. Every policy starts cold;only earlier physical
attempts within its own run teach waiting RSS reservations. Native FIFO first,
then task-memory;all-mode,reuse=false,300s per-attempt unchanged. Only policy
differs. This measures own load-aware admission,not preparation/COW novelty.

Prior fullpair and six original closed-CNF cells have actually retired.
Compile one current release at the free slot,record all build/guard failures,
copy executable outside Cargo target,then smallest real native/core-policy
preflight on original ordinary siblings. Preflight establishes engagement and
native acceptance only;do not infer full32effect. Run both32cells to terminal.
Use existing measure/compare,stdout Capture,stderr resource stream and closed
lossless archival. No new logger,scheduler,control schema or solver.

Report external CLI time plus archival,internal lifecycle,all32uniqueIDs/source,
accepted/status differences,actualattempts,exclusive retries,preemptions,queue
latency/tails,observed RSS kinds/aggregate,all recorded birth retirement. A
resource failure remains operational,not rejection. Lower-bound censored peaks
can underreserve;max sibling peaks can overreserve. Do not treat forecast as
proof of native failure. Monitor1s overshoot is not hard48GiB enforcement.
One fixed-order shared-host devpair cannot establish causal/fullpopulation
gain. Preserve all results,including failure,without final threshold/stop.
Root self-review only;allfourRQs and userdirections remain open.
