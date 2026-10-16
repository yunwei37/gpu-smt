# Independent review: cross-original-input exact LP reuse

Reviewed 2026-10-16. Scope: closed Fast/hybrid reference profile data, exact source association, and the screening decision for cross-original-input exact-query sharing. No native verifier/cache/GPU experiment, implementation change, OMP edit, active-capture inspection or Git operation was performed.

## Sources and independent checks

Read this node's analyze.executed.py, execution.json and analysis.json; source-map.jsonl.gz and qualified-query-rows.jsonl.gz; the earlier E032 full-integer query/group/source outputs; the actual server/split.py; the original ZIP/input/terminal; and artifacts/lean-modern-native-compilation-2026-10-14/analyze-oracle-reuse.py and run-product-application-full.py. The original full-integer census had root self-review, not an earlier independent audit.

Independently streamed all 502,329,013 uncompressed bytes / 173,941 lines of product-application-full1/goedel427-profile-fast.zip member goedel427-profile-fast/oracle.jsonl. Verified every parsed LP's trace line, source ID, original source text, outcome, start and elapsed against the old query rows and new qualified rows. The original archive's input.jsonl exactly equals the cited 29,750-row input file. No source, timestamp, outcome or ordinal-association mismatch found.

Independently regrouped all 62,197 parsed LPs from the original stream, rather than assuming old group IDs were audited. Used type-distinct integer lexical tokens (normalizing -0 to integer zero), exact Decimal values, and ordered dictionary/list representation, preserving every LP field, string/number distinction, coefficient digit and ordering without rounding, hypothesis/variable reorder, hashes or fuzzy identity. This avoids giant decimal-to-integer conversion while preserving the reader's structural identity semantics. All 30,898 group IDs agree, with zero mismatches. Also reviewed the old reader's type-tagged freeze implementation: it preserves ordered parsed structural identity, not mathematical equivalence.

All 28 malformed lines remain present in the original ZIP and identically listed by the old/new analyses: 17629,17630,21862,21863,71402,71403,77112,77114,81800,81801,87557,87558,108085,108086,108854,108855,113597,113598,115248,115249,117616,117617,126146,126147,136917,136918,147521,147522. They are excluded from parsed LP statistics with their errors retained, not silently repaired into synthetic queries. This is a complete scan of the closed stream, not proof that all executed oracle calls were logged.

## Exact original-input association

For all 29,750 original inputs, independently invoked actual server.split.split_snippet(original.code).body. Compared each distinct logged source to the entire resulting body string, without trimming or fuzzy matching. All 21,234 logged source texts match exactly one original input index; zero ambiguous, zero unmapped. Every published source-map record and each of 62,197 qualified rows' original_input_index agrees.

This resolves the prior zero full-code matches: the logger records the actual import-stripped body, not the entire original code. Only 21,234 original inputs appear in parsed LP records; this is not coverage of all original verification work, all Lean Meta queries, every input's execution, or a whole-program proof-reuse characterization. The current splitter file is not proven immutable since capture; exact body equality on the complete observed source population supports the association without that stronger provenance claim.

same_input means equal original input index. It does not mean equal solver invocation, process, branch lifetime, or an existing per-input cache. Distinct original IDs, rather than merely different textual spellings, define the cross-input comparison here.

## Independently recomputed completion predicates and partitions

Used a different algorithm from root's two-earliest-per-group optimization: built each exact group's full list of successful completion timestamps with original input IDs; then, for each timed successful query, explicitly tested every strictly earlier completion in that group for equal versus unequal original input ID. Completion = start_ns + elapsed_ns; prior means completion < this query's start_ns, not start-before-start or trace-file order. All elapsed intervals are nonnegative. Every published same/other flag and category agrees; zero classification mismatches.

