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
cannot recover IPC, LLC/dTLB misses or exact inlined operation costs. The C
control is qualified; Lean sampling is not yet qualified.
