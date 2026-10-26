# Final consumer journals for later resource-pair captures

Root-only source/test/self-review,2026-10-26. This is evidence-retention work,
not a new Lean experiment,accelerator or performance result. The current
source42659a8fullpair remains unchanged. Before source52f912d is retained in
before.rs.gz andGit;old physical-journal semantics remain.

## Missing evidence and implementation

The live pair keeps physical attempts but produces its aggregate Capture at
whole-cell completion. Backend cancellation can be reclassified by the engine
as preemption/resource exhaustion and followed by an exclusive retry. Physical
rows therefore cannot stand in for a finalcaller/native-acceptance set.

Later resource_pair drivers use existing Engine::verify_stream/BatchEvent.
The same original-order Verification vector still forms Capture. Each cell
additionally writes results.jsonl,validating index/ID/unique result/count and
flushing a complete line per event. A validatedComplete covers allconsumer
rows,not idle-backendshutdown or whole-cell lifecycle. EOFwithoutComplete is
partial. No missing outcome is reconstructed. No newpublictype/queue/controller/
checkpoint schema,policy,resource setting or automaticresume is introduced.

The old physical journal remains distinct. Actual journalI/O is included in each
newcell's own clocks;future versions must not be pooled with the current live
recording version. No fsync/power-loss guarantee. Bothconditions pay the same
recording path. Inputsource/timeouts/consumer/cache semantics stay unchanged.

Open the consumerfile before stream submission. I/O failures drop the stream
and pass through the existing unconditional engine.shutdown before propagation.
HandleSIGTERM alongside existingSIGINT,then drain finalconsumer outcomes,mark
thecell interrupted and stop before the nextcondition. Normal fullcell/pair
completion still needs Capture/terminal/comparison. No activebinary is replaced.

## Executed checks and raw scope

validation/receipt.json:53ordinaryworkspace tests/0failed/4nativeignored,
5exampletests,fmt,Clippy-Dwarnings and actualdebugexample--help pass.
No native proof is run. Newfixtures prove a fastfinalresult is readable while
its peer isheld,normalcompletion preserves originalinputorder,aborting the
collector retains a partialline-completeprefix withoutComplete,and writefailure
propagates after ownedworkretires. Controlled forecasts/zeroRSSmonitor are test
fixtures,not realmemory/performance models.

integration/receipt.json exercises the actualdebugexample process with a Python
protocol fixture and signals only its ownPID. BothSIGTERM/SIGINT find one
flushedfinalfastresult before interruption,then retain twofinalconsumerrows,
a Complete(count2),and terminalstateinterrupted. Fast stays accepted in the
fixture;held becomes enginebackend_error. The streamevents exactly match the
saved Capture. Everyrecorded child retires;the preparedcell neverstarts.
This Complete meansconsumer rows,not successfulpair completion.
No actual Leanstatement is checked;environment is controlled-not-Lean.
The 0.12s fixtureobservations are lifecycle checks,not latency/speedup results.

Raw command/driverlogs are stored losslessly asgzip,with originalscripts and
receipts. No raw trailing whitespace is rewritten. The integration fixture and
PIDmarkers are removed fromOStemp after their owned processes retire.

## Resources / publication boundary

Ordinaryvalidation's combined own+originalfull1s sampledpeak33,500,778,496B;
actualintegration sampledpeak11,854,999,552B;48GiB=51,539,607,552B,0pressure/
monitorerrors. Shared-hoststate differs betweenruns;these are combinedsamples,
not modelmemories or a kernelquota. Development usesCPU10–11 and no fixedAScap.
The originalrelease/host/pid/birth/capture remains unchanged;preserved-fullpair
records that actualidentity and pendingcapture. No second nativecandidategroup.

Codegrowth is production+56/test+166lines in the existingexample. Oneprivate
collector reusesBatchEvent,stdlibWrite and existingengine API. Tests share one
gatedbackend/resourcefixture and include partial/errorcleanup,not a newtest
framework. Core/service/backendsource,dependencies/workflows/QuickStart/paper
remain unchanged. Example docs explain the newfile andoldversionboundary;
benchmarking replaces its stalequeueorder with the canonicalevaluationlink.
Review is self-review,not independent audit. Wholepopulationperformance,
safeMathlibbenefit,reliableearlyrejection and OSDIcontribution remain open.
