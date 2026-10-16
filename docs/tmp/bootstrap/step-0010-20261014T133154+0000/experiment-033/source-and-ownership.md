# Actual source/ABI and observer ownership

Lean/Expr.lean's computed_field declares data : @& Expr -> Data under
extern lean_expr_data. Its UInt64 cached bits40/41/42/43 and44+ encode free/
expression-meta/level-meta/level-parameter/loose-bound-range. The wrapper calls
this borrowed metadata getter twice and preserves native object ownership.
Actual generated has*Ex export helpers consume their Expr; these are deliberately
not used without increments. No Expr contents, options, caches or state are
changed.

The generated Meta export has six lean_object* inputs and lean_object* result.
Private clang link reuses the existing original REPL objects and SDK libraries
with --wrap=lean_is_expr_def_eq, outputting a separate native executable.
Both compile and link return0; nm finds wrap and real symbols. Same-object/
private recursion can bypass wrapping, so this is observed export coverage only.

Per-thread MAP_SHARED aggregates avoid relying on destructor/exit flush when
the original backend kills native workers. No per-call I/O or cross-process
mutable Expr access is introduced. Native outcomes and any partial/clock/init
observation failure stay retained. No source/SDK/active executable is overwritten.

This is build/dependency qualification. Only the real original HTTP preflight
and full population can establish executable engagement and useful cost evidence.
No speedup/independent review is asserted.

## Linker coverage clarification

The existing instrument observes references rewritten by --wrap during this
private static link. In addition to private/same-object recursion, runtime-loaded
DSO references can resolve the original exported symbol rather than the wrapper.
Both symbols remain in the executable. Counts/timing therefore describe the
observed wrapped calling paths, not every dynamic entry at the native symbol.
No total Meta coverage, negative conclusion about all variable-free checks,
or transfer of E032's35%CPUweight follows. This limitation qualifies selection;
it does not change the operation, native run or source population.
