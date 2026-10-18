# Full original-1,000 pooled native / CPU oracle result — root self-review

Observed 2026-10-18, owning gpu-smt-dev Workspace. The root alone executed and reviewed this work. This is self-review, not independent audit.

## Admission and execution
RQ4 heterogeneous execution remains open. The comparison uses the fixed original 1,000 arithmetic-heavy sources, original order, corrected family-only headers, upstream 48 GiB address-space allowance, width 8 and the same four CPUs 0–3. Methods run sequentially; both include preparation, queueing, native work, fallback, observer and normal retirement. The pooled native reference imports BatchBaseline and uses the original pinned hybrid CPU oracle through independently reusable native daemon handles; it does not use the AST oracle. The CPU candidate imports BatchOracle with the same pooled protocol. This stronger reference supersedes the serial-native reference for the pending width-8 GPU comparison.

## Complete outcome
| Method | Whole seconds | Reference / method | Complete / rejected / operational |
|---|---:|---:|---|
| Pooled native | 1237.370439599 | 1 | 992 / 8 / 0 |
| CPU AST oracle | 1037.849203905 | 1.192244919 | 992 / 8 / 0 |

Every source verdict and non-message native JSON field agrees. There are 88 warning-only source response changes. Actual task spans cover all 1,000 sources in each cell. Peak sampled PSS is 10.318 and 9.446 GB respectively; sampling has zero read errors. Full raw native JSON, resource samples, task spans, collector receipts and source identities are retained here. See paired-analysis.json for the slowest 1% and 10%, selected separately on each method and compared on the same identities. Their overlapping task-span sums are not whole-cohort elapsed or removable critical-path costs.

The separately closed serial-native control takes 1600.626538715 seconds with 992/8/0. Comparing against that weaker reference would overstate the oracle effect; it is not the primary denominator.

## Interpretation and limitations
This is one full paired observation on the stronger pooled reference, not three replicated pairs and not a GPU result. It does not meet the more-than-1.5x continuation target. Historical 1.34668x and corrected serial-family 1.29560x belong to their own protocol epochs and are not pooled with this result. The GPU cell follows sequentially on the identical source cohort, candidate width and CPU eligibility; no project closure is justified while that cell runs.

The completed width-4 phase diagnostic has its own native clock of 1774.239197591 seconds. Its conditional 1.93412x LP-only zero-cost sensitivity does not exclude 1.5x for that profile. It cannot be rescaled to this faster width-8 pooled-native denominator. A claim that the strongest pooled baseline excludes 1.5x requires its own applicable cost evidence; none is asserted here.

## Collection self-review
An initial archive analysis noticed that pathlib recursive traversal did not descend the separate 24-source qualification's reused-reference symlink. That reference was copied from its actual resolved source and analysis rerun; no numeric result or source response was synthesized. This full comparison's two cells are actual directories and were unaffected. GPU and other active collectors were not interrupted.
