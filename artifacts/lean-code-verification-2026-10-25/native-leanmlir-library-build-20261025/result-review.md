# Library preparation result — root self-review

16 original library modules compiled successfully. The 17th attempted target,
LeanMLIR.Dialects.LLVM.Semantics, failed with unknown module prefix SSA. Its
unchanged source imports SSA.Projects.InstCombine.ForStd and LLVM.SimpSet.
The native header graph contains those edges, but filtering targets by package
discarded them. Library-only grouping was an incorrect preparation choice.

All native logs, dependency-check commands, partial outputs and memory samples
are retained. No original workload root was executed. Combined RSS peak and
sample count are in result.json; no memory-pressure event caused this failure.
Do not claim 37 modules ready or source proof failure: the package search
context was incomplete. Continue the mixed topological order under the original
root package/manifest, preserving its distinct dependency pins rather than
substituting the subproject manifest or stripping reverse imports.
