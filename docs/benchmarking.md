# Measuring engine changes

The engine has two reusable commands: measure captures one execution,
and compare analyzes two saved captures. They do not reproduce another
system or deploy a service.

## Capture a fixed population

The measure command reads one complete [Batch](api.md) JSON object from stdin,
creates a cold engine/cache, runs the batch, waits for native retirement,
and writes one JSON capture to stdout. Keep stderr as the resource-event stream.

From the pinned Lean project's directory:

    lake env /absolute/path/gpu-smt measure \
      --repl /absolute/path/repl --project /absolute/path/lean-project \
      --environment immutable-lean-mathlib-project-pin \
      --cpus 8,9,10,11 --worker-cores 1 --memory-gib 48 \
      --policy fifo \
      < population.json > fifo.json 2> fifo.resources.jsonl

Use an external controller clock as well. The recorded lifecycle begins at
executable main entry and includes input reading, runtime setup, native work,
queueing, retries and backend shutdown. It excludes executable loading and
final record serialization/output. Keep those costs in the external clock;
do not call the internal ratio a complete cold-controller result.

Capture format version 1 retains every original source, task/candidate ID,
timeout and reuse setting, native response, status, attempt, process identity,
sampled peak and preemption history. It also records backend/environment
identity, scheduling policy, RSS/CPU configuration and lifecycle time.
Resource logs carry aggregate RSS; an attempt peak is not total engine RSS.

The default CLI backend starts a fresh native REPL for each independent
source. This default has no warm-state or COW advantage. The optional
prepared-host/sysroot pair selects the declared pinned-context import parent;
its identity, readiness, fallback and child retirement must be checked in the
capture/events before attributing any reuse. A measurement of the fresh backend
does not replace the strongest warm/native reference. Keep native reference
captures and adapters explicit.

The fifo, source-size, task-interleave and task-memory policies are available. Source size is an
unvalidated heuristic, not a learned predictor or a novelty claim.
task-interleave wraps FIFO and interleaves first-success task groups; all-mode
stays FIFO. This ordering is a prior scheduling technique, not a new contribution.
Reuse/mode/resource settings must match the intended consumer comparison.
reuse=false gives every duplicate a fresh native execution; reuse=true
permits exact completed and in-flight sharing in a deterministic pinned
environment. Report reuse as part of the method.

## Measured same-task memory policy

Use --policy task-memory with the same check,measure or serve command to select
TaskMemory::new(Fifo). FIFO ranking remains unchanged;only waiting RSS
reservations learn from actual completed same-task attempt peaks. This is an
explicit opt-in. Default FIFO and frozen captures are unchanged. Do not combine
it with a changed CPU mask,native backend,input ordering or cache mode and
attribute the combined difference to feedback alone.

For a matched new native preflight,repeat the command above changing only
--policy fifo to --policy task-memory and output paths. Use mode all,reuse=false,
unchanged task IDs/timeout/source and the same48GiB/CPU8–11point when measuring
this Workspace's population. Start only after the current sole native group
actually retires. Both measure invocations create fresh policy history;check
and serve retain observations for their engine lifetime. The existing
Capture.policy field records task-memory;no schema or additional log is needed.

Only positive physical-attempt observations are used,after native retirement.
Task ID,backend/resources and timeout scope history. Different siblings can
have different demand:a large one may overreserve or serialize small ones,
while a preempted peak is only a lower bound. Keep the actual-RSS watchdog,
exclusive retry,parent reclamation and every operational outcome. No result is
predicted or reused by this policy. Report accepted-set/status differences,
resource/preemption/retry history,tail behavior and external lifecycle clocks,
not just memory prediction or an internal ratio.

Pinned4.18native controls qualify feedback/raw-response semantics;CLI process
fixtures qualify selection/capture/retirement. Neither supplies original4.9
whole-workload throughput or a novelty claim. The task-memory CLI variant does
not interleave task groups;library callers can compose wrappers separately.

The [prepared real32development input](../artifacts/engine-resource-profile-2026-10-25/task-memory-preflight-20261027/README.md)
preserves exact original candidate bytes/fields and prior outcomes. It uses
outcome-informed heavy/ordinary task selection,not an unbiased full workload.
The [current release/preflight and real32 comparison](../artifacts/engine-resource-profile-2026-10-25/task-memory32-20261027T193536Z/README.md)
now completes both32-source cells:2832.462187/2169.738637s,exactly equal raw
outcomes(16accepted/7rejected/9resource failures),41/37attempts and9/5retries.
Selection is biased toward the tail;this is not fullpopulation or strongestwarm
evidence. Both sampledRSSpeaks exceed48GiB;1s response is not a hardquota.
The earlier competing build failure stays historical evidence.
Do not replace a healthy frozen executable or interpret a prefix as a full pair.

The [current full prepared-backend matrix](../artifacts/engine-resource-pair-2026-10-25/prepared-policy7808-20261028T034248Z/README.md) now follows
the complete32development pair. Both policies use the same actual prepared
Mathlib backend;two blocks reverseFIFO/task-memory order across all7808.
Eachpolicy starts cold. Only policy differs;preparation,parent eviction,
fallback,retry,serialization/retirement remain charged. The currentFIFOchild continues unchanged;the serial wrapper is stopped so the
three further policy cells do not launch. The user now prioritizes the matched
four-warm-REPL resource baseline and resource-layer repair. No result is
extrapolated from selected32. Privatecore retention and
closedcapture/resourcegzip are separatelytimed and additionallycharged.
The oldfrozen4.27generated.private cache is losslessly archived on the samePVC
for space;its cache must be restored before oldenvironment reuse. Current
4.9/nightly SDK/source/data/frozenexecutables are unchanged. No oldoracle run.

