# Complete ProofNet prefix capture:5,952 original candidates
All186original32-candidate blocks complete in the retained Lean/Mathlib setup,
unchanged original order, four-CPU20--23 eligibility, width4,48GiB upstream
memory default. The retained prefix driver has retired; no restart is needed.

| Method | Whole seconds | Complete | Reject | Operational | Incomplete |
|---|---:|---:|---:|---:|---:|
| Native in-process batch |1127.279474057|413|5526|9|4|
| Exact-text prefix |2502.009591446|417|5531|4|0|
| Unit-text prefix |2479.034701545|417|5531|4|0|

Both prefix conditions retain all413native-complete sources with native kernel
receipts. Four batch-incomplete sources become complete; eight operational
sources become rejected; three rejected become operational; one remains
operational. Retain these per-source transitions, not an aggregate matching
claim. This is not a validated performance ratio, native-response transparency,
original-task accuracy or pass@32 result. Complete CPU is censored by forced
retirements (batch3, prefix4each). Source-level outcomes remain operationally
unknown where marked.

Exact prefixes execute13525nodes,37cached lookups and5580fallbacks.
Unit prefixes execute9716nodes,3853cached lookups and5581fallbacks.
These counters are execution/reuse observations, not a percentage of end-to-end
time saved or an estimate of common-proof-prefix CPU cost. Included native
parser times are9.083706318/9.364549671seconds. More cache hits do not deliver
useful elapsed savings in this observation: both prefix captures take over
twice the batch elapsed time, but different outcomes and censored CPU prevent
a valid speedup calculation.

Sequential recorded native request intervals have no pairing defects or
overlap. Failed request roundtrip wall is13.860770045batch,
609.149397807exact and610.307761487unitseconds:1.2296%,24.3464%,24.6188%of
their own whole clocks. These are waiting/roundtrip wall, not native CPU or
internal tactics; cleanup outside requests remains in whole elapsed.
Failure waiting explains part, not all, of the increased elapsed time.

This is our retained native executor using the upstream SHRED parser lineage,
not a reproduction of the complete upstream SHRED service. The in-process
batch baseline is a Kimina-style prepared native process, not a deployed
Kimina service with every policy reproduced. Formal complete RQ3 service
comparison and repeated matched scheduling/memory-policy trials remain open.
This experiment does not establish a new prefix-sharing contribution.

[Full analysis and transitions](analysis.json); [raw batch](batch/),
[raw exact](exact/), [raw unit](unit/). Reproduce with:
```sh
python3 bench/lean-native/linarith-oracle/analyze-prefix-runs.py artifacts/linarith-oracle-2026-10-17/formal-default/proofnet
```
All data copied only after terminal receipts; no original records rewritten.
All work/review by this thread; root self-review, not independent audit.
