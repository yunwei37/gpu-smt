# Step0142 — enforce requested PVC output placement before capture startup

BUILD_AND_EVALUATE;root only. Latest direct user instruction explicitly allows
G10 development work while lab approval is pending and requires a script check.
One storage bug boundary,not a new scientific experiment.

## EXPERIMENT_GATE

Entry: actual main/upstream worktree,step0141,current G10 host,contributor guide,
CI entrypoint and nearby tests. Foreign dirty paths remain untouched. The new
user prompt is appended verbatim to docs/user-instruction.md.

E142.1: main-entry regression engages the actual missing validation:pre-fix
affinity was called despite an invalid/tmp output path. Retain the red log.
[Plan](experiment-001/plan.md),[self review](experiment-001/plan-review.md).

E142.2: early canonical path,mounted-root and same-device validation in run.py.
It executes before optional psutil import,affinity,mkdir or Lean startup.
7 relevant regressions plus complete68-test Python suite pass. Actual PVC
write/read and escaping-symlink CLI rejection checked onG10;no native run.
[Result review](experiment-001/result-review.md),complete logs/command summaries
and actual-placement-check.json separate mocked from real checks.

## WRITE_GATE

Existing capture README documents exact guard behaviour and limitations;daily
maintenance records the loss lesson. Node eviction's container total is measured,
while the dominant/tmp attribution is identified as the user's report because
there is no retained du breakdown. No unrelated documentation or engine API
change. Paper source/RQs/claims/numbers and frozen Lean/C modules unchanged.
No paper build,full writing loop or milestone review claimed.

## REVIEW_GATE — same-thread self-review

Checked branch/scope,path canonicalization,containment vs prefix confusion,
mount/device mismatch,CLI early rejection,absence of writes/native launch,
red-test engagement and all68 green tests. One14-line production helper and
one6-line call;test growth is justified by separate filesystem/startup boundaries.
No new abstraction,dependency,daemon,resource cap or bypass switch.
The latest user explicitly authorizes the check;it is not an invented gate.

The prepared recovery must use a new frozen guarded collector snapshot while
retaining old aee0932 source history. The8031 input,5390 pending/5 deferred
retry plan and qualified ae59c77 Lean/C sources stay unchanged. No collection
is started onG10 and the existing lab approval question is not repeated.

Direction remains the measured expensive ordinary-failure opportunity. Storage
engineering/tests are not novelty or complete replay certification. No independent
audit by user instruction. Commit/push this validated step,refresh the prepared
collector source and continue other G10 work without claiming formal results.
