# Actual GPU API readiness — root implementation notes

The owning lab Workspace Pod currently requests no NVIDIA extended resource;
nvidia-smi/nvcc and cuopt/cupy/torch are absent. This is not evidence of absent
physical RTX5090 capacity. Do not restart an effective prefix capture to change
allocation. No replacement Workspace/checkout/Pod or external GPU runner is used.
CPU all-branch attribution proceeds now; actual GPU execution needs its existing
Workspace resource lifecycle after device admission becomes necessary.

NVIDIA cuOpt 26.10 [official convex features](https://docs.nvidia.com/cuopt/user-guide/latest/convex-features.html)
and [Python API](https://docs.nvidia.com/cuopt/user-guide/latest/cuopt-python/convex/convex-api.html)
were opened on 2026-10-17. The default concurrent method races GPU PDLP/barrier
and CPU dual simplex; a result from that default alone is not evidence of a GPU
solve. Explicit PDLP or attributed algorithm selection is needed for GPU claims.
The local BatchSolve API is deprecated; the HTTP proxy does not accept batch LP.
Do not accidentally use routing BatchSolve. Prefer supported local Solve calls
with measured request parallelism, or an actual small batched solver justified
by our measured shapes. Default PDLP tolerance is 1e-4; support search still
requires exact CPU repair and Lean checking. This note admits no solver choice
or performance prediction before full attribution.
