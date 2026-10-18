# Full1,000-source native/CPU/HiGHS pair

Root self-review only. Same original1,000sources,eight upstream contiguous
queues,max8candidate tasks,CPUs0-3,48GiB,originalimports/heartbeats and EOF
retirement. Whole clocks include preparation,packing,queueing,fallback and
per-cell proxy setup/retirement. This is one complete three-cell observation.

| Method | Whole seconds | Native ratio |
| --- | ---: | ---: |
| Native pooled baseline |691.095897040|1.00000x|
| FP-first CPU oracle |529.171190393|1.30599683x|
| CPU HiGHS support+exact CPU shadow |462.504846990|1.49424574x|

Everycellreturns992complete/8rejected/0operational. All1,000sourceverdicts
and non-message responsefields agree. CPU-only88warning-onlychanges;HiGHS104.
All1,000taskspans mapuniquely;no missing/ambiguous source. HiGHS150process-read
errors make sampled memory peaks incomplete. Native andCPU-only have0.
The observed1.49425x doesnot meet>1.5x;the difference is1.77425seconds from
the460.73060s threshold. Do not use single-pair noise to claim stability or
replace this native denominator with a different run.

HiGHS has1,888numerical races:393external CPUhint certificate wins (legacy
winner label gpu),281exact CPUcertificate wins,1,214exact CPU no-certificate.
The1,385socket records include930completeLPrequests(467optimal/463infeasible)
and455interrupted JSONframes,not1,385completed solves. HiGHS LPcall wall sums
7.29524s and modelbuilding0.60921s. These are overlapping cumulative walls,
not fractions of whole verification. All CPUexact no-certificate race decisions
sum177.75614s;exact certificate decisions7.53301s;external certificate decisions
22.42581s. Decision spans include coordination/childstartup/repair and cannot
be called pure solver CPU or removable whole-wall time.

Native-selected slowest1%:taskspan sums1015.47native/761.48CPU/764.26HiGHS,
occupiedunions580.54/474.94/414.62s. Slowest10% sums2313.71/1728.16/1502.73,
unions656.44/499.66/439.78. Overlap is explicit;these are not end-to-end
speedups for an independently scheduled subset. Native ranking is retained.

The complete result strengthens the CPUalternative. Selecting HiGHS is an
existing solver baseline,not sufficient systems novelty. Actual GPUbatched
simplex qualifies real2/3-source launches and exactcheckedwins,but its selected
whole clocks trailthisstrongCPUalternative;no fullunprofitable GPUmatrix is
admitted. CPU1.49425x isnot a projectclosure orGPUimpossibility conclusion.
The original allcall profile remains scoped to its own earlier native/oracle
clocks,not divided by462.50s. The next numerical opportunity is costly exact
negative decisions that current success-only floating hints cannot discharge;
any two-sided oracle would need exact infeasibility-certificate validation and
complete matched native outcome checks before a full run. FullfourRQ/paper/
novelty/replication gaps stayopen. No delegationorindependent audit claim.
