# Complete two-sided CPU oracle comparison — root self-review

Observed 2026-10-18, completed 10:58:26Z. Frozen source-qualified implementation
from 6bc7199; no implementation or numeric-service mutation during capture.

| Same 1,000 candidates | Whole seconds | Native / candidate |
|---|---:|---:|
| Original compiled native hybrid | 681.243556612 | 1 |
| Positive certificates only, CPU HiGHS | 472.085856153 | 1.443050131 |
| Positive and negative certificates, CPU HiGHS | 453.509810469 | 1.502158368 |

All cells retain 992 complete, 8 rejected, zero operational results. Every
proof_id, verdict and non-message native JSON field matches its fresh native
reference. Both oracle cells have the same 104 message-only differences.
All 1,000 task spans map uniquely. The two-sided cell reuses this fresh native
cell, not a denominator from an older family. Cells ran native, success-only,
two-sided, sequentially with CPU0–3, eight original contiguous native queues,
48 GiB and the same Lean/Mathlib/heartbeat setup. Proxy preparation, complete
native return, EOF and worker/proxy retirement are included. This is a CPU
result; it contains no device execution.

The 1.502158368x observation exceeds 1.5 by just
0.652560606 candidate seconds (threshold 454.162371075s).
It is not replicated evidence of a stable threshold crossing. The previous
success-only full observation was 1.494245739x, and the current success-only
repeat is 1.443050131x. Shared background and fixed acquisition order remain.
A reversed-order, unchanged two-sided/native repeat is the next decisive
experiment; no unprofitable full GPU matrix is admitted.

## Mechanism and costs

Of 1,888 two-sided races, 334 end with an exact-verified external infeasibility
certificate, 400 with an exact-repaired external positive certificate,
274 with CPU positive and 880 with CPU no-certificate. The legacy winner name
gpu means the external **CPU HiGHS** worker in this cell. The parent checks
negative certificates with original BigInt data and kills/reaps the losing
CPU child; it does not trust floating-point infeasibility.

Summed negative CPU decision time falls from 181.975656482s for 1,214 decisions
to 56.738566399s for 880 decisions, plus 15.134823761s for 334 external negative
decisions. This is cumulative concurrent process/coordination/repair time,
not a subtraction from cell elapsed time. HiGHS returns 479 dual rays, of which
334 races are won by the exact-verified negative path. Failed reconstruction
keeps exact fallback. LP call wall sum rises from 6.066718578s to 9.166370869s
because obtaining rays also costs work; matrix building sums
0.676897993/0.582239223s. Connections are 1,384/1,395 but only 930/942 parsed
LPs; interrupted JSON frames are not successful solves.

## Native-selected tails

For the native top 1%, summed overlapping task spans are 1009.477111645,
800.844791990 and 784.999635073s for native/success-only/two-sided.
Their occupied interval unions are 540.057210162, 417.203819399 and
406.792683806s. For native top 10%, corresponding sums are 2276.937748892,
1536.822764415 and 1471.754802413s, with unions 646.686643427,
449.427769366 and 432.387711768s. These overlapping observations do not
establish an isolated subset speedup or a removable critical path.
All indices and proof IDs are in the paired-analysis files.

## Limits and disposition

Resource observer read errors: native 0, success-only 147, two-sided 107.
Do not rank incomplete non-atomic memory peaks. This is one selected heavy
cohort, not all 29,750 candidates or the complete miniF2F/ProofNet service.
External proof certificates, exact infeasibility checking and batched GPU
simplex are established prior art. This local optimization does not establish
systems novelty or OSDI readiness. Self-review only; no independent reviewer.
Continue the research and unchanged hourly automation. Do not close the GPU
route: the applicable current all-call sensitivity has not excluded 1.5x.
Raw successful, failed and interrupted calls are retained losslessly.
