# E1063 — native queue scheduling as an RQ4 baseline confounder

2026-10-18, root thread only. EXPERIMENT_GATE, BOOTSTRAP/unfrozen.
RQ4 asks whether heterogeneous execution improves full verification against the
strongest measured CPU path. This is a baseline scheduling control, not new
verification mathematics, a proposed contribution, or the closed E038 runtime
branching route. No thread-count, buffer, allocator, solver or timeout grid.

Existing evidence comes first: third native 1,000-source capture has exact
interval joins, no same-lane overlap, eight maximum active candidates, 82.28%
candidate-slot occupancy and 74.96 seconds with only one active candidate.
A FIFO list-scheduling model with fixed observed durations predicts a 10.7%
shorter candidate window. Contention can change those durations: this is NOT
measured performance or an Amdahl bound. It could erase the narrow 1.50862x
aggregate arithmetic result, so leaving the confounder untested is consequential.

Use the existing native batch command/body, prepared state and resource limits.
A private copy of REPL.Main adds a dynamic batch mode: eight workers take
original-order commands from one FIFO counter; each command invokes the SAME
runCommandGCAux/timeout and candidateTimed and retains its original output slot.
Keep existing static mode in that same new binary as the matched control.
No edits to the active full29,750 collector, compiled tree or canonical proxy.
Build from recorded original Lean/clang/link trace commands and original imports;
only Main input/output and executable output change. All builds in owning WS.

Preflight original first64 of the frozen arithmetic-heavy1,000 in original order:
static native then dynamic native, width8, four CPUs4–7, 48GiB address space,
cores0. Include preparation, import, body, errors and EOF/reaping in whole time.
Require every ID/verdict/non-message field to agree, full timing coverage and
maximum active candidates <=8. Retain all messages, failures and observer errors.
No short-run ratio is a paper claim. If dynamic has no end-to-end benefit, close
this control without a fresh cohort or grid. If it benefits, qualify AST+dual on
the same dynamic interface, then admit one complete1,000-source native-static /
native-dynamic / AST-dual-dynamic component comparison. No full29,750 scheduling
matrix is automatically admitted. Numeric support/certificate checking unchanged.

Scope caveats: source-native thin scheduler glue does not replace external warm
server comparison or establish process-isolation safety. LeanTree already exposes
a warm ProcessPool service and save/restore APIs (official README inspected
https://github.com/Kripner/leantree); ordinary pools/scheduling are prior work.
No first-scheduler or novel-primitive claim. Current strongest CPU frontier and
all four RQs remain open. Existing full29,750 CPU0–3 and prefix20–23 continue.
Review is root self-review under user's no-delegation instruction.
