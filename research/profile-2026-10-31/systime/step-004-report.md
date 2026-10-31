# M systime004 — complete Grid baseline interim attribution

EXPERIMENT:3plain/3stat/3record/3trace Grid baseline native runs all complete,
accepted, exact diagnostic and84,076,976-byte.olean equality. All records are
retired; no raw binaries or perf.data copied into Git. Stat counters give
user/kernel IPC1.984/0.540medians. Plain53.065%systemCPU is kept separate from
instrumented groups; perf stat increases median systemCPU~33.1%while wall
increases~1.47%, so profiler cost cannot be assumed negligible from wall alone.

Three independently decoded callchain period/sample totals exactly match flat
perf-report native histograms. Resource-accounting paths use74.98%kernel
cycle periods; futex20.42%, page faults0.78%, mapping0.14%.
Two records resolve the caller to stock lean::check_memory,~93%from C++kernel
type checking and~7%IR. Third record reaches libc but not the Lean caller:
that source is unresolved, not zero accounting work. Kernel leaf/path evidence
remains stable across all3. Initial broad-worker operation labels are preserved
but excluded; current kernel classification uses OS call paths, not a generic
task-manager ancestor. Inline RC and48-frame truncation remain limitations.

Trace summaries observe~4.01million getrusage calls and~52million futex calls;
loss counts16749/7348/0 retained. Cumulative syscall elapsed can overlap and
include sleep; it is not kernelCPU. No exact-census or error-bound claim.

WRITE: full Grid median/range counters, native instrumentation overhead,
syscall summaries, user/kernel top20 and runtime operation tables, explicit
callchain-origin examples and scope. Primary Linux/Lean sources contextualize
the mechanism, not replace actual-stack evidence. Root owns docs/paper.

A safely queued priority driver promotes12EXISTING noM/one-worker Grid cells
without touching the active record source/controller; same FLOCK and same
result paths, no added cells. It began only after record3retired. First noM
plain control completed320.612wall/391.521user/107.412system, exact diagnostics
and.olean bytes unchanged; only-M/output path differ. It is exploratory n=1,
not a final3replication gain. Matrix90and other ablations continue.

REVIEW — 自审: no cross-run phase-denominator multiplication, no loss-free
syscall fiction, no .olean-only acceptance surrogate (native compile actually
returns0). No wholesale production or global Lean/GPU claim. New original
baseline/counterfactual kernel measurements qualify only these accepted modules
and current resource point. All raw/failed/partial data and old classifier
preserved on PVC. M paths only; user-approved characterization goal active.
