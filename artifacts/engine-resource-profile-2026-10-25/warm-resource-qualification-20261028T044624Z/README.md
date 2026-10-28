# Corrected four-warm resource qualification — closed warm side

The installed retained Kimina Manager/run_checks returns all24selected sources
at the CPU8–11/48GiB actual-RSS/no-AS resource point. Four preheated REPLs each
map the existing ordinary native Mathlib linarith library;this is ordinary
compilation,not the frozen CPU oracle or a new contribution.
Exact executed adapter/source/pins,input,all native payloads,attempts,readiness,
RSS,preemptions and process exits are retained byte-for-byte (.gz where noted).
[Summary](summary.json),[ingestion comparisons](ingestion.json).

| Outcome | Sources |
|---|---:|
| valid |14|
| Lean error |7|
| timeout |1|
| resource failure |2|

Twenty-seven physical attempts include three concurrent preemptions and their
three solo reruns. minif2f-1885 then times out;3683and3685 exceed the sampled
budget again. Five watchdog kills and peak51,768,815,616B (48.213GiB) are sampled
responses,not a kernel quota. No native workers survive final cleanup.
Sources,timeout300s and no-reuse options match the frozen24input exactly.

Internal lifecycle1429.077858s includes preparation3.578960s;external
launch-to-exit1430.677580s is retained separately. These differently bounded
clocks are not interchangeable. Root compilation/ingestion overlapped on the
same allocated CPU set,so this selecteddevelopmentpoint is not final throughput.

The historical problematic3086 now passes in this warm side;2325/2507/3209/
7230 return Lean errors. Source1885still times out at this no-AS resource point,
where the historical24GiB-AS warm run had a resource failure. This warm-only
observation does not establish causal repair or full engine parity.

The immutable cf1138b engine/native-library-repaired host side starts
sequentially10:27:16UTC and remains pending at ingestion. Retry-frontier code
db8ecbf was not loaded into either side. No pair speedup/full7808gain,
newmethod novelty or independent audit is claimed. Review the complete pair
before changing the native resource point or stacking workload-layer gains.
