# Result self-review — handled CLI termination

Same-thread implementation/review. Evidence index is
[raw lifecycle artifact](../../../../../artifacts/rust-engine-2026-10-25/cli-termination-20261026/README.md).
Actual old idle server exits-15 onSIGTERM,0backend children. This proves the
default signal exit only;old orphan behavior is source-grounded,not measured
by leaking a verifier.

Finalsignal fixtures exercise serve/check/measure SIGTERM and checkSIGINT.
All held fixturePIDs retire before CLI exit;serve drains an HTTPbackend_error
response,while interruptedinput modes exit nonzero. Interrupted measure emits
no complete capture before native completion. Idlecheck/measure exit without
stdinEOF. A first idle-input regression actually fails before runtime fix.

Initial invalid async borrow,targeted-success,fixturePIDreadiness race,
Clippy failure and finalsuccess are all preserved. Atomic readiness rename
removes the fixture race rather than weakening assertions. No live matching
leftover fixture is found at cleanup inspection. No real Lean proof starts.

Final51ordinarytests/0failed/4nativeignored,7CLItests,fmt,Clippy/rustdoc
-Dwarnings pass. Combined development+oldfull sampledpeak14,982,926,336B,
0pressure/monitorerrors,CPU10–11,48GiBbudget. No kernelquota guarantee.

The final scope is resource/process lifecycle only. Existing successfulinput
schemas,verification semantics,resource admission,cache,consumer modes and
requesttimeouts remain unchanged. No newservice/option/supervisor/dependency.
Normalmeasure still captures lifecycle after native retirement. Interrupting
later output can leave a partial record,so users retain exit status.

Original source42659a8fullpair remainsPID408739/birth140695363 with same release
and no completed capture at finalinspection. Physical attempt counts cannot
yield final accepted sets or speedup. Current source is not hotpatched into it.
Allfourdirections,RQs,Mathlib/codeworkloads and OSDIobjective remain incomplete.
