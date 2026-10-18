# Independent-group candidate rejected — root self-review

The root thread implemented independent dispatch/provider group owners,
nonblocking CUDA streams, stream-ordered allocation/copies and per-model
control I/O. The numerical phase-I operations and CPU exact authority stay
unchanged; kernel entry/exit globaltimer probes were added to verify actual
cross-group device overlap, not infer it from host threads. The source builds
successfully with the retained CUDA12.8/sm120 toolchain and has syntax-checked
Python entrypoints. No running CPU implementation/binary/harness was mutated.

The first launch failed before collection because the artifact entrypoint
omitted its own path binding. Exact failed source/lifecycle records are
retained; its Job was deleted and other Workspace/lab remained healthy.
After fixing and verifying the whole runner's --help, the real first64-source
qualification runs with 32 candidate queues, CPU8–11 and the required48GiB.

**This candidate did not execute a GPU kernel.** It returns31build_failed/
out-of-memory replies,21zero-model launch records, zero device intervals.
Actual method wall including proxy setup/retirement is65.444552122s, but that
clock is a failed-allocation/fallback pipeline, not evidence of asynchronous
GPU compute performance. All64verdicts/non-message native fields still agree
(63complete/1rejected/0operational), with5message-only differences.
Memory observer has24read errors; no peak or resource efficiency claim.

Stream-ordered allocation defaults failed under the mandatory
51,539,607,552byte address-space ceiling. The source currently reports the
generic allocation error; it does not isolate which runtime allocation/
reservation consumes the space or establish physical VRAM exhaustion.
Do not assert a CUDA driver defect, resource-policy restriction or physical
GPU OOM from this generic message. The48GiB ceiling is unchanged.
Actual asynchronous memory compatibility and cross-kernel progress remain
unqualified. Do not promote this source into the working backend or launch
a full matrix. The old legacy-allocation backend remains intact.

Lifecycle95.3238069s includes9.6517244s to Pod readiness and18.1340208s
retirement/restoration. Job8ad5cccb-1d19-4c96-8ee4-bb084011698a was deleted;
otherWorkspaceRunning andlabReady. No retained service, replacementWorkspace,
scheduler or Agent was created. The candidate's complete failures and raw
responses are losslessly retained; a proxy/candidate success status alone is
not a GPU execution pass. The after-run /proc receipt has no live proxy
because collection was already over; it is not identity evidence during
execution.

This closes only this stream-ordered candidate's admission. The measured
head-of-line dependency remains real, but its removal still needs a
48GiB-compatible implementation and actual device-overlap proof. The
GPU route is not globally closed. Frozen reversedCPU replication and prefix
collection continue; their results take priority over speculative allocator,
buffer or thread-tuning grids. No fullGPUmatrix is justified by this failure.

PTX globaltimer is a target-specific NVIDIA tools register, not a portable
timing contract. No timer samples were produced in this failed qualification.
Primary register semantics:
https://docs.nvidia.com/cuda/pdf/ptx_isa_9.0.pdf (special registers section).
Review and implementation are root self-work only, not independent audit.
