# Complete7,808candidate scheduling matrix — root self-review

All three cells and group exit0 completed at2026-10-25T21:53:37.717196UTC.
Terminal first collected on2026-10-26UTC;original timestamps are preserved.

Complete consumer clocks:
* All:21,746.811713538s.
* Original-order first-success:15,385.386817670s,1.413471885449x,
  29.252218577%less elapsed.
* Source-size first-success:15,112.118703443s,1.439031292719x,
  30.508807900%less elapsed.

Both policies preserve exactly142solved problem IDs out of244. Original-order
executes3,631/cancels4,177;source-size executes3,724/cancels4,084. Every queued
cancellation references an actually checked same-task winner and no returned
native result. Actual executed HTTP codebytes match original source once each.
This is pass@k,not every-candidate RL rewards. Ordinary cancellation/source-size
ordering is not a novelty claim.

Source-size returns142valid,3,484Lean errors,66timeouts,32resource failures.
All32contain native std::bad_alloc under old24GiB-AS. Their rawbodytime0is
unavailable cost,notfree. minif2f-7231changes from paired all-cellbad_alloc to
timeout;every other executed status matches. This is an operational change,
not accepted-task divergence. Full ID,error,HTTP,process,event,RSS records remain.

Memory peaks(all/original/size):50,313,207,808/42,856,058,880/43,824,566,272B.
Each max2REPLs,0watchdogkills/errors,0live descendants after shutdown.
All15,105third-cell memory samples recomputed;sampling is not kernel-hardRSS.
Old2worker/24GiB-AS/CPU8–11/48GiBsampled point is distinct from the next dynamic
four-worker point. Single sequential captures/shared host and own controls
preclude isolated replicatedconfidence. The small ordering-policy difference
is not causal proof of predictor quality.

Full planned matrix complete;four research directions/RQs remain open.
Next user order:dynamic48GiB four-worker native/Mathlib-derived whole-population
pair,then actual lean-mlirbv_decide. Original42exclusive reruns remain a fixed
separate cohort. Original23simp/48interval runtime attribution is still pending;
qualified observers are not reliable failure certificates. Rootself-review,
not independent audit. Frozen CPUoracle/closed-tail paths not extended.
