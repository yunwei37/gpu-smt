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

The fifo, source-size and task-interleave policies are available. Source size is an
unvalidated heuristic, not a learned predictor or a novelty claim.
task-interleave wraps FIFO and interleaves first-success task groups; all-mode
stays FIFO. This ordering is a prior scheduling technique, not a new contribution.
Reuse/mode/resource settings must match the intended consumer comparison.
reuse=false gives every duplicate a fresh native execution; reuse=true
permits exact completed and in-flight sharing in a deterministic pinned
environment. Report reuse as part of the method.

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

## This Workspace's next execution

The current resource point, completed groups and pending original workloads
are recorded in [evaluation](evaluation.md#resource-point-and-workloads), with
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
