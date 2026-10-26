# Full sampling-window/body-active sensitivity of the prior memory join

Root-only self-review,2026-10-26. This is a control on the same archived
observations,not a new native experiment,dataset or trained predictor.

## Prior evidence and correction

[Step0016](../../../docs/tmp/build-and-evaluate/step-0016-20261025T115728+0000/step-report.md)
already produced the [primary477-source result](../../source-memory-attribution-2026-10-25/result-review.md).
It uses point timestamps,adjacent native ownership labels,observed births and
HTTP envelopes. That result and its raw records/scripts remain unchanged.
The current resumed investigation initially overlooked it and duplicated part
of the analysis. The remaining justified scope is one sensitivity check with
full read windows and active-body observations,not first-time attribution.
One-off code/tests stay here;no second core pipeline or general CI test is added.

## Method and source basis

The existing sequential watchdog reads RSS before writing time_ns
(bench/lean-native/linarith-oracle/memory_budget.py). Thus the preceding row's
timestamp and current timestamp bound the current RSS read. Require the same
native PID/birth in both rows,one observed birth for that PID,exact canonical
HTTP source bytes,and the whole read window inside agreeing native active-body
observations and the matching request envelope. Break at source boundaries,
idle/unknown/conflicting frames,and the same existing2.5s native gap criterion.
The C snapshot records source boundaries before updating the source tag.

Reuse the existing partial-gzip reader:all126native streams lack trailers but
have valid retained complete-line prefixes. Do not extrapolate their tails.
Do not assign aggregate controller/other-worker RSS or header/idle snapshots.
All480source rows remain,with null memory when no window qualifies.

## Completed result

[Final result](final/attribution.json), [matched rows](final/attribution.samples.jsonl.gz),
[comparison to primary](comparison.json), [actual command/RSS receipt](final/receipt.json).

| Profile result | Sources | Body-window observed | p50 observed maximum GiB | Max GiB |
|---|---:|---:|---:|---:|
|Ordinary error|355|310|3.68|12.64|
|Timeout|83|83|14.71|22.60|
|Resource failure|42|42|23.27|23.46|

p50uses nearest rank as the primary analysis. Values are maxima among admitted
samples per source,not actual unobserved high-water marks.45ordinary-error
rows remain unknown. The prior mixed header/body coverage was477;its body-only
coverage was463(338ordinary errors). Thus this is not a477vs435workload change.
No new source classification or resource point is introduced.

All33,039matched rows are a subset of the primary34,130body rows;matching
source/time/PID/birth tuples have exactly the same RSS values. All83timeouts
and42resource failures retain the exact earlier per-source sampled maxima.
137ordinary-error observed maxima decrease under trimming;none increases.
The critical high-memory observations are insensitive to this boundary choice,
not thereby causal,independent or valid at a different resource point.

Unassigned native rows:126first/changed-process windows and1,350windows outside
a qualifying body-owner interval. Source byte mismatches0.324observed sources
have prior selected-source history on the same PID;that is not complete cache
history. Imports,allocator/process history,diagnostic tables and instrumentation
remain in measured occupancy. Old24GiBAS failures do not label >24/48GiBRSS.

## Validation, provenance and limits

Four analysis tests pass:full window/HTTP/birth constraints,transition even when
a tag returns,unknown/idle/conflicting ownership,and valid truncated-gzip prefix
without tail extrapolation. Initial/confirmed runs and their source snapshots
are retained;the final one-off path makes the sensitivity role explicit and
adds the matched-row sidecar. The confirmed exact-birth guard and original run
produce identical row-level summaries;the final existing-gap filter also leaves
the result unchanged.

All runs are offline,CPU11,combined with original live fullpair under48GiB1s
monitoring. Final sampled peak29,601,259,520B;the earlier confirmed run's combined
peak47,333,916,672Breflects the different contemporaneous native state,not a
memory regression of this analyzer.0pressure/monitor errors. No native candidate
is started,stopped or retargeted. Sampling is not a kernel quota.

The cohort is failure-selected,warm/process-history-dependent,instrumented and
AS-censored. No model is trained or transferred to the current uncapped full
point;the settled negative lexical first-success model is not rerun.
No further association variant is selected for this unchanged cohort. Revisit
only if a concrete attribution defect or different capture/resource point changes
the question. Continue other user directions while the sole fullpair runs.

Recompute under the owning process budget:

    python3 -B artifacts/lean-failure-profile-2026-10-25/body-memory-association-20261026/analyze-window.py --run artifacts/lean-failure-profile-2026-10-25/full480 --inputs artifacts/engine-resource-profile-2026-10-25/population-inputs/all.json.gz --out /tmp/body-window-attribution.json

The initial source/test paths were moved from bench/tests into this one-off
artifact after the prior result was found. Initial receipts retain the actual
historical paths;initial-analysis-source.py and initial-tests-source.py preserve
those versions. final/run-source.py records the final executable paths.

The paper adds only the sensitivity scope and unchanged125critical maxima;
the primary477-source result remains. Existing pinnedTectonic compilation
succeeds and allfourRQlines remain byte-identical. paper-compile/ retains the
actualPDF/log/receipt;layout warnings remain,so compilation is not paper readiness.
