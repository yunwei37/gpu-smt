# Associate retained failure-profile RSS with native body ownership

FixedRQ3:"How does prepared-state branching change end-to-end latency,throughput
and memory at equal resources compared with established warm-session reuse?"
This is original retained-data attribution within the failure diagnostic,not a
new comparison answering fullRQ3or a source-only forecasting result.

Question:can completed480native diagnostic data support source/body-associated
memory observations when final activity files have been overwritten? Use the
already-retained native C snapshots (live source/phase/active stack) and watchdog
PID/birth/RSS/monotonic timestamps,plus original request/response envelopes and
exact source bytes. No native run/model training is added.

The native C snapshots record source boundaries before updating ownership.
Build continuous observed body-owner runs,breaking on any boundary,unknown,
ambiguous thread,clock error or missing active body. Never extend a run beyond
its last valid observation;retain incomplete gzip metadata via existing reader.
Use only process IDs with one observed native birth. Never use aggregate RSS.

The sequential watchdog reads processes before writing its timestamp. Require
the entire previous-row→current-row window inside a body run and HTTP request
for that source,and the same PID/birth in both rows. This conservatively removes
switch/start/end windows;record all exclusions. Confirm original HTTPcode equals
canonical source;do not normalize a mismatch. Report per-source sampled
native-leader RSS,first sample,observed growth,coverage,history and censoring.
Those are history-dependent measurements,not independent true peak or uncapped
counterfactual demand. Header/provider/controller/other-native memory stays out.

Reuse original480status selection (355errors/83timeouts/42allocation failures),
old2workers/24GiBAS/48GiBaggregate resource point and instrumented environment.
Keep all480rows,unknown/null for missing observations. Do not train a global
model from selected failures or transfer the capped-resource labels to the new
fullpoint. Do not repeat the settled lexical first-success model.

Preflight on real archived data,then complete all existing480records in one
offline analysis. Python tests cover source/birth/time/envelope boundaries and
incomplete gzip handling;they are diagnostic controls,not native results.
Run CPU11under combined own+livefull48GiB monitor. No new native group,resource/
runtime change,subagent,OMP,CPUoracle or competitor reproduction.

## Prior-evidence correction and final scope

A later full-paper read finds Step0016/source-memory-attribution-2026-10-25had
already completed a477-source point-bracket join. The initial investigation
partly duplicates that work because the resumed summary omitted it.
Do not claim first attribution,new data/model or a new global result.
Retain that primary result and original scripts unchanged. This step is only
a body-active/full-sampling-window sensitivity control,using the same existing
2.5s native gap filter and exact source bytes. Compare body observations with
the primary body-only subset,not its mixed header/body coverage.
Keep the one-off code/tests under artifacts rather than adding a second core
analysis tool/CItest surface. No third memory association or model fitting
follows this unchanged cohort;next evidence needs the current fullpoint.
