# Questions for the author

The root chooses research direction and implementation directly; no delegated
author is running. All four RQs, Lean-first/RTX5090 and OSDI-quality target remain.

## Temporary miniF2F native-memory budget
Question sent2026-10-14: approve8GiB native-process budget uniformly for CPU/GPU
methods in this temporary benchmark, record resource exhaustion on original
inputs, rerun affected comparisons and restore unlimited default after testing?
Why: actual native warm source663 allocated95GiB and triggered host global OOM.
Default action: no cap or blind mini retry; preserve failed/partial evidence and
continue native hotspot attribution on complete ProofNet.
Authority: spark-manage AGENTS.md section2.3/8, exact new runtime cap approval.
No answer yet; elapsed time is not authorization. Revisit when the human responds
or a source-grounded repair avoids the allocation without changing the budget.
