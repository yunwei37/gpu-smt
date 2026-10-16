# Existing-cache and full oracle-log reuse screening: result review

Observed 2026-10-16T00:59:37.690600+00:00. Root personally executes and self-reviews; no independent audit.

## Question and decision

Does the expensive CPU profile justify either blindly adding another generic
Meta cache or repeating the failed scalar GPU constructor? No. Source inspection
finds existing context-sensitive Meta caches; the profile does not measure their
misses or query operands. This whole-log screening identifies exact repeated
numeric oracle inputs on a different CPU route, but it neither implements a
cache nor establishes batching, actual saved work, or a new system contribution.
The failed narrow synchronous GPU constructor remains closed.

## Full closed-log evidence

The Fast/hybrid reference profile covers 29,750 unchanged input attempts and
retains a closed 502,329,013-byte oracle.jsonl. The offline
reader processes all 173,941 lines: 62,197 parsed LP
records, 55,710 Fast metadata records, 56,006 untyped metadata records, and
28 malformed JSON lines. Every malformed line number and
actual parser error remains in the summary; no guessed stitching, selected
deletion, logger repair or native rerun is used. Telemetry catches emission
errors, so parsed records are not a complete call census.

Among parsed LP records, 30,898 exact ordered
problems produce 31,299 repeat occurrences
(50.322363% of parsed
queries). Identity preserves all fields, object/list order, relations, variable
indices and exact integers. No mathematical normalization, rounded coefficients,
hypothesis permutation or source filtering is used.

There are 59,756 successful and
2,441 failed oracle records. In
29,908 successful
occurrences the same exact problem has an earlier successful callback ending
before that call starts. This timestamp predicate is not a demonstrated
cache hit, cache availability, independence or measurable saving: the log is
emitted after the timed callback, and worker identities/publication delay are
absent.

The sum of parsed per-call elapsed wall intervals is
1465.205162857s. The prior-success-repeat-associated
subset sums to 283.281454185s
(19.333910% of
that sum). Intervals can overlap. Neither sum is CPU work, whole-run time,
removable latency or an end-to-end acceleration ceiling. Repeat count is
particularly unsuitable as a claimed performance gain.

The LP size distribution is maxVar median8/p95110/max1614, hypothesis rows
median15/p95325/max5151, coefficient entries median41/p952571/max43690.
All 32,258,256 coefficient entries are exact integers;
the largest has 106,285 bits. A floating-point
LP result cannot be called an exact Lean certificate without the declared
native reconstruction/validation path. These observations do not prove GPU
infeasibility, identify ready parallel batches, or estimate their useful cost.

The records contain 21,234 distinct logged source texts
and 6,831 LP groups spanning multiple
logged texts. None matches the original input code bytes exactly. One inspected
example differs by the import/blank-line prefix, but the full mapping has not
been established. Accordingly these are logged-text associations, not a
qualified per-input/attempt recurrence result. No input/header is changed.

## Actual reader failure retained

The initial reader fails on eight real large-integer rows because Python's
default integer-string limit is4300 decimal digits; one actual coefficient
contains15,955digits. Its other28JSON errors remain distinct. The initial
partial summary/log/grouped outputs are preserved, not overwritten. The
corrected read-only process alone disables that conversion restriction, retains
arbitrary-precision integers, reads the entire original archive, exits0, and
leaves28malformed JSON rows. Native SDK/logger/runtime settings are unchanged.

The initial largest-coefficient value was incomplete because those eight rows
were omitted; it must not be used as the full bound. Corrected summary and all
compressed query/group/source rows are retained. Analysis runtime is
141.777734s, not verifier performance.

## Existing source mechanisms and scope

Installed Lean4.27 Meta/Basic.lean320–386 defines infer-type/whnf/synthesis and
permanent/transient definitional-equality caches;647–667 includes ordered
expression/config keys. ExprDefEq.lean2060–2101 selects transient state for
metavariables or specialized unfolding and handles assigned metavariables;
2163–2178 performs lookup/result insertion. SynthInstance.lean770–806 already
caches by local instances, type and pending depth. A second generic cache
without demonstrated missed reuse is not admitted on the 35% inclusive
CPU-path weight alone.

Farkas Instrument.lean20–35 surrounds the oracle with monotonic timestamps and
logs the exact maxVar/hyps plus certificate/error after the timed callback.
Telemetry.lean35–45 preserves integer serialization but catches sink errors.
Native.lean58–60/115–124 sends the same exact numeric protocol; the shown
oracled.rs stdin loop94–108 invokes respond for each line. These observed
paths do not establish that every component lacks caching.

This log belongs to the Fast/hybrid reference route. E032's full CPU sampling
belongs to the plain compiled original route. Do not transfer its35%Meta/
16.96%inclusive oracle weights to this log or the composed product candidate.
No live capture, input population, solver, SDK, resource setting, GPU owner,
deadline or scheduler is changed. No new native benchmark is launched here.

## Research disposition

Retain the failed scalarGPU/placement/SMT-prefix mechanisms as negative results
and stop their small tuning variants. Complete the already admitted whole
CPU/resource controls. Any replacement GPU mechanism must demonstrate expensive
useful parallel work against a competent CPU route; exact-repeat counts alone
are insufficient. This screening does not replace the real-stream/service/
end-to-end/device/RQ/paper requirements or establish novelty.

[Corrected complete summary](fast-reference-oracle-reuse-full-integers.json),
[actual corrected log](oracle-reuse-screening-full-integers-20261016.log),
[initial partial summary](fast-reference-oracle-reuse.json),
[initial log](oracle-reuse-screening-20261016.log),
[question/source boundary](reuse-screening.md),
[actual analyzer](../../../../../artifacts/lean-modern-native-compilation-2026-10-14/analyze-oracle-reuse.py).
