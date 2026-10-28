# Fresh native receipt deadline — root source review

Prior goal turn is concrete progress: exact-median source and tests/CI,
public status cleanup and push. The sole full7808 remains frozen13d4606 and
is healthy at verified controller/warm process births.

Finding: fresh NativeRepl selected IO versus a sleep timer without checking
the instant at which decoding completed. An IO poll that blocks in synchronous
decoding can finish after the deadline while the timer has not been polled
again. PreparedRepl already guards receipt time. This is a protocol contract
issue,not an explanation for a measured miniF2F timeout or a speedup.

The private request_io function retains IO/error/cancellation selection
and the relative response budget origin (after spawn/IO construction).
It checks the receipt instant before classifying a completed response. Late
JSON or decode errors become timeout. The same helper guards stock CLI IO
completion,whose existing operation waits for stdout plus natural child exit;
its later diagnostic classification boundary is not conflated with REPL JSON. Fully awaited kill/reap/stderr/ownership
retirement code is unchanged. No extra execution time is granted. Deadline
enforcement can change formerly late accepted outcomes; do not silently
substitute this version into the ongoing point or claim accepted-set equality
from unit tests.

The deterministic paused-clock control advances time during one IO poll,
without yielding before its ready result. It preserves the previous exact
selection as a negative control,then tests the fixed path. The installed
Tokio1.54.1 advance implementation updates time before its cooperative yield.
Only test-util is added as a dev feature; production settings/dependencies and
request fields do not change. Timing fixtures model scheduling,not Lean or
measured JSON cost. Actual pinned native/retirement controls remain required.

No local compilation or second native collection competes with the active
full pair. Existing source CI will execute the controls. Full result/paper
claims wait for actual matching workload evidence; this is dependency-only
resource/semantic maintenance,not scientific novelty.
