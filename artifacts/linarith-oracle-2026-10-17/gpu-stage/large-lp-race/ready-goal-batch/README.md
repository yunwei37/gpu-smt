# Ready arithmetic goal batching
RQ4/E1068. Sequential Lean state extraction, parallel immutable numerical requests, sequential native certificate checking. This is a functional batching interface, not an established GPU speedup.

[Plan](plan.md), [source](GoalBatchOracle.lean), [numeric daemon](arithmetic-batchd.rs), [build receipts](build-receipt.json), [real12-source result](result-review.md), [analysis](preflight-analysis.json), [raw data](preflight-raw/).

The owning Workspace retains pinned Lean4.27/Mathlib and the two-sided-oracle/native-omega dependencies. build.py reproduces the combined library and numerical executable; preflight-driver.py runs the exact recorded original inputs with batching off/on. No source or executable used by the active full-population acquisition was replaced.

The first prototype accepts only bare all_goals linarith/nlinarith. It batches two real512-problem groups and checks all1024 certificates, but these groups have no observed parsed external large-LP requests. End-to-end98.964525s versus98.469642s is a single preflight near tie, not useful performance evidence or a GPU result. Argument-bearing nonlinear tails and complete model-shape telemetry are not covered yet.

All work/review is by the root thread. Source/compiler failures, native fallback, all8 rejected originals and warning differences are retained. No full matrix admitted.
