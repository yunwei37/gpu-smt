# Original42 resource failures — corrected native-library solo point

Actually started2026-10-29T05:35:59UTC,after the full7808warm/engine pair
terminated and its root review/raw results were published at269ded9.
Only this finite collection is running. No result or recovery count is known.

Use the unchanged42one-candidate all-mode requests,300000ms,reuse=false,
ordinary native Mathlib,engine13d4606,noCOWparent. All source/id/deadline/reuse
fields byte-match the original full7808inputs. The historical prepared input
omits task_id,which the full7808record contains. No task-aware policy,
first-success grouping or result reuse is active,so it is preserved rather
than silently rewritten. An initial whole-object check caught this metadata
difference before any native launch;all original source bytes were equal.

CPUs8–11,one four-core lease,48GiB summed sampled owned RSS,no fixed process
AS cap. One original source executes at a time and is reaped before the next.
This four-core eligibility point is separate from the fullengine's one-core
leases and historical24GiB-AS/no-explicit-library results. No CPU/GPUoracle,
counterexample wrapper,ranking or diagnostic instrumentation is enabled.

[Actual launch](launch.json) records engine551647/birth168353182 and
[finite wait capture](controller-launch.json)551646/birth168353179.
The existing native CLI check interface accepts one Batch per line;the
finite script adds only launch/exit/retirement capture,no service or policy queue.
It never launches a following experiment or resumes an AI session.

[Actual first native engagement](native-library-readiness.json) observes
source579REPL551653/birth168353184,ordinary library in /proc maps,unlimited
address-space limits,CPUs8–11and one native thread. A four-core lease does not
prove four cores of useful execution. Host MemAvailable at launch was
116298784kB;no Workspace quota,host policy or other workload changed.

The live directory is /tmp/gpu-smt-solo42-native-library-20261028.
Wait for its own actual terminal/exit,then retain stdout/stderr and every failed
or partial row with memory/CPU evidence. Do not report old41failure/1timeout
or full-pair retrospective subset outcomes as this point's result.
