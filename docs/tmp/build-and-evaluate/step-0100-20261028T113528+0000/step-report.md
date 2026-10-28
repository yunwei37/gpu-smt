# Step0100 — preserve a timely native result through mandatory retirement

BUILD_AND_EVALUATE. Root only. The completed retry-frontier24 point is preserved
in step0099; no native research collection runs during these protocol controls.

## EXPERIMENT_GATE

See experiment-001/plan.md and result-review.md. The real-process old-source
control fails as expected: a timely accepted reply becomes Timeout while
waiting for retirement. The fix retains only a timely complete reply, still
awaits reaping and charges cleanup, and preserves late/cancel/error outcomes.
Existing peak metadata survives delayed acknowledgement. No new diagnostic
subsystem, timeout, quota or runtime knob is added.

Both focused controls and all64 workspace target tests pass; one doctest,
fmt/clippy/docs also pass. Five actual-Lean tests are locally ignored and must
run in CI. Release build succeeds. Every failed/raw result is preserved.
This does not establish that the observed real2507/7230 timeouts are caused by
retirement, nor does it measure a performance gain.

## WRITE_GATE

Public trait contract, architecture and implementation distinguish native
reply deadline from mandatory, fully charged retirement. The manuscript
describes this implemented boundary and queue-frontier ordering without
changing RQs, claims, scope, abstract or introduction. Compilation and changed
page inspection follow as a separate actual writing verification boundary.
No full writing/milestone review is claimed.

## REVIEW_GATE

See outer-audit.md. Source/test correction is complete; native CI and original
candidate qualification remain open. Root self-review only. Original research
goal remains active and incomplete; no full7808/fixed42 or new load-layer gain
is inferred from this narrow correctness result.
