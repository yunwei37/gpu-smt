# Runtime-configuration sensitivity of two EPFL wall-outs

Same two original sources,Lean4.15/Mathlib9837,10000HB,M6144,self-wall15s.
Worker configuration changed jointly:CLI-j1/LEAN_NUM_THREADS=1 to-j2/env2.
The old native fixture remains charged. All new controlled invocations retired.

j1:both reach15s wall with only~2.1CPU seconds.
j2:both return native heartbeat diagnostics at13.69/13.73s,with~13.7CPU seconds;
no wall alarm. Neither passes. This is observed progress/failure-class
sensitivity,not a proved deadlock root cause,acceptance regression or speedup.
One j2source also emits unsolved goals before the budget diagnostic.
Operational and native-budget errors can coexist;raw output is preserved.

This small nonrandomized contrast does not identify theCLI flag independently
of its matching environment setting,or resolve the still-running58969 case.
Runtime configuration must accompany any diagnostic/budget-cache provenance;
logical-goal text and budget alone are not this entire operational context.
No stronger replay eligibility or determinism claim follows.
Raw:.../gpu-smt-captures/workloads/epfl-search-threads2 and pending-v3.
