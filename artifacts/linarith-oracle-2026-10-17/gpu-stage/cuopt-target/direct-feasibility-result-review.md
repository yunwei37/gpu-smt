# Direct-feasibility repair rejected before another full run
2026-10-18Z. Root implementation/self-review only; no delegated execution.

## Real protocol and observed failure
The repaired numeric proxy solves original certificate equalities with zero objective, explicit PDLP, infeasibility detection and first-primal-feasible, default crossover=false. It logs full input matrices and actual job IDs, watches native socket EOF and cancels a joint GPU solve only after all clients disconnect. Same48GiB limit and native300s request timeout; no tolerance/thread/time-budget search.

Eight archived real requests were planned (five positive, three no-certificate). First four all hit300.10s, including two originally positive certificate requests. The active GPU job was the known82x152/968nnz no-certificate system; it blocked other requests. Index5 returned a certificate process response in0.445s; it does not rescue four operational failures or prove Lean parity. Root rejected this repair and stopped remaining qualification children before another needless300s wait. Five observed case summaries are preserved; three remaining cases are partial/censored, never silently dropped or counted complete. Native24 repair preflight and any new full1000 are **not admitted/launched**.

[Stopped partial and exact identities](direct-feasibility-stopped-partial.json), [raw numeric requests/replies and matrices](direct-feasibility-numeric-partial/), [solver events](direct-feasibility-numeric-partial/summary.json), [actual target cleanup](direct-feasibility-numeric-cleanup.json), [prelaunch protocol](direct-feasibility-preflight-plan.md), [qualifier source](direct-feasibility-numeric-qualifier.py). The native original source cohort and current matched CPU controls are untouched.

## Cancellation and upstream boundary
The measured EOF/cancel path and per-batch outcomes are retained. Upstream official server behavior says a running CancelJob kills its worker rather than cooperatively stopping a PDLP iteration. Its open issue1662 reports possible sticky CUDA failures after such cancellation; this external report is not proof of a reproduced device error here. Do not add GPU-reset or otherWorkspace churn to rescue this numerical variant.
Sources: https://docs.nvidia.com/cuopt/user-guide/latest/cuopt-grpc/grpc-server-architecture.html ; https://github.com/NVIDIA/cuopt/issues/1662 .

## Decision and limits
This second formulation does not pass real numeric qualification, so no new full matrix, tolerance/buffer/worker grid or custom narrow kernel is started. The first phase-I variant already attempted all1000 in3374.147s with8operational failures. CPU-stage1.34668x remains interim; final same-plan CPU controls still run, and final best(CPU,GPU)>1.5x disposition remains pending. There is no universal impossibility proof for every GPU LP solver. This is bounded implementation failure evidence, not an achieved speedup.

The disposable numeric Job was deleted after qualifier exit143; otherGPUWorkspace Running/labReady. Original CPU driver18460 and prefix5256 survive. One finite pidfd-triggered offline collector will gather/analyze the full three-method cells at exact driver exit; no timer polling, newAgent or auto-commit. Root reviews/commits the actual closed result later.
