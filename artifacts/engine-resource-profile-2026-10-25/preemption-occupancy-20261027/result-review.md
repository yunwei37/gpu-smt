# Preemption occupancy in the completed native population

Root self-review,2026-10-27. All7852physical native PID/births match exactly
one original register/retire event from frozen1f38be7native7808;no missing,
duplicate or negative endpoint is filled. Own whole-cell28391.984735s.

|Group|Candidates /attempts|UTC interval union,s|Overlapping UTC sum,s|
|---|---:|---:|---:|
|All native|7808 /7852|28384.410514|77857.222851|
|Preempted nonexclusive|44 /44|3514.045098|5559.943135|
|Exclusive retry|44 /44|9479.735897|9479.735897|
|Ultimately resource failed|41 /82|11301.664092|13347.562129|

Preempted nonexclusive spans occupy12.376891%of the reference whole clock;
exclusive retry spans33.388775%. The44same candidates eventually return
41resource failures/3timeouts,zero checked success. The41resource failures
each have two attempts. These are occupied intervals,not saved wall time:
nonexclusive spans overlap useful peers,and changed scheduling can change
actual cost/contention. No1/(1-share)Amdahl ceiling or forecast gain is computed.

Monotonic native attempt sums have different scope:preempted nonexclusive
5560.318233s,exclusive9480.134700s,all77928.908684s. Registration omits work
before association/after ownership release and usesUTC,not the native monotonic
timer. These are not interchangeable denominators or disjoint CPU partitions.

Measured-sibling feedback may avoid repeated initial work or overreserve
heterogeneous siblings. It must not predict rejection from memory. Current
acquire source lines503–540routes oversized forecasts to an actual exclusive
attempt,not predicted rejection. Real32performance/accepted sets remain
unmeasured until both live cells complete;no prefix conclusion is drawn.

Analysis briefly usesCPU11while the sole native group runs;retain this as
possible shared-host contention for32timings. Completed canonical rawdata are
unchanged. Run python3 analyze.py to reproduce analysis.json.
Run status:complete existing-data analysis;value:supporting interpretation,
not contribution or independent audit. AllfourRQs/directions remain open.
