# Original-file native contract — root self-review

Published ad7ecdc passes existing engine and benchmark-smoke workflows. Pinned
Lean4.18/REPL CI actually executes all4 native contracts. The source frontend test
now includes raw same-file versus original-file backend checks for both accepted
and rejected Init proofs with --tstack=400000, in addition to existing default/
configured stdin and interruption/retirement checks. Raw responses match within
each same-context pair and the test checks file bytes remain unchanged.

[Exact-head receipt](receipt.json) and [actual job log](native-contract.log.gz)
support this claim. This is no longer just compile/ignored local evidence.
CI runs in the existing declared native workflow, not another research group
in the owning Workspace. No nightly lean-mlir module or SAT workload executes.
No full accepted population, reliable detector, throughput or novelty is proven.
Root self-review is not independent audit.
