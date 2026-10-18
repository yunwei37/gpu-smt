# Argument-faithful nonlinear ready-goal batching
E1069, RQ4. [Plan](plan.md), [source](GoalBatchArgs.lean), [numeric source](arithmetic-batchd.rs), [selection](input-selection.json), [real result](result-review.md), [analysis](preflight-analysis.json), [raw data](preflight-raw/).

Extends the first adapter with per-goal argument elaboration and original only/bang semantics. Custom configurations stay on the existing implementation. Retains complete batch requests/replies and exact-model dimensions and task intervals. Same native omega, direct frontend, two-sided numerical backend and48GiB limit. Build with build.py inside the existing owning Workspace; preflight-driver.py runs the recorded unchanged input.

Four prior-longest argument-bearing sources overlap one retained rejection, so the union is15 unique originals, not16. Both conditions return7complete/8reject/0operational. Whole84.058571s sequential versus79.769111s batch; one selected preflight is not a population speedup. Six groups contain1050 problems;1040 certificates check and10 require native fallback. Real nonlinear models now include42x167 and53x561 coefficient systems; actual floating-service calls are separately reported. No GPU performance is inferred.

[Additive GPU adapter](../additive-device/plan.md) preserves both CPU contenders. Its fresh matched CPU/reference acquisition is separate; device execution is not yet a result. All reviews are root self-review, failures/raw retained, no independent audit or overallGPU closure.
