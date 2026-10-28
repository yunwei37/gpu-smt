# Native IO deadline result — root self-review

Sourcee20dcaa uses one private completion guard for fresh REPL and stock-source
IO. It checks the completion instant as well as a cooperative timeout future.
Old code could accept a result from a single non-yielding IO poll after its
deadline. A paused-clock control with that exact old selection asserts the
late acceptance,then shows the corrected operation times out late successful,
rejected,incomplete and decoding-error fixtures. Clock engagement is asserted.
This is scheduling/protocol simulation,not a Lean benchmark or decode timing.

Actual engineCI40691001753 verifies68 workspace tests and5 separately
executed native differential/lifecycle controls,including source CLI. Format,
clippy and docs build pass;smoke40691002023 succeeds. Full raw logs are retained.

The response-phase budget origin/value and fully charged cleanup remain.
Synchronous parsing still cannot be interrupted;retirement still may extend
whole latency. The new guard can turn previously late acceptance into timeout;
fixture success is not whole-workload accepted-set parity. It has not been
inserted into the active full7808 point or claimed to explain2507/7230.
The added test-util feature is dev-only;production settings are unchanged.

The separately staged original42 input is exact and now has a future command
bound to the actual full point's13d4606 release. The original unexecuted record
is preserved. This is preparation only:the sole current full pair must finish
and undergo result review before42 starts. No other native cohort is launched.
