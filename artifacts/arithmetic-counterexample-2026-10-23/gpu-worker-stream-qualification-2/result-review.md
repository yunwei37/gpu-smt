# Actual worker-stream / RTX5090 qualification — root self-review

Executed2026-10-24UTC, after main24153ff with the working source changes
recorded in this step. This is an integrated dependency qualification for the
approved own native/GPU comparison, not an independent paper experiment,
complete proof run, accepted-set parity result or acceleration result.

## Why this execution was needed

The prior474entry qualification supplied one prepacked RPC batch. It did not
execute the persistent native-facing worker's individual request/response
framing, host recheck, closed-goal dispatch, small ready-batch formation or
worker exit. This run reuses that exact retained real-goal input and reference
witnesses through two persistent ordinary Python workers. No new verification
REPL is created. These workers are program subprocesses, not AI Agents.

Command from the sole infrastructure checkout: load the owning Workspace's
bench/lean-counterexample/device-lifecycle.ps1 and invoke -Phase points
-WorkerStream -SourcePod coder-81668d0b-bcba-4058-a2e6-473350357c52-9dc6df5ff-wzmfb
-Out /workspaces/repository/artifacts/arithmetic-counterexample-2026-10-23/gpu-worker-stream-qualification-2.
The existing finite Job/image/RTX5090 path is unchanged; the source Pod and
GPU Pod must share lab and CPU eligibility8–11. No external method is run.

## Raw evidence and result

- [Executed client](qualifier-executed.py), [executed worker](source/worker.py).
- [Worker input/answers](worker-goals.jsonl.gz), [normalized response](response.json.gz),
  [per-entry checks](checked.jsonl.gz), [worker exits](worker-exits.json).
- [Summary/memory](summary.json), [RSS samples](memory-rss.jsonl.gz).
- [Provider batch/device/retirement log](provider.log.gz),
  [exact finite Job](job.json), [lifecycle](lifecycle.json).

All474source/entry-owned replies return.84fullysupported closed goals are
evaluated once on CPU;390nonclosed requests traverse the actualRTX5090
provider. Two exact witnesses match the existing reference;0missing/additional
witnesses,0invalid returned points and0provider errors. Both worker processes
exit0. This checks the interface only: the hook inside Lean, native alias
semantics and complete candidate outcomes remain unexecuted here.

Actual provider logs contain381GPU batches:372singletons and9pairs.
Seven batches contain two distinct sourceIDs; two pairs have a single sourceID.
These are two offline worker streams replaying retained goal records, not
evidence of simultaneous native proof candidates or useful online batching.
Do not transfer these batch statistics to the pending native/full run.

The observed worker-stream interval is1.146360831s, qualification wrapper
1.151394057s. Full finite cold lifecycle27.9238408s decomposes into
9.0845371s API startup,3.41672s remote-client wrapper and15.4206483s retirement.
CUDAfirstinitialization364.610353ms is inside the monitored request interval.
These are functional diagnostic clocks, not a speed comparison with the earlier
one-batch run or native proof checking. Shared batch times are not summed across
individual replies.

## Memory, cleanup and original capture

The existing one-second watchdog includes this local tree, the exact retained
original observation PID255332/birth124305929 and the provider's owned RSS.
Two samples see peak21,584,822,272bytes/max2actual nativeREPLs,0kills/errors,
peak sampled external provider172,883,968bytes. Budget remains48GiB aggregate
and24GiB per REPL. Two samples are not a full cold-lifecycle peak or kernel
hardRSS enforcement.

CUDAcontext closes; provider exits0; the exactUID Job is deleted and Pod
absence verified; cleanupErrors is empty. The original full observation stays
on its frozen code. The short joint qualification window is retained as
coexecution, so its observer request timings are not called an isolated
performance baseline. No secondfullcapture, Agent or Workspace is started.

## First failed attempt and bounded repair

[Attempt1](../gpu-worker-stream-qualification-1/) is preserved, including raw
memory, provider, lifecycle and PID/command ownership evidence. A newly added
client line emitted literal backslash-n rather than a newline. Both workers
waited for a complete request. Only that exact qualification tree was stopped;
client exit143, no provider batch/CUDAinitialization, provider exit0 and
complete ownedJob cleanup are recorded. The failing client source is explicitly
labelled reconstructed from the exact two-line escape correction, rather than
claimed captured before execution. No device or performance result is taken
from that attempt.

The framing is corrected before attempt2. Its actual executed client is
copied directly into this directory. This is an execution repair inside the
same qualification, not an extra research claim or new experiment matrix.
The native exporter/active observer are unchanged.

## Result review and return

Run status: valid functional qualification after one preserved failed attempt.
Tested scientific hypothesis: inconclusive; no complete verification pair.
Research value: dependency-only, zero independent RQ contribution.
Paper impact: no result value, novelty claim or RQ answer changes.
Root self-review checks all474worker records/ownership, reference witnesses,
actualdevice/batch rows, worker exits, jointmonitor and exact cleanup receipt.
This is not an independent audit.

Return to the already-approved sequence: actual original7808observation
termination/collection, native24off/on qualification, then the complete
same-candidate native/GPU pair. Do not repeat point-only qualifications,
tune parameters or claim proof acceptance/performance from this check.

Closed raw JSON/JSONL streams are losslessly gzipped after process/provider retirement; byte-for-byte decompression was verified before removing the uncompressed copies. No active census file is archived or removed.
