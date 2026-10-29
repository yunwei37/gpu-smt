# Step0150 — preserve CronJobs and enforce shared-node collection stops

BUILD_AND_EVALUATE,root only. Read latest direct user words,step0149 and actual
quiescent G10 state. Existing cluster CronJobs must not be changed,suspended,
deleted,manually triggered or rescheduled. No such command is issued.

## EXPERIMENT_GATE
Engineering dependency only,not paper evidence. [Plan](experiment-001/plan.md)
and [result review](experiment-001/result-review.md).
E150.1:Implement startup signal-retirement controls,host available-memory floor
and asynchronous existing-account API readiness in the finite capture script.
Keep nominal1s ownedRSS sampling independent of HTTP;failure/stall/available<6GiB
stops the whole group,with operational retirement evidence and no fake candidate
rejection/retry. Current max/default12GiB cannot be raised even on a larger host.
No fixedAS,credential creation,security policy,production engine/native observer,
schedule or CronJob changes.

E150.2:Nine new regressions yield81Python passes. Initial fixture escaping errors
and intermediate successful checks are preserved. Final tests CPU6–7 sample
82,173,952B ownRSS;minimum sampled host available21,492,310,016B. Pure development,
no native workload. Self-review puts final API drain/shutdown before computing
controller terminal time/completion;all real guard costs belong to the new point.

E150.3:Actual G10 entry reaches only its finite2s Python signal control. PID/birth/
errno13/exit0/natural retirement are recorded. It refuses startup:zero Lean
launches,zero candidate rows,no segment and no complete terminal. All output on
PVC. This establishes current refusal,not under-load API/memory guard qualification
or a kernel-hardRSS cap. A source reconstruction is labelled as reconstructed,
not a captured-time source copy. No repeating expensive positive/native control.

## WRITE_GATE
Append only the user's verbatim request. Canonical evaluation and capture README
now distinguish implemented guard paths from remaining live qualification.
Explain new12GiB max/default,existing-account-only API,probe/sample response
latency,whole-collection stop semantics and unchanged cluster CronJobs.
No paper result/claim/RQ/evaluation promise or frozen scientific contract change.

## REVIEW_GATE — same-thread self-review
Production script net growth is~132lines;tests~108lines. One internal background
API worker is needed so HTTP cannot block the existing parent RSS sampler;it
retires with the controller and is not a new service/daemon/schedule. No new
dependency/helper schema,permission or flag bypass. Resource/credential absence
is not a proof failure. API failures do not disappear at successful termination.
No claims of native replay,under-load stop guarantee or hard quota.

Native capture remains off because the actual interruption control fails.
Existing Pod account lacks readiness material;no permission request/change.
Continue authorized low-load G10 implementation while preserving shared jobs.
Full Python CI follows push;prior source Rust88/native6checks are not relabelled
as tests of this Python-only patch. No agent delegation or independent review.
