# Ready bounded GPU experiment — Lean expression metadata

Prepared in the owning `gpu-smt-dev` Workspace/PVC, branch research/lean-acceleration.
This is a dependency-ordered loose-bound-variable metadata pass over the complete
real Lean init export DAG, not a GPU proof checker. Code, PTX and independent
CPU/official-Lean reference are ready. It is scientifically useful to test
whether GPU throughput survives 325 dependent waves, preparation and transfer,
and quantify the scope rather than claim whole-kernel acceleration.

Execution entrypoint (all paths on the owning Workspace/PVC):

```bash
cd /workspaces/repository
python3 bench/lean_dag_gpu.py \
  --ptx artifacts/lean-state-2026-10-04/dag_bounds.ptx \
  --input /workspaces/.agent-state/gpu-smt-lean-dag/init.dag \
  --reference /workspaces/.agent-state/gpu-smt-lean-dag/init.lean-reference.bin \
  --repeat 7 \
  --json artifacts/lean-state-2026-10-04/dag-gpu.json
```

The fixed measurement does 7 passes of 6,132,277 expressions, 325 waves/pass.
Every returned per-expression value is compared to actual official Lean metadata.
It reports initialization/JIT, allocation, upload, resident host/CUDA-event elapsed
and download separately. Python stdlib plus assigned matching libcuda.so.1 is
sufficient; PTX is already built with NVRTC 12.9.86, target compute_80.
Use the existing Kubernetes NVIDIA device-plugin/runtime allocation path; one
NVIDIA GPU supporting the PTX target (the available RTX 5090 is suitable) and
matching driver libraries. Packed buffers use 171,703,756 bytes of device memory;
allow approximately 1 GiB free VRAM for context/runtime overhead and about 1 GiB
host RAM. This does not require manual device mounts, allowlists, or host probing.
Preserve the owning Workspace/PVC and other projects/production model placement.

Input identities and exact file sizes are in
`artifacts/lean-state-2026-10-04/gpu-input-manifest.json`. The full original export
hash is 620502ac9e63ba4a2dea9d46386c2f6aebc49faf8848ea3aaa18a77a09491a6a.
Packed DAG/reference copies are retained under agent-state on the owning PVC;
originals are also in /tmp. Code can reproduce them from that export if needed.
The measured native CPU serial median is 21.9 ms (7 passes, affinity CPU 1);
Python preparation took 13.26 s plus 0.56 s scheduling/write, and official Lean
parse/reference output took 5.04 s plus 0.58 s serialization, single observations.
Neither preprocessing path is a production fast parser baseline. No GPU result
exists yet. Coordinate execution and return the actual result/log; do not infer
success from device visibility or a launched process.
