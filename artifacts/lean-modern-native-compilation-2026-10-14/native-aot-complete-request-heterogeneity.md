# Complete-source reference latency heterogeneity

Observed 2026-10-14T23:54:16.361477+00:00

All29750 terminal nativeAOT reference requests, preserving all original outcomes. This reuses complete raw source responses and does not start another performance experiment.

| Native outcome | Sources | Median request s | p95 s | p99 s | Max s |
|---|---:|---:|---:|---:|---:|
|complete|27319|0.399016|3.323858|11.421045|272.692000|
|operational|55|300.015060|300.024999|300.027655|304.426355|
|rejected|2376|0.173162|1.853512|4.321189|68.003677|

Completed operational outcomes consist of41 stock300s timeouts and14 generic decoder errors. Only originalProof2269 has a directly confirmed native out-of-memory cause; no blanket cause is assigned.

The55operational requests are0.185% of the population. Their overlapping request-duration sum is12485.747s of42085.462s across allrequests (29.67% of that summed client duration). This is neither a CPU share nor a decomposition of the10531.819s whole clock. Per-request times overlap under four outstanding requests; no Amdahl bound or whole speedup follows from this concentration.

Actual source inspection of slow successful cases finds both nonlinear arithmetic (Proof05612/29123) and large case enumeration (Proof06484/18147), as well as linear arithmetic after polynomial simplification (Proof26303). Tactic presence alone is not measured stage cost. The slowest successful request is272.692s; full reference sourceIDs and original author metadata remain in the raw analysis.

The publisher records180s timeouts for several of these sources, while this established service uses300s. Published author outcomes/times therefore remain metadata, not matched speed baselines or a generator arrival trace. The source population is unchanged; no hard source is removed to improve the reported throughput.

Decision impact: reject extrapolation from the four-source product-reuse pilot to the whole verifier. Use measured whole-population results plus source-native stage/certificate evidence to select the next mechanism. The existing CPU and device frontier and allfour RQs remain open.

[Raw complete-source analysis](native-aot-complete-request-heterogeneity.json). Root direct interpretation, not independent audit.
