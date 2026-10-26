# Pinned bv_decide timing hooks — source observation only

The actual prepared nightly2025-12-01 SDK source is retained, under its original
Apache2.0 notices, alongside [line-indexed observation](source-observation.json).
No workload executes and no time/proportion/call count is inferred from this map.

Native frontend includes:
- Normalize: preprocessing goal and per-pass traces, class Meta.Tactic.bv.
- BVDecide: reflecting a goal, bitblasting to AIG, converting AIG to CNF,
  obtaining an external certificate, compiling expression/certificate/reflection
  terms, preparing reflection and verifying LRAT through mkAuxLemma.
- LRAT: DIMACS serialization, actual external SAT query, LRAT parsing and
  trimming, certificate construction. Keep nested parent/child costs distinct.

The standard trace profiler defaults to10ms and exports Firefox stacks.
By default output.pp=false exports class plus tag, omitting the message that
distinguishes many Meta.Tactic.sat phases. The next diagnostic export needs
-Dtrace.profiler=true -Dtrace.profiler.output=ABSOLUTE_PROFILE_PATH
-Dtrace.profiler.output.pp=true, with original --tstack=400000. No threshold,
SAT timeout, proof trimming, binary proof or kernel trust option is changed.
In particular debug.skipKernelTC stays at its native default. The source
frontend writes the profile only near completion; a killed/timeout run can
lack final profile data and must remain censored/missing rather than zero.

Full-message export may incur significant pretty-printing/time/memory overhead.
Retain raw profile and own diagnostic lifecycle, distinct from uninstrumented
file/stdin clocks. Native export constructs synthetic threadCPUDelta from wall
trace slices: it is not sampled CPU. Partition nested trace slices; do not sum
inclusive parents and children or overlapping threads into a whole-wall speed
ceiling. Missing below-threshold nodes are not zero-cost stages.

This is preparation for our original source workload, not reproduction of another
system or a claim that any SAT/LRAT stage is large enough for acceleration.
