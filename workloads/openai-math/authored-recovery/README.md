# Two original-source dependency recoveries

LogProfiles and Frobenius previously exceeded the replay's100k HB point.
Exact source bytes, no CLI HB override, package autoImplicit=false,
Lean4.34.1/pinned Mathlib,8threads/M8192, self600s/group1400s:
both compile with no sorry. Walls7.93s/33.88s. Source option values are
recorded separately; native defaults and authored0 are not conflated.
The failed100k measurements remain intact. These are budget-point changes,
not fixes to proofs or evidence that budget-exceeded implies false.
Total native41.81s; capture50.06s;1Hz own-tree+old-stuck peak11.99GiB.
Artifacts .olean only, not full Lake build. Raw native/memory/exit records:
/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-authored-recovery.
