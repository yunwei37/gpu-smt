# Plan — native differential qualification of task memory feedback

Supporting resource/workload node after99709ec. Keep the sole frozen4.9
full pair running unchanged. Use the existing official4.18/REPL native CI,
not another local Lean collection or new workflow/service. Extend the existing
raw-native accepted/rejected/sorry test with opt-in TaskMemory composition.

The actual backend must publish positive retired-attempt observed memory,
and same-task subsequent reservations must reflect its maximum. Context is
opaque and captured by a test-local inner policy; do not duplicate its encoding.
Check different task/timeout/context isolation and exact native response/status,
including an accepted sibling after a rejected one. Native process retirement
and noncached execution remain explicit. No synthetic RSS as native evidence.

Compile/Clippy/format locally onCPU11 under existing combined own-tree48GiB
support monitoring. Native tests remain ignored locally while capture runs.
Push source and pending evidence,let the existing CI execute actual native
tests,then retain bounded run/job conclusion and relevant log evidence on
completion. Do not call a commit/green compile a completed native qualification.
No throughput/fullMathlib/novelty claim. Root self-review only.
