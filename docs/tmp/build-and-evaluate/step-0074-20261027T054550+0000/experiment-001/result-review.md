# Result self-review — existing CLI exposes TaskMemory

One new opt-in task-memory choice composes TaskMemory::new(Fifo) in the existing
common check/measure/serve policy selector. Default remains FIFO;task-interleave
and source-size are unchanged. Native input/resources/consumer modes,typed
requests and Capture schema are unchanged. Capture.policy labels the method.
No new collector/logger/service or policy parameter grid is introduced.

The extended existing executable test fails before implementation at unknown
scheduling policy. After selection is wired,it captures two same-task distinct
sources,one physical fixture attempt each,retired processes,correct policy
label and identity comparison. The fixture is Python,not Lean. Earlier81fe7cc
nativeCI qualifies TaskMemory library controls;it is not proof of full original
workload throughput or of this executable transport's native performance.

Green:7CLI tests,5HTTP tests and5measurement tests pass. Server library has
0tests,not added to the passing count. Workspace all-target check,Clippy
-Dwarnings and formatting pass. Other packages' runtime tests are not rerun.
Red/green commands,raw logs,lossless gzip source/outputs and support memory
samples are retained. No native candidate executes locally in these tests.

CPU11/oneCargo job support monitoring sums the active own capture tree with
the support tree every1s. Red peak15,541,481,472B;green15,129,923,584B versus
51,539,607,552B budget. No monitor error or support abort. Sampling is not a
hard guarantee,and shared CPU overlap remains a fullpair timing confound.
The running group uses its frozen copied executable;it is never rebuilt or
reconfigured by these debug tests.

Public guide now gives a matched FIFO/task-memory recipe using unchanged
native input/source/task IDs/timeouts/mode/reuse/backend/resources and cold
policy history. Native testing waits until the current sole group actually
retires. Heterogeneous sibling overreservation,censored memory peaks,growing
history,operational outcomes and complete clocks remain explicit. This is
engineering readiness,not an acceleration result or novelty. Root self-review.
