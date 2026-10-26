# Plan — reproduce and fix a possible admission/shutdown race
Sourceinspectionfindsacquirechecks fatalbefore synchronousresource sampling,
then insertsa leasewithoutrecheckingunder theactive-state lock. Shutdown can
finishwhile sampleisoutstanding,then staleadmissionmightstartnewbackendwork.
This is a concreteengine lifecycledefect,not newresearchtooling.
Firstdeterministicnon-nativefixture:holdresource sample,complete shutdown,
releasesample,assert nobackendcall/leaseiscreated. Retainredfailure on oldcode.
Ifconfirmed,recheckfatal understate lock beforeleaseadmission,run focusedred/
greenand relevantengine tests. No nativeprooftests/CLIrebuildwhile71runs.
UseexistingcombinedRSSmonitor on currentnativegroup+newcompiler/testchild,
CPU11/onecargo job;abortonlynewchildifpressure. No runtimebinaryreplacement.
Preserveactualcaptureclock/confoundscope. Root-onlyself-review;noagents.