| Partition | Calls | Sum logged call wall seconds |
|---|---:|---:|
| no prior successful completion | 29,848 | 1160.718469461 |
| same-input only | 3,536 | 3.240462267 |
| cross-input only | 18,519 | 275.541315451 |
| both same- and cross-input prior | 7,853 | 4.499676467 |
| non-success | 2,441 | 21.205239211 |
| Total parsed LP calls | 62,197 | 1465.205162857 |

There are 59,756 successful timed rows. The three prior-success partitions sum to 29,908 calls and 283.281454185 logged interval-seconds, matching the earlier census; the new split does not lose or manufacture repeats. The cross-input-only interval sum is 18.805647% of the parsed LP logged-call interval sum. Adding both-prior rows answers a different question (any prior other input), not an incremental benefit beyond a hypothetical per-input cache.

The earliest completion optimization is valid here: only an existence predicate is required, and retaining the earliest successful completion for each input, followed by the two earliest distinct-input entries per group, suffices to find an earliest other input. The independent full-list result confirms its application to all rows.

## Whole-clock provenance and scope

The denominator 13,346.049945904 seconds is the original same-profile terminal product-application-full1/goedel427-profile-fast.terminal.json: (534265315260023 - 520919265314119) / 1e9. It returned all 29,750 attempts, failure=null, counts 27,321 complete / 2,376 rejected / 53 operational, server_returncode=-15 under the recorded service shutdown protocol.

The original command is the native compiled Kimina service, four HTTP requests in flight, private port8008, recorded CPUs0-23 and stock resource/time settings. run-product-application-full.py sets its Fast flag on top of the hybrid arithmetic route. It does not set FARKAS_USE_PRODUCTS for method fast. This is the Fast/hybrid reference of that experiment, not its fast-products candidate and not E032's plain compiled-original perf profile.

275.541315451 / 13346.049945904 = 0.0206459077081 is a scale comparison against the same original whole clock, not a measured end-to-end speedup or a strict 2.0646% Amdahl ceiling. Call intervals can overlap, lie outside a removable critical path, include waiting, and do not represent CPU fractions. The observed stream has malformed records/possible omissions. No transfer to a different arithmetic composition, source population, service condition, CPU profile or GPU path is justified.

The existing execution.json records an approximately 11.29-second successful offline reanalysis and exit0. These are analysis costs, not native benchmark performance. This independent audit likewise only reads and recomputes closed data.

## Scientific disposition and paper decision

Hypothesis: cross-original-candidate exact LP sharing might offer materially more reusable work than repeats confined to an original input. The data establish that such observed timestamp-qualified repetition exists: 18,519 cross-input-only rows are the substantial incremental parsed-call subset, while both-prior and same-only interval sums are small in this trace. The initial source association uncertainty is resolved for this observed population.

They do not establish a working cache or savings. Success of the earlier oracle call is not success of its full Lean proof; a returned certificate still needs compatible use/repair/checking. The trace lacks a realized cache's publication delay, process/global scope, synchronization, transfer/serialization, lookup/invalidation costs, and certificate lifetime/compatibility behavior. Treating all same-input repeats as already removed by a baseline would invent an unimplemented cache. same-input is only a clearly labeled optimistic comparison for screening.

Paper impact: this is useful negative/limiting opportunity evidence and an exact reproducible characterization within one complete closed profile. It is not a new cache-system contribution, universal reuse bound, executed cache evaluation, or evidence that heterogeneous execution wins. The cross-only interval scale is too modest and the generic exact-cache mechanism too established to justify a new OSDI headline or immediate standalone cache implementation on this record alone. No new experiment or correctness campaign is requested by this review.

Next decision: preserve this result and do not promote this narrow exact-query cache route as the project's new main system solely because many calls repeat. Continue the original Lean-first verification acceleration objective and its larger paid-work/behavior/resource questions. This conclusion does not close all proof reuse, preparation-state sharing, broader mathematical equivalence, other workloads, GPU opportunities or any complete paper-level RQ.

Disposition: accept the source-association reanalysis and all reported partitions with the stated measurement limits. No blocking arithmetic, identity, source-population or timing-provenance discrepancy found.
