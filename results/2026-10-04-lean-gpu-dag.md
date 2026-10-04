# RTX 5090 execution of a real Lean expression-DAG primitive

A CUDA dependency-ordered metadata pass over all 6,132,277 expressions in the
real Lean init export completed on **RTX 5090**. All seven returned arrays
matched actual official Lean metadata at every index. Resident GPU execution
had median host wall 0.853 ms versus 17.799 ms for the best measured native CPU
reference, a 20.87× ratio for this primitive. This is an implemented, executed
GPU experiment; it does not check proof types, perform reduction, or establish
a full Lean-verification speedup.

## Operation and independently checked input

The primitive computes `Expr.looseBVarRange`: zero for closed leaves, `index+1`
for bound variables, maximum across application children, saturating decrement
under binders, and the corresponding recurrence for lets/projections. Lean
expression constructors cache this metadata. It is a clearly delimited parallel
construction/metadata operation, not an identified dominant kernel hot spot.
Recomputing all nodes in a prepared DAG is different from incremental creation
and use of that cache in an ordinary checker.

Input is the pinned Lean Kernel Arena init export, SHA256
`620502ac9e63ba4a2dea9d46386c2f6aebc49faf8848ea3aaa18a77a09491a6a`.
`bench/lean_dag_pack.py` validates dense expression IDs and backward child
references, packs nodes into a 20-byte layout and schedules them by DAG depth.
The selected export has 325 levels, peak level width 339,488, and 117,170
declaration type/value roots, all with zero loose-bvar range. This root property
does not certify declarations' types or proof validity. Unsupported tags,
sparse/forward references and bound indices outside the tested metadata range
are rejected by the packer rather than silently approximated.

`bench/lean-persistent/LooseBVar.lean` uses the existing official exporter parser
and writes actual `expr.looseBVarRange` for every expression. The independent
Python implementation matched all 6.13 million values byte-for-byte, as did
every native CPU and GPU pass. Reference SHA256 is
`a005b640664d91d844e9e894e178f6c526660b2942bdae3df05c3c58823f7d60`.
The packed input is 147,644,656 bytes; node/order/output device buffers total
171,703,756 bytes. Compressed exact input/reference and a hash-verified manifest
are retained in the repository, with originals also on the owning PVC.

## Measured CPU and GPU components

Native `bench/lean-dag/dag_bounds.cpp` compares a serial topological traversal
and OpenMP depth waves. CUDA `dag_bounds.cu` launches one kernel per nonempty
level, all in one ordered stream, with 256 threads/block. PTX was built on CPU
using NVRTC 12.9.86, `compute_80`, C++17. Runtime is a stdlib Python ctypes CUDA
Driver API harness; no Lean or framework code is executed on the device.

| prepared/resident pass | affinity / device | median of 7 passes |
|---|---|---:|
| native serial | CPU 1, one thread | 17.799 ms |
| native depth waves | CPU 1, one thread | 68.381 ms |
| native depth waves | CPU 0–7, eight threads | 18.186 ms |
| CUDA depth waves, host wall incl. launch/sync | RTX 5090 | 0.853 ms |
| CUDA depth waves, event interval | RTX 5090 | 0.841 ms |

The native serial path is the best measured CPU backend for this operation.
Eight-thread waves offer no advantage over it here. That does not establish
bandwidth saturation or an irreducible serial cost. Earlier CPU observations
were 21.932 / 109.039 / 78.261 ms and are retained; the matched rerun supersedes
them for this comparison. The rerun followed completion of deliberate Lean
measurements; an SMT probe ran on CPU 8. Affinity does not establish isolation,
and CPU/system pressure was not controlled across CPU and GPU measurements.

One assigned-device job reported these separate components:

| component | observed time |
|---|---:|
| packed input/reference host read and preparation | 368.928 ms |
| CUDA context/module initialization and JIT | 354.937 ms |
| device allocation | 0.204 ms |
| packed nodes/order upload | 12.545 ms |
| resident pass, median | 0.853 ms |
| output download, median | 2.784 ms |

Upload + median resident pass + median download totals **16.183 ms**, only
1.10× below the best CPU resident pass. That sum combines one observed upload
with medians and excludes host reading, packing, context/JIT and allocation;
it is not a measured end-to-end speedup. Resident pass + median download is
3.637 ms when the GPU representation already exists. The first-pass measured
component sum, including host read/init/alloc/upload/compute/download, is
739.895 ms; it excludes JSON output, comparison bookkeeping and original export
preparation, and is not paired with a comparable CPU end-to-end trial.

