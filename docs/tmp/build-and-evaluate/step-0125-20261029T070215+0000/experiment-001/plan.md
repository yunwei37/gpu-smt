# RQ3 dependency repair — source CLI retirement

Scope:only native source backend completion/pipe retirement and regression
fixtures;no resource queue,classification,publicAPI,default timeout,Lean tactic,
prepared-parent behavior or frozen live binary change.

The source backend awaits stdout EOF/child.wait under the request deadline,but
stderr reader completion follows outside that deadline. If a successful leader
leaves stderr held by a child,the resource lease waits for that child. Stdout
inheritance can instead manufacture a timeout after the compiler has exited.
Reproduce through the existing real OSprocess fixture,not another Lean capture.
Three-second fixture children naturally retire even in old failing code.

Add the same regression before production fix. Preserve old failure. Then keep
both pipes draining concurrently and observe kernel exit without reaping the
owned leader,stop its own group while PID/birth remains verifiable,and reap.
Do not add a cleanup deadline,daemon,process scan or new dependency. All source,
diagnostics,exitclassification and charged retirement remain.

OneCPU11support command group is jointly sampled with the birth-matched live
original42controller551646/168353179 at1s. Abort/reap only the new support group
if aggregate exceeds48GiB. Do not restart/alter the actual collection.
Focused regression precedes source/workspace tests,fmt,clippy and CI.
This is necessary engine correctness/throughput dependency,not research gain.
