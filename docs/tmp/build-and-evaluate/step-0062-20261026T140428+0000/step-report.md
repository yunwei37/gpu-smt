# Step0062 — fix confirmed shutdown/admission lifecycle race

BUILD_AND_EVALUATE,root-only,fourRQ/OSDIgoalcontinue.
[Plan](experiment-001/plan.md),[planreview](experiment-001/plan-review.md).

## EXPERIMENT_GATE
Realenginecode permitsstaleadmissionaftershutdownreturns ifresource sampling
overlapsclose. Deterministicnon-nativefixture provesit:redcargo101/1backendcall
aftershutdownvs0expected. Finalbackend_erroralonewouldhidethebug.
Sixlinein-lockfatalrecheck preventsleaseinsertionaftershutdown/fatal sampling.
21relevanttests pass;clippy-Dwarnings/rustfmtpass. Actualhelpersetupfailure
beforecargo retainedseparately,thenunusedLeanenvdependencyremoved.
No nativeproof/secondcollection/activeCLIrebuild. Combined1smonitor protects
current71ownerandnewcompiler;max46.034GBsampled,noabort/errors.
[Results](experiment-001/result-review.md),
[rawsources/receipts](../../../../artifacts/engine-lifecycle-2026-10-26/admission-after-shutdown/README.md).

## WRITE_GATE
Updatearchitecture atitshomewithactuallease/shutdownordering. No paperheadline/
RQ/novelty claimchange. Fullwriting/PDF/milestonereviewskippedforunchangedpaper.
ShortsupportCPUoverlapwithnative71referenceisrecorded,notcleanbenchmarkclaim.
Dailyreflectionretainsrealpriority:continueactual71/lean-mlirratherthanlogging.

## REVIEW_GATE
[Outer self-audit](outer-audit.md),rootself-reviewonly. Current71binary/module
identityunchanged. Newenginefixverifiedinsource,notretroactivecapturebehavior.
No independentaudit/OSDI/performance/correctnessofwholeLeansystemclaim.

## Next
Preserveactual71group,collectrealterminalsandinterpret48interval/23simpseparately.
Thenoriginallean-mlir. Applyfixedengineonfuturefreshbuildaftercurrentgroup.
No timer/poller/model/permission/quota/resourcepoint changes.
