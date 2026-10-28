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

The immutable cf1138b engine/native-library-repaired host side also exits0.
[Completepairedanalysis](paired-analysis.json),[native/resourceclosure](paired-ingestion.json).

| Condition | accepted | rejected | timeout | resource | external seconds |
|---|---:|---:|---:|---:|---:|
| Kimina4warm |14|7|1|2|1430.677580|
| Repairedengine before retry-frontier change |14|5|3|2|1540.705220|

The engine is descriptively7.690596%longer in this selecteddevelopmentpair.
AcceptedIDsets match exactly,including restored3086acceptance. Sources2507and
7230return native errors inwarm but timeout inengine. Rawpayloads differ on21IDs;
after the separately labelled top-levelenv/emptyAST view,only those two differ.
No diagnostic/metavariable/position rewriting is used. That is not all-status
parity or resource-layer victory. Source3086takes299.966440s inengine,close to
the unchanged300sdeadline;do not extend thatdeadline or hide tail outcomes.

Both sides execute27physicalattempts and5watchdogkills. Engine has2prepared
readyevents and3exclusivefreshfallbacks;all29registerednativebirths are retired
withno live/zombiesurvivor. Its samplepeak51,677,036,544B is overshoot,not hardquota.
Lateordinary7230does not start until3683solo retires10:47:56UTC,an observed
resourcebarrier;elapsedbenefit from changing it remains unmeasured.
Per-attempt warmenvelopes and engine retirement-inclusive clocks differ in
boundary and overlap;their sums are not a disjointwhole-flowcostbreakdown.

The initial analyzer incorrectly treated the requesteddirectoryalias and
canonicalbackendpath as differentexecutables. The post-run
[native executable identity](native-executable-resolution.json) verifies
samefiledevice/inode/size. It is separate from the unchangedfrozenmanifest,
not a retrospective launch-time attestation. The strict repairedanalyzer
rejects a differentexecutable/missingalias and replays this compressedartifact
without requiring the liveprivatebinary. All9analyzercontrols pass.

The db8ecbf retry-frontier source was not applied to either side. Next is its
unchanged24source resource-repair measurement,not full7808or newfailure/policy
layers. Rootself-review only,no strongest-warm gain or paperacceptanceclaim.
