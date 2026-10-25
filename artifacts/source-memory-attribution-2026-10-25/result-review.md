# Source memory attribution — root self-review

Completed existing-data diagnostic, not a predictor or native speed result.
All clocks/worker identities below come from the same completed480failure profile.

## Coverage and missing observations

- 480selected sources retain355Leanerrors,83timeouts and42resourcefailures; status changes:0.
- 477sources have bracket-inferred RSS observations. Three ordinary-error sources are missing, not zero.
- 34284of34515native-worker RSS samples satisfy the stated bracketing/PID/HTTP rule.
- Excluded: {"outside_source_HTTP_envelope": 19, "unbracketed_time": 84, "unusable_label_bracket": 128}.
- All126native streams lack gzip trailers after termination, with0trailing partial bytes; surviving complete records are retained through the existing partial-stream-aware reader.
- Sampler/capacity/clock flags are0. These facts do not recover unseen allocation peaks.

## Sampled single-worker process occupancy

| Old profile status | Sources with observations | p50 GiB | p90 GiB | Max GiB |
|---|---:|---:|---:|---:|
|lean_error|352|3.6733|6.9695|12.6409|
|resource_failure|42|23.2720|23.3677|23.4560|
|timeout_error|83|14.7089|17.6561|22.5955|

These are asynchronously sampled process occupancy during an inferred source
context, including imported/retained state, allocator history and diagnostic
overhead. They are not source-only allocations, exact true high-water marks,
removable memory, or4worker admission guarantees. All42resource failures have
direct bad_alloc messages; their sampled occupancy is concentrated near23GiB,
under the old24GiBaddress-space cap. Address space and RSS are different metrics;
allocation failure is not a label that actual RSS exceeds24or48GiB. Burst
allocations can also be missed by1s sampling.

A process is associated only when its observed birth is unique, adjacent native
source labels agree with <=2.5s gap, and a unique same-clock HTTP envelope
contains the RSS snapshot. Birth here is recorded psutil create-time seconds;
new Rust identities use kernel start ticks. Do not equate those representations.

Concurrent native/whole-tree envelopes are retained separately. They bound
possible per-worker values at those sampled instants only and are never called
a source peak or a bound on an unobserved maximum. Per-source missing cells
remain blank/null. Invalid/unknown labels and unbracketed times remain excluded.

## Consequence for the new engine

The failed-only, instrumented, AS-censored480cohort does not calibrate a full
uncapped7808population predictor. These measurements support the need for
dynamic memory-aware admission and isolated42reruns, not four-way admission
by candidate count or a trained source classifier. New same-resource native
observations remain necessary before forecasting/throughput claims.

The audit also found the engine peak field mixes registered-tree RSS samples
with a backend supplement: fresh transport samples the leader before retirement,
while the prepared child supplies wait4 leader high-water. Those kinds must be
retained explicitly, not described uniformly as sampled RSS or whole-tree HWM.
The implementation now records rss_observation events with kind,PID,birth and
bytes, preserves the conservative maximum for admission and exposes a clearly
scoped measurement alias without changing native responses. Old records without
kind metadata remain untyped. This is data provenance, not an acceleration.

Actual implementation checks/CI are appended at the completed boundary. All
four RQs/directions remain open; CPUoracle remains frozen. Root self-review
is not independent audit. The original native group stays live; no second
native acquisition starts.
