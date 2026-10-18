# Native integer arithmetic CPU control
RQ4/E1067. Existing Lean omega is a competing standard CPU algorithm, not the project's contribution.

[Plan](plan.md), [self-review](plan-review.md), [source](IntegerControl.lean), [build receipt](build-receipt.json), [real preflight](preflight-result-review.md), and [raw preflight data](preflight-raw/).

Runtime prerequisites are the retained Lean4.27/Mathlib and two-sided-oracle build used by the main experiment. Build with python3 build.py in the owning Workspace after these dependencies exist. run-control.py reuses the source-native collector and selects the native or direct frontend through the finite benchmark driver. All newly measured variants load the same compiled module set. Explicit arguments/options remain on the original path, and failed omega restores the tactic state.

The full1000 comparison runs native+omega, direct+omega and direct without omega, using four CPUs,8queues,48GiB and the same numerical backend. Launch is not completion. Raw/data analysis, normal setup/fallback/retirement costs and all warning differences remain. Full-population and prefix acquisitions are unchanged.

Root thread executes and self-reviews. No agents, OMP, new Workspace or persistent service.
