# Executed compiler-context native contract — root self-review

Exact source25debfc passed both existing engine and benchmark-smoke workflows.
The pinned Lean4.18/REPL native job actually executes all4 native contract tests,
including source frontend default proofs, interruption/retirement, and the newly
configured raw/engine --tstack=400000 accepted/rejected Init proof comparisons.
[Raw native job log](native-contract.log.gz) and [exact-head receipt](receipt.json)
retain executed status rather than treating local ignore/compile as execution.

Native job completed2026-10-26T01:28:19UTC. No additional owning-Workspace native
collection ran. The sole full resource pair remains version42659a8 and is not
rebuilt or restarted. These CI proofs use the pinned4.18 test context; they do
not execute lean-mlir's nightly source, provide SAT/LRAT attribution, or establish
full-population throughput/parity. The original7808 full-pair observation at
01:27:04UTC had1012 flushed physical native attempts and the same live owner
408739/start_ticks140695363; no prepared cell or terminal outcome was present.
No partial ratio or acceptance-set conclusion is inferred.

This review is performed by the implementing thread, not an independent audit.
