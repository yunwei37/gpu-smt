# M1 — hardware counter access and precompile census

Self-review; actual G10 read-only probes, no main-engine change.

- CPU: AMD Ryzen5 3500U,4 physical cores/8 eligible logical CPUs; about27.8GiB RAM.
- perf executable absent; perf_event_paranoid=4.
- Direct perf_event_open for hardware cycles AND software CPU-clock both fail
  EACCES(errno13). No privilege/security change attempted. IPC,LLC/dTLB miss
  rates and cycle fractions for lean_inc/dec,allocation,hashing/interpreter
  remain UNMEASURED; a CPU-time profile is not a substitute for those counters.
- The retained matching4.9 Mathlib cache has4360olean modules and392flat shared
  library files(31,667,520bytes).124of217tactic modules have matching -1.so
  names. Presence does not prove they were loaded or executed. The prior
  observation that Linarith is loaded does not imply all other tactics interpret.
- Existing generated C:4365files,300,689,051bytes. This is source size, not
  compilation seconds, peak RAM, final library size, or a speedup estimate.
  A full precompile is deliberately not launched on the shared G10 point.
  Build planning must include all downstream objects/linking and SDK libraries;
  currentPVC free space was about2.49GB before this branch's small outputs.
- A finite import/maps control is in progress, with source maxHeartbeats10000,
  Lean -M4096/-T20000000/-j1,CPU4-5 and no signals. Its initial observed state
  is low-RSS disk wait; no terminal result or native-execution fraction is claimed.

## Direction decision
Counter-access evidence makes the requested perf experiment unavailable here;
it neither supports nor refutes precompile benefit. The native-library census
refutes the premise that the installed cache contains only a Linarith library.
An interpreter-cycle fraction or actual matched A/B is still needed to estimate
precompile acceleration. Do not use124/217as a time fraction or Amdahl input.
