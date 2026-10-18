# Completed selected-LP qualification: stronger CPU and a GPU runtime fault

Root self-review only. All compared source verdicts/non-message responses
match native,with ten complete sources in each cell. Native74.444597310,
CPU-only37.540061162,CPU HiGHS18.129769163,and GPU Barrier40.055880871 seconds.
These inspected LP-head sources do not establish a full-cohort gain.
HiGHS has two resource-observer read errors;GPU has ten. Sampled memory
excludes full upstream GPU service aggregation.

The CPU HiGHS cell has34races:8external-support certificate wins,16exact-CPU
wins,10CPU no-certificate. The historical race log labels the external worker
gpu even with a HiGHS backend; these8are CPU wins,not GPU execution.
There are31socket connections,23parsed LPs(17optimal/6infeasible),8incomplete
JSON frames. CPU-shadow cancellation can interrupt transmission; connections
are not LP solves. Exact checks and native fallback remain active.

The GPU cell really requests Barrier,original feasibility,independent jobs,
minimum-ready1. It admits20jobs,observed RPC peak4,with11results and9member
cancellations;all20DeleteResult calls acknowledge,dispatcher pending0.
But eight returned results report worker death;server logs repeatedly show
CUDA error2 at cudaMalloc for x_values. Three successful RPC returns report
primal infeasibility and NaN solve-time fields;NaN is unknown,not zero.
All34races end on CPU(24certificates/10no-certificate),zero GPUcertificates.
Thus this is a preserved failed integration diagnostic,not a healthy Barrier
performance comparison or evidence excluding GPU opportunity.

The temporary Job is UID-checked deleted,other GPU Workspace Running and
labReady true. Complete cold lifecycle56.9204seconds includes client42.2116,
startup5.8551 and retirement/restoration8.8520seconds. Cold/collector clocks
are different boundaries and must not be conflated.

A fresh full1,000 native/CPU-only/HiGHS comparison is admitted and running on
CPUs0-3 based on the actual beneficial CPU preflight. Preserve it. GPU repair
now investigates the real allocation failure under the unchanged48GiB
ceiling before reusing this candidate. Do not start a full failed GPU matrix
or close the GPU route from these clocks. The full fourRQs,novelty and
repeatability remain open. No Agent or subagent was used.
