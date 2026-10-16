# Repaired-registry first full-trio service observation

Observed UTC: 2026-10-15T07:31:25.030535+00:00

This supporting EXPERIMENT node directly inspects the three closed rep0 receipts
and complete native service logs under
artifacts/autoverus-native-2026-10-09/experiment025/full-registry-repaired1.
All three retain the original 3,566-source order and CPU affinity 21–23.
Root performs this work directly; there is no delegated author or independent audit.

| Method | Whole observed seconds | Service evidence |
|---|---:|---|
| Stock | 1561.116914134007 | Complete receipt |
| Branch | 2124.1392411700217 | 2,789 terminal reuse requests; 473 parent preparations |
| Logical | 2306.2364935890073 | 2,789 terminal reuse requests; 473 parent preparations |

Both services record 2,790 online lookups: one stock-no-earlier-prefix route and
2,789 retained-native-branch routes. Each records 2,789 native terminal-kind 2
responses, 472 parent evictions, the final parent termination, and service
termination. The shared transport calls the route branch for either method;
the method argument remains distinct. These are service receipts rather than
independent native fork/translate-call counters.

The old logical baseline accepted only 473 reuse sessions and systematically
refused retained-parent hits. The repaired complete trio now establishes that
native reuse completes across the later requests. It does not by itself establish
full response/artifact identity, a causal fork/translation cost decomposition,
a replicated superiority result, a memory frontier, or any RQ closure.
The recorded whole clocks include the existing archival/acquisition boundary
and shared-machine interference; they are not pure solver timers.

The byte-comparison raw analyzer remains running through the original capture.
Its eventual result will be reviewed separately; no generic engagement boolean
is substituted for the concrete counters above. The full 12-condition matrix
and resource profiles remain incomplete. No live source/binary, data selection,
deadline, CPU allocation or acquisition process is changed by this observation.

Evidence: [recomputed receipt/log fields](smt-registry-first-trio-service-observation.json).
Original raw ZIPs, failed/older runs and their analyzer versions remain retained.
Continue the existing complete matrix and Lean paired acquisitions, without a
replacement writer, duplicate run, new microbenchmark or performance claim from
an unfinished pair.
