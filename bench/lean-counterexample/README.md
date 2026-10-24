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
