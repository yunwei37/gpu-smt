# Step0022 — compile original code-workload library prerequisites

## EXPERIMENT_GATE
Selection: direction3's original public Lean code workload, prerequisite stage.
Plan: experiment-001/plan.md. Plan self-review: experiment-001/plan-review.md.
EXPERIMENT node: real native source compilation with combined48GiB observation;
no candidate workload executions. Readiness and outcome must follow actual
terminal/logs, not process launch. Keep partial failures. RESULT_REVIEW remains
pending until the attempt retires; dependency setup cannot fill a performance
result slot.

## WRITE_GATE
Current paper, fixed four RQs and Initial Narrative remain unchanged. Update
workload preparation evidence only after native build returns. Full paper
writing refinement is not claimed for a dependency setup boundary.

## REVIEW_GATE
Root self-review only, recorded in outer-audit-report.md. Verify command exits,
pins, excluded workload root, cleanup and scope before committing a result.
No independent audit or complete paper milestone follows from this preparation.

## Actual result

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
