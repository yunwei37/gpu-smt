# Plan and implementation review — root self-review

RQ4/scientific contract unchanged. The strongest competing explanation is
that CPUHiGHS already cheaply avoids the exact fallback, leaving no extra
GPU benefit; large nativeLP time alone does not refute that explanation.
The same current Kimina/Power frontend and CPUportfolio must therefore be
retained in both conditions, with actual four-CPUeligibility, source2/live2,
24GiB each and aggregate48GiB including device-provider host memory.

Source review: default CPU method keeps native+HiGHS, cutoff11, unchanged
proof route. Only device speculation is gated at38actualFProws. Gating
the entire race at38would wrongly remove HiGHS for small LPs; implementation
instead routes those to retained HiGHS and labels its PID/role correctly.
Large LPs have native, GPU and HiGHS children. Every returned positive or
negative candidate must pass existing exact checks; CPU shadows stay until
a valid winner. The CPU replay uses the same fresh Rust binaries as GPU.
The pre-existing CUDA kernel/provider/library is not numerically tuned.

Parent watchdog sums local ownedRSS plus the exact owned provider's recursive
processRSS; remote PID/startticks identity and four-CPUeligibility are checked.
Sampling uses the existing private provider connection and fails closed on
unknown RSS, with no extra service/policy/container privileges. It kills only
the largest own localREPL when the combined48GiB threshold is exceeded; no
REPL remaining causes the finite group to stop. This is1s sampled response,
not a hard kernelRSSquota. Every external-provider read/sample cost is
charged. The provider is alone before any client/REPL starts; root lifecycle
UID-deletes it after cleanup, including on client failure.

Real CPU24already closed41.456217s native/27.508183s Power,24valid each,max2,
0monitorerrors/kills/noleftovers. These are qualification clocks, not final
1kGPUbenefit. Current GPUcell must actually show source-owned dispatcher
groups/models, CPUretention, outcome parity and zero outstanding device
allocations/complete context retirement. Pending/failed startup has no
performance meaning. Original1000whole/native-rankedtail comparison remains
the decisive matrix. BroaderGPUroute cannot close from a slow variant.
No subagent/OMP/independent review, new scheduler or Workspace is involved.
