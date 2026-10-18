# RQ4 independent LP cancellation control — root plan/self-review

## Causal admission and sources
The full1000 joint-model GPU race cancels311of384jobs when any CPU shadow wins.
The native-eight-queue qualifier repeats the pattern:7of9jobs cancelled and
23.857sGPU versus23.476sCPU. The actual pinned server banner is26.10.00.
[Official26.10 server behavior](https://docs.nvidia.com/cuopt/user-guide/latest/cuopt-grpc/grpc-server-architecture.html)
states that cancellation kills the active worker and spawns a replacement.
The generated pinned RPC descriptors expose single LP jobs and per-job cancel,
not a batch-of-LP RPC. [Official local batch API](https://raw.githubusercontent.com/NVIDIA/cuopt/main/python/cuopt/cuopt/linear_programming/solver/solver.py)
runs independent LPs in C++ threads; its return waits for the batch and no
per-LP external interruption is exposed in the inspected public Python/C API.
This observation is not proof that no low-level extension can implement one.
A same-context custom kernel is not justified before testing independent jobs.

## Mechanism and fixed comparison
Dispatch only simultaneously live groups of at least2eligible requests, as
before. Replace the joint block-diagonal solve with one independently
cancellable RPC model per group member. Allow at most the same8candidate
streams and8server workers; all server/client processes remain eligible only
for CPUs8–11,oneRTX5090shared device,48GiBAS per process,zero cores.
The upstream default/recommendation is1worker/GPU;8workers is a finite
benchmark candidate chosen from the fixed8candidate streams,not a retained
server setting or parameter grid. CPUeligibility is unchanged. Additional
worker/context/RMM memory is a cost,not equal-memory evidence. NoMPS,extraGPU,
newWorkspace,scheduler or persistent helper is introduced.
Each model retains the exact same phase-I PDLP+crossover settings,CSRpacking,
CPUshadow,exact repair and Leancheck. A CPUwinner cancels only its own GPUjob;
it cannotdiscard another model's work. Existing joint batching is default;
the independent mode is opt-in.
These are concurrent independently cancellable LP jobs admitted as groups,
NOT a fusedGPUbatch. Parallel server intervals do not prove overlapping CUDA
kernels; separateCUDAcontexts maytime-slice. Report both distinctions.

## Execution and decision
Use the same original24sources and native8queue protocol as the just-closed
comparison,maximum8commands,CPU8–11,48GiB. Reuse its actual matching native
and CPUoracleraw references. Cold-start a fresh instance of the same pinned
upstreamJob name; no numerical warmup,retire all RPCs,deleteUID-matchedJob,
verify labReady and otherWorkspaceRunning. Private endpoint only.
Record source outcomes/native payloads,actual task spans,winner/cancellation
ledgers,admissiongroups/singleLPjobs,all serverworker logs and fullcoldclock.
Successful interface engagement alone does not admit a full1000matrix. Only
a beneficial matched preflight with completecost rationale can do that.
Failure retains the raw data and rejects this integration,not theGPUroute.
The current2.67957x own-clock sensitivity does not establish impossibility;
answer-aware omission controls remain excluded from the1.5xthreshold.
No unrelated collector/nativebinary is modified or restarted.

## Self-review and lifecycle authority
Same root thread owns all code/run/review. ScientificRQ4,InitialNarrative,
fourRQscope and finalbestvalidCPU/GPU>1.5xcriterion are unchanged. This is
supporting causalqualification,not a completedpaperclaim.
User-authorized finite benchmark:「只把大 LP 送 GPU…同时让 CPU 并行求解同一个 LP，
谁先给出可精确修复的支持集就用谁，另一个立即取消。」
and「在总资源相同的前提下让多个候选并发跑」.
The benchmark ends at completed24rows plus RPCretirement andJobdeletion;
no persistentconfiguration is retained. Baseline and all earlierfailures
remainretrievable. Moreworkerprocesses mayaddstartup,CPUcontention andGPUmemory;
capturethatcost ratherthan claimingGPUcanneverbeslower.
