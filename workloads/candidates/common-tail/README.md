# A common slow-tail metric, separate from budget exposure

Offline only; existing public-candidate native records, no verifier reruns.
Rank each point by its own measured candidate/request cost, then take
k=ceil(0.016*N). The ratio is sum(top-k costs)/sum(all costs), not budget-error
time. No hardware normalization or causal speedup comparison.

| Point | N / k | Slow-tail cost share |
|---|---:|---:|
| miniF2F historical physical attempts |7808/125|**at least72.677%**|
| ProofNet reps0/1/2 |5952/96|**33.554% /33.519% /33.591%**|
| AutoVerus reps0/1/2 |3566/58|**3.399% /3.338% /3.315%**|
| EPFL completed prefix |136/3|10.199%|
| APRIL selected mutations |39/1|6.820%|
| APRIL selected references |39/1|6.400%|

ProofNet's70budget-containing sources use11.57%of request time; its96slowest
requests use33.55%. These are different subsets/metrics. This supplements,
rather than overwrites, the [budget-exposure comparison](../cross-dataset-budget/).
miniF2F's unusually concentrated tail still does not generalize to AutoVerus.

## Exact results versus a proved lower bound

ProofNet recomputes all5,952retained elapsed_seconds from each original zip
and checks denominators against M's retained totals.
AutoVerus reuses its prior raw-process top58audit, same ceil convention.
EPFL uses the136actual completed requests; censored214 and missing returns
are not imputed. APRIL reuses39+39qualified runs, not the78startup failures.
These small selected points are descriptive, not population estimates;
ceil rounding gives3/136=2.206%and1/39=2.564%, shown in the CSV.

miniF2F's table entry is **a lower bound**, not the exact top125:
M's126distinct budget-source witnesses have per-source physical attempt sums.
Their125largest sum38,513.155589s. The true top125among all7,808sources
cannot sum less than any chosen125sources. Divide by the same retained
52,992.124106s whole-attempt denominator to obtain>=72.677131%.
Retries/preempted work are included per source; other points measure a single
request/process per source. Do not call this an exact or common-policy tail,
batch-wall ratio or intrinsic mathematical failure property.

Reproduce analyze_common_tail.py with --repo, --raw (PVC workloads capture
root) and --out. It reads only existing records and writes this small CSV.
No CIs or extrapolation from the small EPFL/APRIL selections are claimed.
