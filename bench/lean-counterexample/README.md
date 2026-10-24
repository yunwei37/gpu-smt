# Arithmetic counterexample screening

This is our own experimental method. GPU values only propose counterexamples;
CPU exact checking is mandatory, and the native verifier still accepts proofs.

## Current evidence

The native hook's off/observation qualification preserves all 28 complete and
four rejected outcomes on 32 real candidates. The original 7,808-source
observation is still running with frozen source.

The actual RTX5090 point qualifier returns all 474 captured arithmetic entries
from 169 source IDs, with the same two exactly checked witnesses and no invalid
returned points or provider errors. The device context closes, provider exits0,
and the UID-owned Job is gone. Complete finite cold lifecycle is30.746s.
This is offline functional hardware qualification, not online candidate
batching, native proof equivalence or end-to-end acceleration.
[Actual device/phase/resource/retirement records](../../artifacts/arithmetic-counterexample-2026-10-23/gpu-point-qualification-1/result-review.md).

## Source responsibilities

- Prepare.lean / prepare.py locate and wrap source-native arithmetic syntax.
- Counterexample.lean exports the actual supported typed goal/context; only
  the native recursive placeholder is excluded and logged.
- worker.py checks exact rational/integer points and source/entry ownership.
  Errors or no witness keep native fallback and enclosing proof alternatives.
- point_proposals.py constructs the finite rational grid and sampling recipes.
- gpu_points.py / points.cu pack/evaluate goal programs. A fixed kernel is
  reused; floating masks alone never authorize rejection.
- point-provider.py is a finite benchmark endpoint with actual device and
  CPU-reference backends. CUDA initializes on the first monitored request.
- qualify-remote-points.py checks an offline batch through the actual endpoint.
- build-point-job.py / device-lifecycle.ps1 package and run the existing finite
  K8s route, including process exit and UID-owned cleanup.
- qualify-screening.py runs the pending native24 qualification, then accepts
  --full for an original7808off/on pair. Full off uses untouched original
  Lean sources; on pays native parser/export preparation and GPU screening.
- analyze-screening.py reports paired statuses/acceptance changes, failures,
  timeouts, fixed baseline1%/10%tails and separate warm/cold cost accounting.
  Its closed32observation replay validates analysis only, not GPU benefit.

## Resources and boundaries

Use the existing Workspace and RTX5090 route. Keep48GiBtotal owned sampledRSS,
at most two actual REPLs, each24GiBaddress space, and fourCPUeligibility8–11.
A point-only check may overlap the observation under a joint monitor; it
creates no extra REPL. Native24/full pairs still wait. The monitor can include
a retained owned root only after PID/start validation and writes any actual
budget failure into that REPL's original attribution directory.
[Joint admission and limits](../../artifacts/arithmetic-counterexample-2026-10-23/joint-memory-and-point-admission.md).

One sample in the subsecond point transaction is not a complete cold-lifecycle
RSS peak or hard quota proof. API readiness precedes CUDA initialization.
Kernel-only time and offline replay batches must not be called proof speedup.
The GT/GE exporter is compiled in separate fresh outputs with joint memory
monitoring. Native runtime qualification remains pending; the ongoing
observation keeps its original frozen binaries.

## Repeat closed CPU functional checks

Use the Workspace's existing NumPy environment and a fresh output directory:

    python bench/lean-counterexample/qualify-points.py --backend cpu \
      --input artifacts/arithmetic-counterexample-2026-10-23/point-evaluator-qualification-input.jsonl \
      --out /tmp/own-point-qualification

The socket check starts and retires its own short CPU-reference process on an
OS-assigned port, without CUDA or Lean execution:

    python bench/lean-counterexample/qualify-protocol.py --out /tmp/own-point-protocol

The PowerShell lifecycle runs from the sole spark-manage controller checkout
with the actual SourcePod, a fresh Workspace Out path and Phase points,
lean24 or lean-full. First review native24outcomes before running lean-full. Source/build/result work stays in the owning Workspace. No persistent
Service, Workspace, additional schedule or Agent is created.


## Analyze a closed own pair

From the owning Workspace, run the existing capture Python with the two
completed cell directories and a fresh result directory:

    python bench/lean-counterexample/analyze-screening.py \
      --off <run>/off --on <run>/gpu --out <run>/analysis \
      --lifecycle <run>/lifecycle.json --preparation <run>/summary.json

The lifecycle receipt is available only after actual provider retirement.
HTTP/body sums can overlap. Whole warm-group and complete native lifecycle
ratios are separate from cold controller accounting. The cold residual
subtracts the measured off cell from the complete combined controller clock,
so it includes preparation, GPU execution, controller/API work and provider
exit. One fixed-order pair does not quantify host-load/run-order uncertainty.
