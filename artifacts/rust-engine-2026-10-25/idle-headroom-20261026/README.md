# Idle prepared memory must not strand a large forecast

Root-only implementation/self-review,2026-10-26. No native local acquisition.

## Reproduced defect

With actual resident memory20,budget100 and forecast90,the old engine waits
forever:90is below100,so not exclusive,but20+90cannot satisfy headroom.
There is no active peer that can retire to make the reservation fit.
The new regression first executes the fitting case,then fails on this case
with the5stest bound and Cargo101 on unchanged production source484fd57.
These are toy resource units and a fake verifier,not a native memory benchmark.
An initial Python wrapper syntax error launched no test/build;its source and
repair note remain in the step directory. It is distinct from the real defect.

## Repair and contract

If no attempt is active and the forecast cannot fit actual idle headroom,
admit it exclusively under the existing actualRSS policy. A forecast at/above
the total budget follows the same exclusive path. Neither predicted oversize
nor past resource failure is logical rejection. The existing backend resource
hook reclaims idle preparation and runs fresh verification under the same
deadline;initial exclusive headroom now uses it even without a previous attempt.

CPU allocation,watchdog,real-RSS admission,queue/cancel/cache semantics,timeout
and schemas are unchanged. Backend implementers overriding the0.1resource
hook must support an initial call after peers retire. An explicit exclusive
headroom event records forecast,actualRSS andbudget;Attempt.exclusive does
not imply a prior failure. Ordinary fitting forecasts keep ordinary execution.

## Validation and limits

[Run index](validation-index.json) retains actual failure and both successful
ordinary validation runs. fmt,Clippy,49tests,warning-free docs and CLIhelp pass.
Four native tests compile but are deliberately ignored locally while the old
sole fullpair runs. Final combined own/full sampledRSS50,051,530,752Bunder
51,539,607,552B;0pressure/monitor errors.1s sampling is not a kernel quota.
Both success runs are retained because the second also compiles the strengthened
native CI fixture. Debug builds never replace the live release or native host.

The fixture matrix covers normal headroom,below-total-budget shortage,total/
above-total forecasts,and actualRSSalready over budget. Over-budget actual
RSS makes no backend call. Forecast oversize gets one accepted fixture attempt,
not a fabricated failure/rejection. This proves the modeled admission boundary,
not real native accepted-set parity or speed.

The existing pinned-native prepared-parent CI case now reaches resource
reclamation through Engine rather than invoking the hook directly. A synthetic
forecast of budget-minus1byte forces the path without allocating that memory.
It checks one exclusive attempt,real parent retirement,fresh child retirement,
unchanged raw-native response and re-preparation on later ordinary work.
That source compiles locally;actual native CI execution follows publication.
No additional local candidate group or new workflow is created.

[Original fullpair observation](original-full-observation.json) confirms the
originalPID/birth and old release still run. Its eventual result belongs to
42659a8,not this fix. The code does not assert that the current capture hit
this defect or claim faster throughput. No resource primitive is novelty.
[Previous-step CI](previous-484fd57-ci.json) closes prior pending status only.
