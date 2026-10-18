# Request-sized VMM implementation self-review

Root only. Numerical phase-I kernel is byte-identical to the prior independent-
group source. No solver tolerance, pricing, thread count or iteration budget
changes. Allocation sites replace cudaMallocAsync with synchronous address/physical
mapping operations sized from actual arguments and discovered minimum granularity;
copy/kernel dependencies still use their existing nonblocking streams/events.
Driver flags0, default driver address choice, single current GPU location,
no shareable handle export. Both allocation/map error cleanup and owner-stream
synchronization before unmapping are explicit. Mapped creator handles are released;
mapping ownership remains until unmap, then exact reservation size is freed.
Live count/bytes/peak bytes are exported for real retirement evidence.
No startup pool or arbitrary arena size exists. Underlying allocator internals
are not claimed; only actual API outcomes are evidence.

Retirement removes handles from cancellation state under its existing lock,
then frees outside that lock so waiting owner-stream cleanup cannot prevent
other groups' cancel operations. Cancellations already holding the lock finish
before handle removal; later calls see no handle. Batch event has finished before
model retirement. A free failure remains a live allocation in accounting and
cannot be reported as successful cleanup. The C++ error string retains precise
driver operation/status rather than replacing it with a generic runtime error.
Build CUDA12.8/sm120/shared CUDART/driver stub succeeds in owning Workspace.
This is compatibility source review, not GPU engagement or performance proof.
Actual64source/kernel overlap/retirement qualification is required next.
