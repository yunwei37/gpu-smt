# E1058 implementation continuation: request-sized VMM

Root thread only,2026-10-18. Keep the same independent-group mechanism, numeric
kernel, CPU shadow/exact repair, Lean checks, row11 eligibility and actual ready
batching. The async allocation candidate and one discovered-maximum pool repair
both failed before any GPU kernel under48GiB. This is an implementation
compatibility repair, not a new research question or a pool-size/buffer/cache/
thread tuning grid. No further pool policy is tried.

Use NVIDIA driver VMM operations to create exactly each actual LP buffer size
rounded only to the API's discovered minimum allocation granularity. No pool,
pre-reserved giant arena, resource limit increase, memory sharing across users,
new persistent service or cluster policy. Driver-chosen addresses, flags0.
Original async stream/event/cancel operations remain. Each buffer maps one
physical allocation and releases the creator handle after mapping; after its
own stream finishes, unmap the same size and free the address reservation.
Track live allocations/bytes and preserve API names/status codes on failure.
This is established CUDA memory management, not a novelty claim.
Primary source: https://docs.nvidia.com/cuda/cuda-driver-api/cuda_driver_api/group__CUDA__VA.html

Qualification is the SAME original64/capacity32/fourCPU8–11/48GiB finite
5090 benchmark. Existing CPU/native capacity controls are retained. Require
actual launched kernels, cross-group globaltimer overlap, per-source verdict/
non-message fidelity, and all model/group allocations retired. No fullGPUmatrix
without a real end-to-end advantage over the strong CPU path. Cold GPU context
startup remains separately reported. Failed repair and earlier failures stay
published. The active full29,750 CPU0–3 and prefix20–23 remain untouched.

Current opportunity does not allow broad negative GPU closure: all-race deletion
on the third CPU pair still models1.53475x versus its native reference, with
missing product/small-LP attribution. This does not guarantee this candidate can
win. A functional or performance failure is retained at its actual scope.
Review is root self-review, never independent audit.
