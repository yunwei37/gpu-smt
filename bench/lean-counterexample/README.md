# Arithmetic counterexample screening

This is our current experimental method. It does not reproduce an external
solver or accept Lean proofs from a numeric answer.

1. Prepare.lean locates actual arithmetic tactic syntax; prepare.py wraps its
   original byte spans without rewriting the candidate tactic.
2. Counterexample.lean exports a typed current goal and complete supported
   ordinary context. Unsupported expressions retain native execution.
3. worker.py checks rational/integer counterexamples. A checked witness fails
   only this arithmetic tactic, preserving enclosing alternatives.
4. point_proposals.py supplies the measured rational-grid proposal recipe.
5. gpu_points.py and points.cu pack multiple real goals into a fixed CUDA
   interpreter. Each GPU thread evaluates one point; each grid row is one
   goal. CUDA outputs proposal masks only. CPU reconstruction and exact
   checking remain mandatory.

## Current qualification

The frozen off/observation Lean hook returns matching statuses on 32 real
candidates. The full original 7,808-source observation is still running.

The GPU kernel compiles to compute_120 PTX with the existing CUDA 12.8 SDK.
The CPU bytecode qualification covers 474 captured entries from 169 sources,
with 4,096 points each (1,941,504 point evaluations). Proposal masks match the
nested evaluator exactly; both find two exact witnesses. **GPU execution,
RPC/Lean integration and end-to-end speed are not qualified yet.**

[Build, functional records and limits](../../artifacts/arithmetic-counterexample-2026-10-23/point-prototype-review.md).

## Reproduce the closed CPU functional qualification

Use the Workspace's existing NumPy environment. This command creates a fresh
output directory and does not launch Lean, a GPU Job or another full capture:

    python bench/lean-counterexample/qualify-points.py --backend cpu \
      --input artifacts/arithmetic-counterexample-2026-10-23/point-evaluator-qualification-input.jsonl \
      --out /tmp/own-point-qualification

A later finite GPU qualification uses the same input with backend device,
an explicit PTX path and optionally the existing nvcc path. It runs only
through the established RTX5090 K8s benchmark route, after the current
acquisition retires. Its host memory joins the same 48 GiB aggregate budget.
Offline replay batches must not be called concurrent online candidate batches.

Errors, unsupported contexts and no exact witness must retain native fallback.
The source's pending GT/GE extraction repair is not part of the active
frozen observation; its own qualification remains pending.

## Finite provider and worker interface

point-provider.py is the temporary benchmark endpoint for a device backend;
its cpu-reference backend is only our functional/algorithm control. The worker
uses GPU_SMT_CEX_GPU_HOST and optional GPU_SMT_CEX_GPU_PORT (default5001).
Returned points and source/entry identity are checked; provider claims are
never sufficient. The exact point is checked again by the worker before the
Lean wrapper may fail the current arithmetic tactic.

CPU-reference socket qualification returns two checked witnesses and leaves
the correct-goal control unrefuted. Endpoint closure falls back; all children
retire. [Actual protocol and memory evidence](../../artifacts/arithmetic-counterexample-2026-10-23/point-protocol-review.md).

The provider exposes owned RSS/birth/backend/affinity for the existing
aggregate watchdog. The optional capture callback includes it without enabling
the old LP method. It does not change the memory budget or other Workspaces.

qualify-screening.py is prepared for the post-observation24-source off/on
qualification, including actual witness sources. It is not yet executed.
No persistent endpoint, Service, additional scheduler or Agent is created.

To repeat only the closed CPU socket qualification in a new output directory:

    python bench/lean-counterexample/qualify-protocol.py --out /tmp/own-point-protocol

This starts and retires its own short CPU-reference process on an OS-assigned
port. It does not use CUDA or execute a Lean candidate.

## Actual device qualification lifecycle

The batch endpoint has completed CPU-reference RPC qualification on all
474 retained entries in one batch. It returns the same two exactly checked
witnesses. This is offline batching, not observed online candidate overlap.

build-point-job.py packages only our source/PTX into the existing finite
RTX5090 Job path. device-lifecycle.ps1 is a Windows infrastructure entrypoint
invoked from spark-manage; application code and result directories remain
in the owning Workspace. It refuses an incomplete original observation,
preserves existing Jobs/results, and records actual process exit before
UID-owned cleanup. Neither it nor point-job.json has been applied/executed.

qualify-remote-points.py validates a remote backend's real goal responses,
CPU exact points and owned memory. Device mode requires original observation
completion. The alternative24-source qualifier also checks native children
have retired. [Executed CPU records and pending device boundary](../../artifacts/arithmetic-counterexample-2026-10-23/batch-and-device-preparation-review.md).

The point provider initializes CUDA lazily on its first monitored request.
API readiness alone is not device execution. A joint monitor may include
the retained original capture PID/birth and the provider while keeping
48 GiB total and max two actual REPLs. [Qualification and admission](../../artifacts/arithmetic-counterexample-2026-10-23/joint-memory-and-point-admission.md).
