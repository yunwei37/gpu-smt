# Existing complete-capture attribution — self-review

Both7,808-source component cells are complete and their native responses/status
sets match each other,as previously recorded. They are not the warm baseline.
The exact historical warm cell is21693.761299439s,not a rounded reference from
another run. Prepared22891.507754520s is5.521156%longer descriptively,with different
AS/retry/clock conditions. Warm gives3014accepts;the engine gives3013. Six source
statuses differ:1885resource→timeout;2325/3209reject→backenderror;
2507/7230reject→timeout;3086accept→timeout. These differences are not hidden by
the equality of the two engine backends.

Largest prepared native occupied-time groups (OVERLAPPING,not additive):
* Final resource-failure sources:11242.055534s interval union,41sources/82attempts.
* Final timeouts:10650.161919s union,87sources/88attempts.
* Fresh-fallback attempts:9115.254031s union,62attempts.
* Exclusive attempts:8924.778203s union,42attempts.
* Rejected sources:6196.930914s union;accepted sources3320.479818s.
* Nonexclusive preempted attempts:2916.120179s union.
* Fourteen parent preparations,registration→handoff:31.365106s union.

The62fallbacks are42exclusive resource retries (8927.469733s overlapping attempt
sum),18import mismatches (2.277782s sum),two missing-retirement faults
(188.857940s sum). Fallback cost is largely the same exclusive checking,not a
second disjoint9115s tax. Preparation interval is readiness wall,not complete
import CPU. Registered child-count integration sees10375.984325s with one child
and11297.380866s with four;occupied-child slots are63.8440%of four-slot whole-cell
capacity. These are process-occupied intervals,not CPU utilization or all admission
causes. Measured sample histograms and CPU lower bounds are in analysis.json.

Historical warm42resource failures use3996.430801s accumulated HTTP envelopes;
its native300s allowance and24GiB-AS terminate different work than the new
uncapped exclusive attempts. Native warm83timeouts use24966.405942s accumulated
HTTP envelopes. Both sums overlap;they cannot be subtracted as saved wall.

31.37s parent readiness and external-minus-lifecycle1.314194s do not measure
in-execution observation/logging overhead. The retained structured driver is
35,804,683uncompressed bytes/98,595rows;byte count is not overhead time.
Within-native startup/import versus proof work and watchdog/logging CPU still
need matched controls. No made-up full disjoint breakdown or repaired gain.

Source inspection finds a real monitor defect:the persistent engine-root's
known-descendant vector retains dead PID/birth identities,so every admission and
watchdog sample revisits request history. Fix and regression qualification are
experiment002. Its whole-run impact is not measured by this offline analysis.
One healthy FIFO child continues;three queued policy cells are deferred by
pausing their serial wrapper. No new full baseline starts alongside it.

Run status:valid retrospective attribution,matched4warm comparison incomplete.
Tested resource-superiority hypothesis:inconclusive;no engine gain established.
Research value:supporting RQ3mechanism diagnosis. Independent audit:absent.
