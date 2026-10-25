# Actual qualification1 stopped
The diagnostic GNU C++ wrapper introduced a different C++runtime alongside
Lean's pinned libc++ runtime. The real allocationfailure source2404 changed
from native std::bad_alloc/resource_failure into return134 with
'terminate called without an active exception', causingHTTP500/retry.
This is a diagnostic ABI conflict; no hotspot or performance result is admitted.
Root sends SIGINT to its exactPID/birth only, retains raw and waits for actual
native cleanup. Replace diagnosticwrapper with C/pthreads/zlib so the original
C++exception/runtime remain untouched; retry within the same plan. No full480
capture is admitted until real timeout/allocation handling qualifies.
