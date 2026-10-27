# Result self-review — inputs complete;release interrupted

The fixed selection produces32byte-preserved original Candidate records at
48GiB/CPU8–11/onecoreperworker,modeall,reusefalse/300s. Heavy tasks are
amc12a_2020_p4 and mathd_numbertheory_483 (29and9prior full-task resource failures).
Ordinary controls are aime_1983_p2 and aime_1989_p8. Taking first8per task and
restoring original order yields16prioraccepted,7priorrejected and9priorresource
failures;all9resource sources had preemption. No unknown observed peaks.
This is outcome-informed development input,not blind/full-population evidence.

Selected prior attempts sum2906.130923099elapsed seconds under concurrency.
That is neither a future wall time nor a removable-work/speedup/Amdahl bound.
The exact prior attempt histories remain. Intrinsic solo-budget failure is not
corrected by TaskMemory;the method hypothesis concerns redundant preemption
and admission cost,including overreservation. No future native verdict is
injected and no selected candidate runs in this preparation.

Preparation completes1.003490s with3combined own-tree samples,peak3,929,231,360B,
no monitor error or abort. Reused runner's inherited rust_support_test_only
label is inaccurate for this cell;scope-note and actual command explicitly
identify offline input preparation,not Rust testing. Raw receipt is preserved.

A subsequent real release build of source596a6a2 starts only after verifying
tracked build inputs clean and active executable is the separate frozen
resource_pair copy. At51.146246s,the combined1smonitor samples51,890,610,176B
(48.326897GiB),over51,539,607,552B,and kills only the new compiler group(exit-9).
No monitor error. Sampling is not a hard cap. OriginalPID457460/birth150297500
remains alive with no native terminal after containment;it is not restarted.
Retain partial build/logs. No release executable is frozen or qualified,and
no retry competes with the active capture. This interruption is not a compile
correctness failure and does not establish that all processes stayed below48GiB.

Existing hostedCI for596a6a2 is actually complete:engine run40457363047,rust job
122033703766,native job122033703651 and benchmark40457363062 succeed. Selected
exact test-step logs retain the changed CLI case and4actual native functions
with0ignored. This closes prior CI evidence,but does not rescue the interrupted
local release or measure original4.9throughput. Root self-review only.
