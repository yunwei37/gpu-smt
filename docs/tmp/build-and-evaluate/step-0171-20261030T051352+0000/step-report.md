# Step0171 — portable automatic service resource defaults

BUILD_AND_EVALUATE; all implementation/review by this chat, self-review.
User explicitly requests usable onboarding and automatic CPU/memory defaults.
This change touches CLI defaults/documentation/tests, not native semantics,
research capture parameters, cluster configuration or historical data.

## EXPERIMENT_GATE
Existing CPU eligibility is discovered; new defaults also honor visible cgroup-v2
ancestor CPU quotas. Memory defaults to80% of current available capacity,
bounded by remaining cgroup-v2 memory. Explicit research flags still override.
Physical total/swap are not used as available capacity. Errors fail explicitly.
Three timer-free resource unit tests and one real empty-batch CLI integration
cover auto selection and explicit1GiB override. G10 CLI really exits0 with
CPUs6–7 and a snapshot-derived budget; no native candidate/process is launched.
This is a startup-default test, not an authorized larger G10 research capture.
Fmt/clippy complete successfully. Full signal lifecycle suite is delegated only
to existing CI because G10 denies own-child signals; do not rerun that fault.

## WRITE_GATE
CLI help removes hardcoded research CPU/memory examples. API documents formula,
override behavior and current cgroup-v1 auto-discovery limitation. Next step
provides pinned one-command environment, client and user-facing README.

## REVIEW_GATE — self-review
No fixed default48GiB remains in CLI. Parent controller limits are inspected
without changing them. Runtime/thread CPU masks retain existing inheritance.
No production failure cache, new source-cost predictor, external agent, UI,
CronJob, security or deployment change. Preserve all unrelated dirty paths.
