# Comparison-alias native build — root self-review

The previously committed exporter supports native GT.gt and GE.ge by
swapping operands of LT.lt and LE.le. Its original full observation did not
contain this source repair; no historical coverage is relabelled.

This fresh build completes both Lean modules and native linking with exit0,
from 2026-10-24T05:39:47.238756+00:00 to 2026-10-24T05:39:56.648861+00:00. Sources, commands, compiler
logs and native products are retained here. Two existing deprecation warnings
do not affect the successful build. No verification REPL is started.

Outputs live in /tmp/gpu-smt-counterexample-next-20261024, separate from the active observation's frozen
/tmp/gpu-smt-counterexample-20261023. The canonical build receipt selects only
future runs. The active collector already retained its own source receipt,
loaded old binaries and fixed worker paths; none are replaced.

The sampled joint watchdog covers compiler descendants and the original
capture PID255332/birth124305929. Nine samples see at most two actual REPLs,
peak combined RSS 12788453376bytes
(11.910GiB), no kills or monitor errors.
Compiler address space is24GiB and the same four CPU cores are used.
This is a sampled build/coexecution window, not an isolated performance run.

Disposition: native compilation is complete; runtime qualification of the
alias repair, own off/on proof outcomes and performance remain pending.
The full observation retains its original source/version and all limitations.
No external method, subagent or independent audit was used.
