# Barrier allocator diagnosis and two failed temporary repairs

Actual48GiB tiny-allocation control:cudaMalloc4096 succeeds,async4096 returns2,
with20,353,122,304bytes freeVRAM and about14GiB VmSize. Replaying the retained
195x324LP without any CPU-cancellation shadow still kills the Barrier worker.
This identifies a real async allocation compatibility issue under this setup;
it doesnot prove memorylimit causation independently of the runtime/driver.

The runtime-symbol fallback returns a working legacy pointer for the direct
probe but doesnot affect cuOpt's failing internal call. Actual worker maps and
LD_PRELOAD values prove the library is loaded. A Driver Entry Point Access
interception attempt also has no effect on the actual tiny/worker failures.
Both attempts are rejected as deployment fixes. They were finite benchmark
artifacts only,not installed in the Workspace or a retained service.
No memory ceiling was raised. No device,driver,otherWorkspace or scheduler
configuration changed. All three subsequent temporary Jobs were UID-deleted,
with otherWorkspaceRunning and labReady receipts. The source/raw logs remain.
The output transcription initially copied a stale original-probe buffer after
a Windows file-sharing error;the completed repaired transcript was subsequently
read after its owner ended and overwritten with the actual completed bytes.
No result is derived from that transient transcription.

Do not continue layering loader hooks or claim Barrier normalperformance from
this failure. The existing full CPU comparison continues. Next admitted GPU
mechanism should use proven legacy CUDA allocation and genuinely batched,
independently cancellable device search,keeping exact CPU repair/Lean checks.
GPU opportunity remains unresolved by the complete own-clock profile. Reviews
are by root and not independent. All fourRQs/OSDI novelty remain open.
