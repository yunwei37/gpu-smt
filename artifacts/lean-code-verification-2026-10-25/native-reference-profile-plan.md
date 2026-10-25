# Verina native reference timing

The user requests continuous work on code-verification loads alongside
earlyfailure and first-success scheduling. Use official Verina66b3ce5,
original189task.lean files, Lean4.18.0/11ccbced7964 and Mathlibaa936c36;
retain reference stubs/admissions, not just46apparently complete source files.
The pinned SDK and6,471cached library files are prepared in owning-Workspace
temporary storage. No new persistent service or alternate Workspace.

Run native then builtin-profiler/trace on the same files, two CLI workers,
CPU8–11,24GiBAS each and48GiBaggregate sampled RSS. Default120s comes from
the official synchronous Verina checker, not a new project timeout tuning.
Direct native invocation reuses the exact prepared package search path;
the author's model-generation/evaluation system is not reproduced.
Source text is untouched; profile flags are a declared diagnostic change.
Record own import/frontend/tactic/checking/cleanup times, warnings, admission
tokens, native exit codes, resource failures and missing killed traces.
Profiler100ms/trace10msdefaults and prettyprinting overhead remain explicit.
Never label Firefox synthetic threadCPUDelta as sampled CPU or convert
nested/concurrent spans to a removable whole wall share.

First run basic1/basic2/advanced1 native/profile as real integration
qualification, then all189references. Both wait only for the user's one-group
resource invariant; no performance admission condition, deadline or closure.
Actual components depend on native executed calls: bv_decide/grind are absent
from this4.18source set and are pursued separately in real lean-mlir pins.
Source token preparation is not dynamic measurement or proof completion.

Runner implements process-group retirement on timeout/cancellation and keeps
every source/log/result. Builtin profiler summaries and trace outputs will be
interpreted after actual qualification, not with guessed log formats.
All code/review remains this thread's work and self-review.
