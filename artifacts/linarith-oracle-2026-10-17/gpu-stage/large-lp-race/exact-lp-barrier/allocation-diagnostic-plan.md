# Diagnose the actual Barrier allocation failure

Preserve the failed qualification as invalid for healthy GPU performance.
Reproduce one retained195x324LP without a CPU cancellation shadow in the same
pinned finite cuOpt Job/eightworkers/CPU8-11/48GiB. Capture actual VRAM and
worker VmSize/RSS/limits before and after. In the same temporary GPU target,
compare a tiny cudaMalloc and cudaMallocAsync under48GiB and report return
codes. No raised memory limit, solver tolerance, new service or full matrix.
The upstream current sparse_cholesky.cuh associates the observed message with
cudaMallocAsync of n*sizeof(double); this source lookup is a hypothesis,
not proof that the running pinned image contains exactly that revision.
https://github.com/NVIDIA/cuopt/blob/main/cpp/src/barrier/sparse_cholesky.cuh

A reproduced process-limit/allocator problem calls for a compatible allocator
repair under48GiB; VRAM exhaustion calls for removing the excessive worker
override. Retain all failure receipts. No performance inference from errors.
UID-delete the temporary Job and verify lab/otherWorkspace restoration.

Actual tiny allocation:cudaMalloc4096 succeeds,cudaMallocAsync4096 returns2,
freeVRAM20,353,122,304bytes,VmSize14,135,616KiB,RLIMIT_AS48GiB. RetainedLP
replay fails without CPU shadow. Diagnose async allocator compatibility,not
claim physicalVRAMexhaustion or remove48GiB. Root compiled a finite preload
fallback:only async allocation error2 invokes legacy allocation;track those
pointers and synchronize the supplied stream before legacy free. Errors still
propagate. No other limits/tolerances changed;this may serialize work and its
cost is included. Test same tiny allocation and LP before source performance.
The fallback is a temporary benchmark repair,not research novelty or service.

The first runtime-symbol shim fixes only its direct probe,not the static-runtime
cuOptworker. Actual worker maps/environ prove it loaded;unchangedLP stillfails.
Keep that failed repair,do not promote it. The next repair uses CUDA Driver
Entry Point Access (cuGetProcAddress v1/v2 plus loader lookup),since static
runtimes retrieve driver pointers directly. Preserve all nonallocationsymbols,
versions and status;intercept only allocation-error2 and corresponding frees.
Reference: https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/driver-entry-point-access.html
