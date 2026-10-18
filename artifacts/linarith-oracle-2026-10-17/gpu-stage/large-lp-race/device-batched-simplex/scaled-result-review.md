# Scaled device-batched LP preflight: real kernels,still slower than HiGHS

Root self-review,not independent. The same inspected10sources complete with
native verdict/non-message parity;warning-only source changes:['Proof_01755', 'Proof_15934'].
Warm complete cell32.718745698seconds vsfirstGPU37.979239485,CPU-only37.540061162
and CPUHiGHS18.129769163. The selected-subset gain over CPU-only is12.84%,but
GPU remains80.47%slower than the strongest selected CPU alternative.
Complete cold lifecycle51.0970244seconds includes preparation/retirement;
do not compare its scope with bare kernel time or erase cold startup.

Six actual CUDA launches each include two distinct source candidates,twelve
models total. Result states:two feasible hints,three independent cancellations,
five phase-I no-hint,two numerical declines. All34races finish:22CPUcertificates,
10CPU no-certificate and2GPUcertificates checked by exact repair and Lean.
Allsix launched groups have model/kernel-retirement acknowledgements;dispatcher
pending0. CPU cancellation doesnot discard siblings or restart a process.
This directly establishes engaged GPU batching/cancellation,not1.5x performance.

Row/column equilibration and reduced-cost pricing lower the selected whole
clock,but one case still reaches12435pivots before CPU cancellation. The
numerical provider remains weaker than HiGHS on these real moderate LPs.
No tolerance/grid or full unprofitable GPU matrix is admitted. No broad GPU
impossibility claim follows. The complete own-clock profile still fails to
exclude1.5x. The ongoing full native/CPU/HiGHS comparison determines the
strongest CPU end-to-end result,then any remaining GPU opportunity must be
judged against that actual competitor rather than the weaker exact-only path.

Ten process-tree sampling read errors make the sampled memory peak incomplete.
All raw errors/partial JSON frames and launch/source identities remain.
The temporary5090Job is UID-deleted;labReady and otherWorkspaceRunning.
This is implementation evidence,not a novel systems contribution by itself.
The original fourRQs,full experiments,paper and novelty goal remain open.
