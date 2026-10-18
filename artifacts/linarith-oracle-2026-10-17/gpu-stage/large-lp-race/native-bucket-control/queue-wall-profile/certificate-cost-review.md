# Certificate features and Lean checking — root self-review

Reuse the complete native-queue diagnostic's CPU-oracle cell on its own
545.050104294sclock. This predates the HiGHS/two-sidedimplementation, so
the result does not attribute costs to the later453/447sprimarycells.

All4,202directroundtripsjoin4,202Lean checkrecords by source andcall_id.
605have no returned certificate;3,597return certificates and all3,597are
accepted by the native Lean reconstruction. There are zero missing joins.
Calling-thread CPU for all checks is172.613325395s, of which accepted
checks use172.600115165s. Accepted check wall intervals sum394.665682257s
and occupy a273.743885471sunion. They overlap across candidates and include
waiting/scheduling; neither sum nor union is removable critical-path time.

Accepted certificates contain a median4/p90 23/max84terms, median0/p90 19/
max74productterms, and median4/p90 61/max232provenance nodes.
Their coefficient-bit sums have median11/p90 111/max2,025.
Same-call checking-thread CPU has Spearman0.913withtermcount,
0.921withprovenancenodes and0.892withcoefficient-bit sum.
Median checkCPU0.014947258s, p90 0.130887300s,max0.489944979s.

This is evidence that certificate quality deserves examination as well as LP
search time. It does not prove that selecting a different feasible basis
improves wall time, predict the newer backend's performance, or admit a GPU
portfolio/parameter grid. Smaller support alone is not new systems work, and
existing native Fast support restriction is a necessary comparator.
The immediately decisive full component ablation keeps the same numerical
backend and restores the native proof-producing frontend; finish it before
crediting direct export with the whole CPU improvement.

Analyzer and per-call top costs are retained. Feature correlation is
observational, no causal/novelty claim; all review is root self-review.