## Pair completed captures

    gpu-smt compare baseline.json candidate.json > comparison.json

Comparison checks exact source/ID/task/timeout populations and the pinned
native environment, total RSS budget and CPU eligibility. Different budgets
or populations are separate measurements. Worker core assignments, policies,
reuse-option differences and backend identity differences remain visible.

The report includes:

- Lifecycle ratio and candidate throughput using each capture's own wall clock.
- Accepted-ID differences, every status change and raw-response differences.
- Solved-task differences for pass@k, with no per-candidate parity claim when
  either side cancels siblings.
- Counts of timeout, resource failure, cancellation, preemption, reuse and
  actual attempts.
- Completion latency quantiles including queueing.
- Slowest 1% and 10% cohorts ranked by the baseline's accumulated native attempt
  wall durations, with retry costs retained on both sides.

Attempt sums overlap under concurrency. Neither those sums nor completion
latency sums are end-to-end time. Slowest-cohort membership is diagnostic, not
an oracle scheduling policy.

A favorable ratio alone is insufficient: inspect changed accepted sets and
operational outcomes, resource logs, controller clocks, input provenance and
contention. Resource-point changes can change which candidates complete.
An environment label records the operator's pin; it does not authenticate the
binary or make arbitrary stateful Lean metaprograms deterministic.

## Current priority: warm resource baseline

The user requests retained official Kimina with four warmed REPLs against FIFO
engine at48GiB actualRSS/CPU8–11,no AS cap,dynamic admission and exclusive requeue.
The historical two-worker warm cell also had24GiB-AS;do not pool its clocks with
uncapped four-worker retries. Own fresh-versus-prepared is a component control,
not overall engine benefit. [Attribution and priority](tmp/build-and-evaluate/step-0086-20261028T041734+0000/step-report.md)
retain six historical status changes and observer-cost unknowns.
Complete the current healthy FIFOchild and collect its source/output;do not resume
the deferred automatic policy queue. Qualify the matched resource baseline,
repair resource overhead,then fullpair and the fixed42solo cohort.
No further scheduling/failure/LRAT efficacy layer before this resource work.

## This Workspace's next execution

The current resource point, completed groups and pending original workloads
are recorded in [evaluation](evaluation.md#current-resource-point), with
the actual active capture linked there. Only one native collection group runs;
preserve its frozen source/resources until it retires. The prepared
[42 isolated inputs](../artifacts/engine-resource-profile-2026-10-25/isolated42/README.md)
remain a separate cohort. Do not copy an obsolete queue order from this guide
or pool old AS-capped captures with the current dynamic-resource point.

The [resource_pair example](../examples/README.md#matched-nativeprepared-resource-pair)
uses the existing streamed BatchEvents to retain final consumer results before
a whole cell finishes. Its physical-attempt and consumer journals have distinct
meanings. Complete in the consumer journal does not replace the post-shutdown
Capture/terminal or external cell clock. The additional recording cost belongs
to that driver's own version and both of its cells; older live captures remain
untouched.


## Internal task availability and consumer rows

Comparison reports internal_task_first_success_seconds and solved-task latency
quantiles, taking each task's earliest actual Accepted result after batch
submission. These observation times come from the batch result loop and include
queue/retry/retirement; they are not reconstructed native CPU intervals. Unsolved task IDs/counts
remain explicit; conditional solved-task quantiles do not hide their failures.
Cache/coalesced checked decisions remain labelled through existing provenance.

These are internal acceptance events. Collected HTTP/CLI routes reply after
the whole batch; the optional typed NDJSON route has its own
[streaming contract](api.md#http). These fields do not measure client delivery.
Use a client/controller clock for delivery, parsing and full cold lifecycle.

returned_candidates_per_second counts returned consumer rows, including
cancelled/cache/coalesced rows. The earlier candidates_per_second key remains
as the same value with an explicit scope string. Neither denotes fresh native
verification throughput; physical-attempt statistics retain their per-caller
history/coalescing limitations.

Attempt memory is observed, not uniformly sampled or a complete high-water.
Use rss_observation events to separate current leader RSS, wait4 leader HWM
and registered-tree sampling. The combined maximum remains a conservative
admission observation. Complete aggregate RSS comes from the owned-tree event
stream. Historical attempts without kind metadata remain ambiguous. Do not
train a new-RSS-point source model from old AS-capped bad_alloc labels or
concurrent aggregate envelopes presented as per-source allocation peaks.


## Code-verification source frontend

The same measure command accepts --lean /absolute/pinned-sdk/bin/lean instead of
--repl. Launch from the matching project's lake env, with the same full Batch
input format and eligible CPU/48GiB resource point. It executes the stock JSON
stdin frontend, not a model/prover implementation. Keep this backend identity
and its source-path limitations explicit; it is not automatically equivalent
to native original-filename invocation or the strongest warm REPL reference.
Existing legacy Verina results remain at their recorded old resource point.
New whole-workload execution still waits for the sole retained native group.
