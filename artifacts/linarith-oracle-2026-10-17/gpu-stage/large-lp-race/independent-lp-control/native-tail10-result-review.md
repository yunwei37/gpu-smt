# Immediate GPU admission on the native-selected heavy ten

This is a purposefully inspected tail diagnosis, reviewed by the root thread.
The ten candidates are selected from the previously complete native 1,000-source
task-duration ranking, then kept in their original input order. They are not
fresh representative final evidence.

## Complete matched measurements

| Condition | Whole seconds |
| --- | ---: |
| Native compiled, upstream eight queues | 206.683302312 |
| CPU AST oracle | 173.262311239 |
| Immediate independently cancellable GPU oracle, warm server | 170.256469474 |
| Complete cold GPU lifecycle | 191.469171300 |

All ten sources complete in every condition, with identical source verdicts and
non-message native payloads. CPU and GPU each have the same one accepted-source
warning-only change. The warm GPU observation is 1.735% lower than CPU oracle;
charging its cold lifecycle makes it 10.508% slower. One selected tail
observation does not establish a stable GPU benefit. The four GPU sampler read
errors and omitted aggregate server memory prevent a resource benefit claim.

## Mechanism engagement

All processes share CPUs 8–11, at most eight candidate tasks, and the 48 GiB
address-space limit. One RTX 5090 is shared through the existing device plugin.
The server uses the declared eight-worker candidate. The real proxy startup
receipt confirms independent jobs and minimum-ready one.

There are six actual single-LP jobs, each admitted immediately. All six admission
groups contain one request, and client RPC peak is one. Therefore this tail
capture demonstrates neither cross-candidate batching nor simultaneous GPU work.
Three jobs return results, three are cancelled, all six retire and acknowledge
DeleteResult; the dispatcher has zero pending jobs. Returned jobs report 0.666
summed solve seconds. Cancelled device time remains unknown.

The 197 labelled races choose 194 CPU certificates, two CPU no-certificate
answers and one exactly repaired GPU certificate. Their summed overlapping
decision time is 6.287659498 seconds. This is neither a four-stage partition
nor the whole critical path of this ten-source observation. The earlier
source-37 proxy wait of 22.548 seconds is evidence of the old admission gate,
not a removable duration that can be assigned to this new clock. Do not join
earlier phase data to these new tail times.

Cold time includes 7.5214476 seconds to PodReady, 172.6437459 for the wrapper,
and 11.3020730 for retirement/restoration. The exact Job UID is deleted; lab
remains Ready and the other Workspace remains Running. All raw responses,
task timing, sampled resources, job events, native input and launch-source
snapshot are retained.

## Disposition

Immediate admission removes a concrete waiting condition, but this capture
does not establish useful batching or a stable complete-cost GPU advantage.
No full GPU variant matrix is admitted from it. This rejects neither all GPU
designs nor the paper's original four RQs. The user requires applicable
Amdahl opportunity evidence before negative GPU route closure.

A stronger native interface has now completed the full 1,000 sources in
685.730742286 seconds on CPUs 0–3, max eight candidates, versus the older
eight-item-wave reference of 1,237.370439599 seconds. Its matching CPU oracle
cell is still collecting. The earlier answer-aware 1.600x omission control
uses eight-item waves and cannot be divided into this new reference or treated
as a queue-protocol opportunity bound. Complete this stronger common CPU pair
before claiming any new representative heterogeneous gain.

All reviews are self-review. No independent audit or venue readiness is claimed.
