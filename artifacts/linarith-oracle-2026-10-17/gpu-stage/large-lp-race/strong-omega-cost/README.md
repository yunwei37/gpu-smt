# Strong common-omega backend cost accounting
RQ4/E1071. [Plan](plan.md), [root review](plan-review.md), [build](build.py), [phase source](phase.rs), [CPU proxy](support-proxy.py), [qualified data](qualification-result-review.md), [numeric analyzer](analyze-numeric-phases.py).
The current complete1000-source control is native+omega/same-dualbackend versus direct+omega/same-dualbackend. No GPU run here. Both use8queues/fourCPU4--7/48GiB; stockomega, numericalsearch/repair and fallback algorithms are unchanged. Retained Lean phase hooks add per-threadCPU/wall; numeric guards plus per-PIDwait4 retain cancelled-workerCPU and HiGHSprocessCPU. Unknown cancellation/internal/startup CPU stays bounded/unassigned.

Build in the owning Workspace with python3 build.py after the pinned Lean4.27/Mathlib dependencies exist. The crate uses its normal private target. The original qualification-driver.py includes a historical fast-hybrid control; [routing correction](reference-routing-correction.md) excludes that denominator. qualify-native-dual.py exercises the proper same-backend native frontend. Actual current qualification has3351joinedrequests,15unchangedsourceoutcomes/fullJSON, completechild/serviceaccounting and one0.55%observercomparison.

Status: both complete original1,000-source diagnostic cells closed:
475.968475283s native /406.461143583s direct, each992complete/8reject/0operational,
65message-only differences, no verdict or non-message mismatch.
[Complete results, cost table, conditional bounds and limitations](full1000-result-review.md),
[reproducible budget](full1000-complete-budget.json), [full raw](full1000-raw/).
Perfect numerical-work removal gives a conditional1.46068x component-reference
capacity ratio; deleting all Lean products too gives1.53960x. These do not
justify overall GPU closure or change the original whole-system criterion.
The forward logger fix is unmeasured; measured source and partial logs retained.
All work/reviews by this thread, self-review only.
