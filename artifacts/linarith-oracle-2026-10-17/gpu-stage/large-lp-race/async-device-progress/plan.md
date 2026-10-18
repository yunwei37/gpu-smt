# Independent GPU batch progress, not another numerical tuning grid

Admission evidence: the completed capacity32 trial has median0.561s/max8.914s
proxy dispatch wait, actual4.15/8.78s group head-of-line tails, but only
0.012s median dispatch/provider handoff. Both proxy and provider wait for
entire group retirement before accepting the next ready group. Individual
result/cancel messages therefore do not provide independent group progress.

Mechanism: keep unchanged row11 eligibility, minimum2 simultaneously ready
different-source requests, same two-sided numerical algorithm and exact CPU
shadow/repair/Lean checks. Let groups dispatch and own independent nonblocking
CUDA streams. Use stream-ordered device allocation/copies instead of adding
threads around globally synchronizing allocation. State/cancellation uses
per-model I/O streams, no per-model pinned-memory allocation or mapped output
registration between active kernels. Keep default CUDA allocation policies.
No numerical tolerance or parameter tuning, no artificial duplication,
no precomputed answers or free warmup. Temporary source snapshots are permanent
experiment provenance, not a replacement checkout. Build in the owning WS.

First qualify actual5090under48GiB with the original first64 cohort,
capacity32/equalCPUs8–11 against the already-closed matching native/CPU cells.
Require actual overlapping kernel groups, exact source/native verdict/non-message
parity, correct individual cancellation and every kernel/model/context retired.
Retain allocation/runtime failures. If defaults cannot operate within48GiB,
record that result, do not enlarge the limit. No fullGPUmatrix unless a real
end-to-end preflight beats the strong CPU competitor. Frozen reversedCPU
capture/binaries/harness onCPU0–3 and protected prefix are untouched.

Primary API semantics: NVIDIA stream-ordered allocator documentation
https://docs.nvidia.com/cuda/archive/13.1.0/cuda-programming-guide/04-special-topics/stream-ordered-memory-allocation.html
describes ordering allocation/copy/kernel/free without costly global allocator
synchronization. This is established CUDA functionality, not a novelty claim.
All work and review are root-thread execution/self-review.
