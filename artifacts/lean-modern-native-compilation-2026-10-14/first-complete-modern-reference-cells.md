# First complete modern CPU reference cells

Observed 2026-10-14T23:32:47.100447+00:00

These are two separate complete reference cells, not a paired speedup comparison. Offline analysis has finished; both terminal archives contain all29750 original source inputs and responses. NativeAOT source order/bytes/population checks pass. The corresponding native-oracle pair and CPU-solver trio are not complete.

| Reference | CPU eligibility | Whole seconds | Terminal attempts/s | Complete proofs | Rejected | Operational |
|---|---|---:|---:|---:|---:|---:|
| NativeAOT reference | 0–3 | 10531.819453 | 2.824773 | 27319 | 2376 | 55 |
| Native tiered reference | 4–7 | 9784.204512 | 3.040615 | 27320 | 2376 | 54 |

The reference cells use different affinity/background/order, so no ratio, CPUwinner, speedup, resource superiority or sole algorithm effect is computed between these rows. NativeAOT completes27319 proofs and tiered27320; the one-outcome aggregate difference does not identify which source or a mechanism cause. The complete paired native response/outcome comparison is pending.

Whole clocks include input persistence, server/import/library setup, source verification, HTTP/raw/logging/replacement and shutdown/EOF; ZIP follows the clock. Terminal attempts include every accepted/rejected/operational result and are not accepted-proof throughput. Request latency is the closed-loop service response, not an offered-load queueing result.

NativeAOT request latency: {"n": 29750, "median": 0.382627137, "p95": 3.263481473, "p99": 12.373437969}. Tiered request latency: {"median_request_s": 0.403146192, "p95_request_s": 2.676557127, "p99_request_s": 8.775767444}. Request durations overlap, so their sum cannot decompose the whole clock.

Original operational/default-memory/timeouts remain in full data. One actual decoder error was directly identified as native allocation failure; allothers are not assigned that cause without evidence. No source filtering, memory relaxation or live-code replacement is introduced.

Research decision: the acquisition path can produce complete producer-version/reference data; keep the paired candidate methods running. These reference results alone do not answer RQ4 or validate the selected-source product-reuse improvement across the corpus. No final paper numerical claim or independent audit is asserted.

Raw/recomputation: [NativeAOT analysis](native-oracle-complete-cells-analysis.json), [CPU oracle analysis](highs-native-cpu-complete-cells-analysis.json), terminal ZIPs in their originalrun directories. The six live Lean collectors plus the original SMT matrix remain owned by root direct execution; no delegated researcher.