Separately, Python NDJSON parsing/value packing took 13.261 s plus 0.561 s for
scheduling/write. Official Lean parsing/reference output took 5.036 s plus
0.583 s serialization. These are single observations of different preparation
implementations, not matched parser baselines or measurements of metadata's
share of ordinary checking. Raw NDJSON transfer alone would miss these costs.
Measured upload/download replaces assumed PCIe bandwidth for this experiment.

## Execution identity and limits

Outer coordination ran Kubernetes Job `coder/gpu-smt-lean-dag-5090-20261004`,
Pod `gpu-smt-lean-dag-5090-20261004-npq9w`, node `lab`, through the existing
NVIDIA device plugin and `nvidia` RuntimeClass. The retained runtime record
shows one healthy assigned device, actual RTX 5090, restart count 0, exit 0,
and execution from 11:16:45 to 11:16:47 UTC on 2026-10-04. The fixed container
image is `lmsysorg/sglang@sha256:9ca30410d6280c09c8e6804525b8ba0ef598c456044e758819046f8ef3037020`.
The CUDA driver API version reported is 13030; this is not a full OS driver
package version. Input/reference/PTX hashes in the returned JSON match the
submitted artifacts. The script snapshot matches the source retained here.

The user directed “不要 b300, 用 5090”. No GB300 computation ran. The four
public files were mounted read-only from this project's existing PVC. No manual
device mounts, host probing, production model move or interruption of another
project was needed. The retained `gpu-cleanup.json` receipt confirms Job
deletion and Pod absence during 04:16–04:24 America/Los_Angeles
(11:16–11:24 UTC), with the same Job/Pod/node identities. Node readiness,
pressure and disk availability in that receipt are observations from that
window. They do not describe the later Longhorn auto-salvage/container recovery
at 22:16 UTC. The same source PVC survived that later recovery; temporary
dependencies were lost.

Seven passes are repetitions within one initialized context and one job, not
seven independent device launches. Kernel/transfer timings do not include image
pull, Pod scheduling or allocation queue delay. No throughput-under-arrival-load,
device-memory peak, power/cost or sustained bandwidth result is inferred.

## Reproduce and use the evidence

The following packed-input commands do not require the lost `/tmp` dependency
checkouts. [Recovery reproduction instructions](../docs/reproduce-checkpoint.md)
also cover optional toolchain rebuilding and the Mathlib/VeruSAGE entrypoints.
CPU execution needs Python 3/C++17/OpenMP; the GPU step needs an assigned RTX
5090 with matching driver libraries, and has not been rerun during closure.

```bash
mkdir -p /tmp/lean-dag-replay
tar -xzf artifacts/lean-state-2026-10-04/init-dag-inputs.tar.gz \
  -C /tmp/lean-dag-replay
g++ -O3 -std=c++17 -fopenmp bench/lean-dag/dag_bounds.cpp -o /tmp/dag-bounds
taskset -c 1 /tmp/dag-bounds /tmp/lean-dag-replay/init.dag \
  /tmp/lean-dag-replay/init.lean-reference.bin serial 1 7
# On an assigned RTX 5090 with matching libcuda.so.1:
python3 bench/lean_dag_gpu.py --ptx artifacts/lean-state-2026-10-04/dag_bounds.ptx \
  --input /tmp/lean-dag-replay/init.dag \
  --reference /tmp/lean-dag-replay/init.lean-reference.bin \
  --repeat 7 --json /tmp/dag-gpu.json
```

Rebuild PTX with `python3 bench/lean_dag_gpu.py --compile-only --ptx /tmp/dag.ptx
--nvrtc /path/to/libnvrtc.so.12`. To regenerate packed data, run
`bench/lean_dag_pack.py INPUT.ndjson OUTPUT.dag`; build `looseBVarReference` in
`bench/lean-persistent` to regenerate the official reference. Input hashes,
toolchains, build logs, initial/matched CPU results, full GPU JSON, runtime
record, cleanup receipt and derived arithmetic are under
`artifacts/lean-state-2026-10-04`. Original temporary paths in provenance describe
the measured container; use the retained archives or rebuild dependencies after
recovery. Hashes are provenance, not new startup or proof-acceptance gates.

This result supports fast GPU execution of a wide dependency-ordered expression
primitive **when the representation is resident**. Useful next GPU work requires
measuring its contribution during real checker construction, or selecting a
more expensive operation that can reuse this representation. Fusing constructor
metadata or batching other expression analyses may amortize preparation, but
those are hypotheses. Whole-library checker comparisons still favor measured
alternative CPU checkers; no comparison between this metadata-only executable
and nanoclo/official full verification would have matching semantics. GPU
certificate proving also remains distinct from ordinary Lean type checking.
