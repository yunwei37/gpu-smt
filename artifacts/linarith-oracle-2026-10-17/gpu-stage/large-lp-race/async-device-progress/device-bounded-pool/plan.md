# One allocator-compatibility repair, unchanged48GiB

The first independent-stream candidate returned31OOMbuildreplies and executed
zero kernels. The installed CUDA12.8 API exposes cudaMemPoolProps.maxSize:
0 uses a system-dependent maximum. Test exactly one repair: an internal
device-local stream-ordered pool whose maximum is the GPU total physical
memory discovered by cudaMemGetInfo. This is not a guessed/per-experiment
buffer size, quota, resource reservation or a cluster setting. Both Workspaces
keep sharing5090; processRLIMIT_AS remains48GiB. No release/reuse-policy tuning.

All failures label the specific CUDA pool/allocation operation. Expose the
discovered maximum and successful pool retirement in the provider log.
Keep the same independent-group numerical code, LP eligibility, same first64,
width32/equalCPUs8–11, CPU race, exact checking, allstartup/fallback/retirement
and cold lifecycle. No hidden numerical/context warmup. Failed default source
and raw result remain immutable in the parent artifact. Existing working
legacy backend and CPU captures remain untouched.

This is a dependency repair within the previously admitted GPU experiment,
not a new paper-value experiment or a parameter grid. Actual kernels and
cross-group device timing must engage; mere native result parity is insufficient.
If it still fails under48GiB, retain the exact failure and do not enlarge the
limit or launch a full matrix. If it works, the same64source end-to-end result
must beat the strong CPU competitor before anyfullGPUadmission.

Primary API: https://docs.nvidia.com/cuda/archive/12.8.0/pdf/CUDA_Runtime_API.pdf
cudaMemPoolProps.maxSize and cudaMallocFromPoolAsync. No novelty claim.
Root sole execution and self-review.
