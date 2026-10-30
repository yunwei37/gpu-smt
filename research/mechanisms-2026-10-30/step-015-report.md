# Step015 — correct observer timing and whole-group deadline accounting

2026-10-30UTC;M;self-review.

EXPERIMENT entry:363851c preserves the initial successful sampled digits
point and explicit NS-window erratum. Move the stop timestamp immediately
after addDeclCore returns,before HB logging,sampler shutdown or msync.
The mathematical declarations region is byte-for-byte unchanged from the
proved DigitsCertificate.lean. Revalidate stock/off/on at a new named point
without overwriting the first data. Native per-cell bound180s; serial M
within16GiB,8cores. Actual completion metrics follow the terminal receipt.

Forward controller correction and five offline remaining-budget controls
are recorded in collection-budget-erratum.md. Prior six-cell total exceeds
30minutes; no claim that per-cell limits make it compliant.

EXPERIMENT completion:corrected pointpc-digits-pure-timing returns3/3,
all exit0 and retired. Pure return-bracket wall8.645867747s(stock),
8.679850596s(off),8.516724790s(on). Non-timing stdout/axioms identical;
recheck rawHB57844573 in every cell. The extra clock read now lies inside
the HB measurement scope,so these counters are not equated to the old
57844572 scope. Maximum sampled own RSS2402803712bytes (~2.24GiB).
No failure or sampled overbudget event.

WRITE:pc-digits-pure-timing-result.json keeps new receipts,clock values and
4258 CPU samples.0 IR;699explicit RC(16.42%);462allocation/free(10.85%);
777named table(18.25%);124unresolved(2.91%). These are residence lower
bounds,not PMU cycles or complete algorithm costs. Snapshot is one ordered
pass,not causal sampler-overhead evidence. Whole source execution includes
the original theorem construction plus this explicit second kernel check.

REVIEW:mathematical declaration region unchanged from original proved
prototype. Source/result/capture of the earlier post-flush timing window
retained; no silent replacement. Pure stop timestamp precedes diagnostics,
shutdown and flushing. Full native matrix and all later native groups have
retired; no active M collection left. Prior group-budget overrun remains
an explicit deviation,not retrospective compliance. No old data erased.
