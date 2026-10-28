# Refresh the existing global fallback at actual admission

Inner::run currently combines the policy forecast with the then-current global
median before the request queues. Acquire refreshes global fallback only if
that cached value isNone,so warm batches can remain stuck on an obsolete high
median even after observed demand falls. Keep only explicit policy forecasts
in the queued request;use the existing fresh-median fallback insideacquire.

No resource cap,deadline,ranking,exclusive retry,verdict/cache contract or public
API changes. This is a resource-layer repair,not a new scheduling/failure policy.
The historical singleton partition does not establish a cost for this bug.

Regression:seed priorfallback60,budget100/three virtualCPUslots;queue5unknown
requests before firstcompletion. Firsttwo report actualpeak1;allremainingthree
must enter together on the new median1. A cached60would serialize them. Cleanup
must complete even if the regression reappears. This is an engine fixture,not
Lean/native workload evidence. Existing workspace,watchdog/retirement,clippy/
fmt and subsequent pinned-native CI validate the surrounding contracts.
Supporting tests stay inCPU8–11 and under combined currentgroup/helper monitor;
do not start another native collection or alter its frozen binary.
