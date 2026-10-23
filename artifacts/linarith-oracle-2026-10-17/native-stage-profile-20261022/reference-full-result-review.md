# Complete native-helper1000 attribution — root self-review

## Question, completion and comparison

RQ4: after preparation reuse, when does heterogeneous execution improve complete
verification over the strongest measured CPU path? This supporting diagnostic
tests which actual numerical work could be replaced or avoided, not GPU speed.
Run status valid for measured wrappers; GPU hypothesis remains inconclusive.
Original1000/order,source2/live2,24GiB per REPL,48GiB aggregate sampledRSS,fourCPU
8–11, qualified reference hybrid algorithm. Whole1380.322630987s, warm
1374.125432706s, preparation5.676476965s. All992complete/8reject and all1000
full raw responses match the frozen native cell. Earlier1448.917480465s
reference and1450.783580374s diagnostic are separate clocks; neither is a
denominator to rescale these phases, and their difference is not GPU gain.

## Same-clock stage partition

|Stage|Caller CPU(s)|Accumulated wall(s)|
|---|---:|---:|
|Preprocessing|99.856771|99.875718|
|Linearization|104.185575|104.198326|
|Nonlinear products|225.577301|225.613134|
|Lean LP wrapper|8.750058|1013.994258|
|Lean certificate construction/check|220.855698|220.896434|

All8646native requests, from995actual arithmetic sources, have paired,
source/call-owned phases and packed FPmatrix shapes. Every helper request is
inside its own source's Lean LP wrapper. No unknown source, unpaired event
or escaped interval. The5remaining sources have omega rather than helper work;
do not inflate actual helper-source coverage by inserting zero-cost tail rows.
The reader's earlier995→1000defaultdict side effect was corrected before this
result publication; no raw observations changed.

|Native helper phase|Calls|CPU(s)|Wall(s)|
|---|---:|---:|---:|
|FP matrix packing|8646|1.110725|1.498451|
|FP LP solve|8646|39.911513|39.935943|
|Exact fallback|1636|951.680533|951.845679|
|Exact positive support repair|7061|0.575332|0.599694|
|Exact certificate verification|15016|0.446071|0.453481|
|Complete native helper request|8646|999.397150|1000.126516|

Exact fallback is95.97%of FP+exact-fallback wall. It includes matrix
construction, coefficient conversion and rational cleanup, not just pivots.
Request wall outside inner-stage unions totals5.793268s; Lean LP wrapper
outside helper requests totals13.867742s, which includes Lean packing/IPC/
stock fallback/queueing and must not all be labeled communication.
Initial context parse precedes the helper request guard; output flush follows it.
All observation/logging costs remain in whole time. There is no old976CPU
denominator repartition and no unobserved path becomes zero.

## Shapes, tails and batch eligibility

Actual FProws median37,p90=114,p99=218,max888; columns136/309/630/3160;
nnz727/2309/5603/26044. Shapes include the normalization row and accumulated
matrix values, not maxVar/exact-tableau dimensions or wire terms.
The median split gives4330calls below38rows and4316at least38rows.
Small calls still have187exactfallbacks costing50.095157s, plus1.099154sFP;
large calls have1449fallbacks costing901.750521s, plus38.836789sFP.
The historical0.02CPU-small-call assertion does not describe this measured
whole native stream. Eligibility must use this actual population.

There are3102cross-source overlaps from FPmatrix-ready to native answer,
max2open under source concurrency2. These include search/repair; they are
hypothetical race windows, not completed GPUbatches or free device input.
Exactfallback tableau dimensions and per-call nonlinear product provenance
remain unavailable.

Use the same frozen-native-ranked identities. Slowest1% (10complete) has
446.724797s overlapping HTTP,LP110.562035s/products0.711505s/preprocess
52.943992s/linearize3.977645s/certificate30.243111s. Its2314helperrequests
contain only9exactfallbacks, but those cost108.364228s versus0.483857sFP.
Slowest10% (98complete/2reject) has1267.084249s overlapping HTTP,LP484.028918s/
products70.637797s/preprocess67.446310s/linearize50.925226s/certificate
76.943620s. Its4863helperrequests have673fallbacks462.362903s/FP9.878342s.
No overlapping tail sum is called an isolated tail lifecycle.

## Opportunity and decision

LPwrapper wall/own whole is73.460670%,products16.344957%, but those concurrent
sums are not disjoint removable wall. Combined product+LP occupied union is
956.066424559s,69.263982%of this own1380.322631s clock. Deleting that entire
observed union while fixing all other timestamps gives a conditional
3.253512x sensitivity. This deliberately overbroad fixed-trace calculation
is not a scheduler-independent Amdahl ceiling: LP envelopes include repair/
transport and products include proof construction; omitted work and schedule
changes prevent a strict bound. It cannot justify negative GPU closure.

The measured bottleneck is expensive exact fallback, not the39.94s FPkernel.
GPU support search must avoid fallback while retaining CPU HiGHS and native
contenders, then pass exact repair and Lean checks. Existing additive64GPU
qualification was slower than HiGHS; that honest negative remains. Next
execute the large-LP additive competition at the current safe resource point,
including actual source-owned batches and every lifecycle cost, rather than
another narrow kernel, parameter grid or broad impossibility statement.
Original1.5x criterion uses the better valid CPU/GPU result; all4RQs and
OSDI-level target remain open. This result supplies mechanism costs, not a
novel systems contribution or evidence of GPU acceleration.

## Resources, raw records and self-audit

Peak sampled ownedRSS15.550793GiB,max2liveREPLs,1381samples,0kills/errors,no
owned descendant after retirement. One-second monitoring is not a kernel-hard
RSS quota. All failures/partial history and raw bytes are retained; closed
plain logs are gzipped with byte-equal roundtrip receipts. All work and review
are by root, with no independent audit claim. A transient SSH timeout and
HA API refusal during collection of this result recovered through existing
management reads; lab/UM760 SSH/services and all cluster nodes were verified
Ready, with no reboot/configuration/Workspace/data change.
