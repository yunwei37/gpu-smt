# Source-native8queue CPU qualification — root self-review
Same original24sources,width8,CPU8–11,48GiB and same private timing executable.

| Submission | Pooled native seconds | CPU AST-oracle seconds |
|---|---:|---:|
| Waves of8 | 30.483053785 | 27.222929571 |
| One upstream array,8sequential queues | 29.551738559 | 23.475818756 |

Every cell returns24complete with identical source verdict/non-message JSON; native responses unchanged,oracle2warning-message changes. Actual individual timing covers24sources each; peak timed candidates never exceeds8. Native queue sampler has6proc-read errors; no memory superiority claim. All references share the same source/binary and CPU eligibility. The source patch adds the already-existing candidateTimed wrapper to upstream sequential queue iteration only.

This qualifies stronger common submission, with3.06%native and13.76%oracle less elapsed on this one small set. It is not a full1000source speedup or a new batching contribution. The queue condition has no array-wide observation deadline; native retained heartbeat behavior and48GiB are unchanged. Therefore no timeout-equivalence claim is made outside this no-operational-failure arithmetic qualifier.

Next admit the matching GPU24qualification on the same8queues/4CPUs,exact row11eligibility andminimum2live-request batches, using the unchanged whole-LP CPU/GPU race. No new GPU LP algorithm,concurrency grid or fullmatrix follows without useful real qualification. Preserve the existing wave results and their exact scope. Root self-review,not independent audit.
