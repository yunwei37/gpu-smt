# Hot-tactic native-code audit

2026-10-30 UTC, self-review. This uses the persisted Lean 4.9.0-rc1 installation
and the frozen full7808 engine capture. No PMU or native precompilation build.

## New finding

The historical prepared backend reports successful loading of
libMathlib-Tactic-Linarith-1.so. Its ELF dynamic section contains **684 direct
DT_NEEDED entries**, including the Linarith frontend, preprocessing,
verification, oracle and simplex modules, plus NormNum Core, Basic, Result,
DivMod, Pow, Inv, Eq, Ineq, OfScientific and the NormNum umbrella.

Consequently “only Linarith was loaded” does not mean only Linarith code was
native: successful dynamic loading also resolves those dependencies. This is
linker evidence tied to a historical successful load, not a fresh process-maps
measurement or a CPU-time fraction. Raw dynamic sections and selected dynamic
symbol tables are retained in hotspot-static/.

| Hot tactic | Observed compiled implementation | Qualification |
|---|---|---|
| simp / simp_all | SDK libleanshared.so exports evalSimp and evalSimpAll | Native entry handlers exist in the SDK loaded by Lean. Recursive simplification may still invoke interpreted extensions; whole-tactic native time is unknown. |
| omega | SDK exports Lean.Elab.Tactic.Omega.omegaTactic | Core compiled implementation exists; this is not the unrelated external CPU oracle. |
| decide | SDK exports Lean.Elab.Tactic.evalDecide | Elaboration dispatch is native; ordinary decide subsequently uses kernel reduction. Compiling tactic code does not bypass the kernel. |
| norm_num | NormNum Basic exports arithmetic evaluators; its library and Core are dependencies of the historical loaded Linarith library | Not wholly interpreted in that service. Extension dispatch and any modules outside the loaded closure remain to be measured. |
| linarith / nlinarith | Frontend and preprocessing/verification/solver libraries occur in the loaded dependency closure; frontend native symbols exist | The umbrella .so itself has few tactic bodies. A filename-only census misses its dependencies. |
| interval_cases | No matching IntervalCases shared library in the installed module census | Its tactic implementation is an interpreter candidate in this build. Native helper calls remain possible. This does not imply all interval_cases CPU is interpreter overhead. |

The matching interpreter source sets its default prefer-native option to true
unless overridden at build/option level. For each function it searches boxed,
then unboxed native symbols; otherwise it executes IR. Execution is mixed at
function granularity. We have not proved the installed binary's build macro was
unmodified, nor sampled all dynamic dispatches. The raw command line and
options of any performance experiment must be retained.

## Decision

The available evidence **rejects using 124/217 as an interpreted CPU fraction**
or as an Amdahl speedup estimate. It narrows the precompile opportunity: several
important hot handlers are already compiled. An all-native build has no
measured speedup yet. Without timed interpreted-helper residence and a same-run
denominator, its acceleration estimate is unknown.

Reference counting often inlines, and allocator/hash operations can lie inside
native tactic and kernel paths. Process CPU PC sampling can estimate residence
in identifiable symbols, with unknowns and sampling overhead retained; it
cannot recover IPC, LLC/dTLB misses or exact inlined operation costs. Native small-control and representative sampling is now qualified as
detailed below; whole-workload/native-helper attribution remains limited.

## Native-qualified software residence,2026-10-30

See software-profile-result.md. Small median repeated diagnostic bodies show
IR-related PC residence5.21%(no-error),3.96%(ordinaryerror),2.25%(budget
prefix). These are not whole interpreted-strategy costs or population
fractions. Most IR in the complete instrumented process belongs to the
collector/InfoTree-export phase,which is excluded from candidate bodies.

An actually accepted digits computation's ordinary C++ kernel recheck has
4258samples and0IR observations at the corrected timing point;explicit cold
RC,allocator/free and named-table residence16.42/10.85/18.25%. Helpers are
part of the kernel even without type_checker in their symbol name. AOT of
more Mathlib tactics does not remove this already native structural checking
work. Whole-workload precompile gain is unmeasured; do not turn module
census124/217 or these median samples into an overall Amdahl bound.

The genuine original-timeout-prefix stratum is separately measured in
genuine-timeout-prefix-result.md:149/1751body samples are IR-related(8.51%).
Its earlier diagnostic-median counterpart was a clipped historical pass;
the two labels and cost denominators must not be conflated. Cold RC plus
exact out-of-line inc/dec wrappers provide an explicit lower bound13.82%
at this real timeout prefix,not its complete300s execution.
