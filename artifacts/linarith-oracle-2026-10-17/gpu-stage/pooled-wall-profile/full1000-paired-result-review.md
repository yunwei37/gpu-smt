# Complete strongest pooled-family paired wall profile — root self-review

## Completion and comparison boundary
Both original1000source cells are complete: pooled native1245.961262403s,CPU AST-oracle1072.374382485s;992complete/8rejected/zerooperational in each. CPU0–3,width8,48GiB; original candidate order,8item waves, same corrected family-only imports and existing numerical-handle pool. Every native response JSON equals its corresponding noninstrumented primary exactly. Native/CPU-oracle differ in the previously documented88warning-only messages. These diagnostic clocks are not substituted into the primary1237.37/1037.85/1020.12s performance table.

Every native13230call and CPU-oracle10251call is source/invocation-labelled and has complete shape/product metadata. No unmatched calls or ambiguous source groups; all numerical workers have EOF/wait4receipts. Native12590certificates/640failures; CPU direct3597checked/605no-certificate-or-error, fallback5440certificates/609failures. Failed branches are included, not inferred from the old151second successful-only sample.

## Requested four native regions
| Observed native arithmetic region | CPU seconds | Interval-union wall seconds | Occupancy / own whole |
|---|---:|---:|---:|
| Hypothesis preprocessing/linearization | 234.053346267 | 269.143410453 | 21.6013% |
| Nonlinear product proof construction | 201.970219971 | 222.678455342 | 17.8720% |
| Exported numeric FP+exact LP search | 857.342589814 | 600.017430350 | 48.1570% |
| Lean certificate construction/checking | 197.153765158 | 230.838293196 | 18.5269% |

These are measured region occupancies across concurrent calls, not four disjoint portions of end-to-end wall; they overlap and do not sum to100%. Other parsing, export, kernel/frontend, observer and retirement work remains in whole. Ring/defeq/typeclass costs remain inside the appropriate Lean preprocessing/linearization/product/proof regions. The native product timer includes constructing Lean proofs and cannot all be called GPU arithmetic. The CPU-oracle's pre-query unsupported/export work is not an exhaustively instrumented four-way wall partition.

## CPU numerical service, including failure
Direct numeric service212.732021448CPU seconds; fallback339.306086398s. Search totals28.244493236FP+515.885945754exactLP=544.130438990CPU seconds. Numeric products3.114414867s,linearization0.307652706s,matrixpack0.650455466s,LPbuild0.493194265s,parse2.320531280s,exactrepair0.259213114s,exactverify0.040324830s,responsepack0.055542066s,responsewrite0.064362814s,dispatch remainder0.601977448s. Complete startup/read/diagnostic-write/exit accounting remains in each wait4worker ledger.

Among failures,605direct no-certificate/error attempts consume3.906473632FP+72.412503832exactCPU seconds;609fallback failures consume2.377535034FP+41.646325230exactCPU seconds. The failed numeric work is retained alongside successful direct and fallback paths. These CPU totals do not sum into whole wall or imply GPU-device time.

## Applicable Amdahl sensitivity
All exported numeric LP plus numeric products sum to607.389419503seconds of invocation wall, or56.63968%of the CPU-oracle own clock. With all other work/certificates/fallback choices fixed, subtracting the entire overlapping sum leaves464.984962982seconds; its paired native reference divided by that residual gives2.679573237x. This is a deliberately optimistic fixed-work sensitivity, not achieved GPU speedup, disjoint time saving or a universal scheduler theorem.

The exported numeric interval union is439.539173307s,40.98747%of CPU-oracle elapsed. Union measures occupancy and cannot simply be called removable critical-path work. Including the two native internal LP invocations as free gives the still more generous610.402192891s sum and2.697048200x relative to the same paired native clock. Removing all native product proof construction too is outside the present GPU guarantee. Neither calculation proves a below1.5x ceiling. Therefore GPU route/hourly automation remain open.

The earlier1774.24/1342.06width4profile and historical2234.69primary have their own clocks. None is rescaled to this pair. The complete noninstrumented current comparison stays1.21296xGPUwarm/1.19408xcold vs its own1237.37snative reference.

## Shape, batching and heavy tails
Exact row/column/nnz/product-count distributions are retained in full1000-paired-wall-summary.json. Native row median10,p99187,max888; columns median20,p99557,max3160; nnz median74,p994679,max26044; generated-proof product columns median14,p99524,max3081. Direct and fallback distributions remain separate. The row11gate removes7201calls using only0.021079925numericLP CPU seconds from this native capture, without changing the earlier gate choice.

Native exported-call concurrency median1,p99=5,max8;CPU-oracle median1,p99=4,max6. Native time with≥2outstanding client calls247.790139713s;CPU-oracle131.229418762s. These include export/queue work and do not establish GPU-ready overlap or a scheduler-independent upper bound.

The summary retains each method's actual source1%/10%selection and native-selected cross-method component tables with exact proofIDs. Component sums overlap; native-selected1%LP exactCPU78.51677s is smaller than its preprocessing108.25373s. Heavy-tail whole-task/region costs are retained, not replaced by a whole-population mean.

## Result review and next action
Run status: valid,complete paired diagnostic.
Tested hypothesis: nontrivial numerical work exists; a below1.5x opportunity ceiling is not established.
Research value: supporting the decisive RQ4 heterogeneous opportunity decision.
Paper impact: additional current-family evidence; no new-system novelty or fullRQanswer.
Next: the qualified fixed-coefficient omission control now runs with a fresh actual native reference onCPU0–3, using complete same-cohort recorded answers (16015unique keys,zero conflicts). It is excluded from best-valid CPU/GPU continuation results. Separately, upstream native8queue submission is in real24source CPU qualification on8–11 to test the collector-created wave barrier; no new GPU algorithm or unqualified full variant matrix is admitted.
Root alone performs implementation/analysis/self-review; no independent-audit orOSDIacceptance claim.
