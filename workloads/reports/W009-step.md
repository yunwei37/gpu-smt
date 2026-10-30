# W009: audit a newly public code-verification workload
## EXPERIMENT
Offline audit while no second W Lean can run.
MetaLKV pinned129e65b has173files,12Lean/189413B,90released KIR fixtures/
481125B. Full tree and all90JSON parsed,not generated. MIT;Lean4.34.0 core/Std.
The fixture set adds finite GPU-kernel semantics beyond mathematical proofs.
## WRITE
Small source/asset/fixture CSVs and README in workloads/lean-kernel-verify.
Distinguish checker counterexample FAIL from compiler failure; full public
frontend unavailable at pin. Native costs,axiom closure and timing-tail
concentration unknown. No borrowed upstream example costs.
## REVIEW
Same-thread self-review. Released fixtures,not a public failed-candidate stream.
No new native invocation,no candidate generation,Mathlib build or GPU use.
Native4.34.1 not substituted for4.34.0. Existing blocked W child retained;
this static audit does not resolve that fault or establish acceleration.
