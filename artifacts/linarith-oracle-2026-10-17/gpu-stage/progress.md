# Current GPU oracle research frontier

Root thread only; main; RTX5090. Original4RQs/Lean+SMT/OSDI target and
better-valid-CPU/GPU1.5× selected-cohort criterion remain unchanged.
Historical pending descriptions are preserved in Git and
[the earlier archive](progress-before-20261023.md.gz), not current health.

## Complete current matched boundary

Original1000at source2/live2/24each/48aggregate sampledRSS/fourCPU8–11:
native1376.236473s,CPU769.116831s,GPU762.439983s. Native/CPU1.789372×,
native/GPU1.805042×; GPU cold797.608028s/native-over-cold1.725455×.
All992complete/8reject, matching verdict/nonmessage fields, CPU/GPUfullresponse
equality,108native warning differences retained. GPUonly0.87%lesselapsed than
CPU in one fixed-order observation, cold3.70%moreelapsed. No useful extra GPU
gain is established.488actualsingletonmodels,6positive/4exactnegativeGPUwins,
no true crosssource multi-model batches. Allraw/failures/tails/memory are
[closed and reproduced](../current-budget-gpu-20261023/full-result-review.md).
ProviderUIDdeleted, both experiment parents ended, no active fullqueue.

## Current opportunity and next action

The same-clock native diagnostic finds39.94sFP vs951.85sexactfallback and
225.61sproducts in its own1380.32s lifecycle. Concurrent sums/occupied unions
do not establish a strict Amdahlceiling. Current CPUHiGHSalready removes much
native fallback, so the1.8×selectedcohort improvement is not GPUcontribution.
[Native attribution](../native-stage-profile-20261022/reference-full-result-review.md).

The single-flight CUDA admission dependency is removed using existing
non-daemon worker/shutdown joins. Real first24×3 qualification preserves all
outcomes and resources, but GPU29.670819vsCPU25.757304s and seven singleton
cancelledmodels show no actual crosssource hardware/submission overlap.
[Closed dependency qualification](../current-budget-gpu-20261023/admission-async-20261024/result-review.md).
No further fullvariant is admitted from this result. No fullcollector remains
active. Select the next decisive mechanism using existingfullsource-owned
ready-work/race evidence rather than another kernel/solver/batch-wait grid.

## Scope that remains open

Whole29750CPUcomparison is1.106271× across three pairs with2outcomechanges,
not a fullpopulation1.5×transparentgain. Current miniF2FSHREDis1.30%slower
with changed outcomes. EarlierGPU/CPUvariantfailures remain retained, not
a broadGPUimpossibilityproof. No strict bound excludes the original criterion.
No narrowkernel/solvergrid, unsafe8worker queue, otheragent or scheduler.
All review is self-review; novelty/all4RQ answers and completepaper are open.
