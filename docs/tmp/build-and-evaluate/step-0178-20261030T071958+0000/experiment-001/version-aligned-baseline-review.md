# Version-aligned native baseline — offline source self-review

30 October 2026. These are source facts at exact Lean tags, not new native
measurements. No Workspace, SDK installation, build, test or security change.

| Source/version | Verified boundary | Consequence for this paper |
|---|---|---|
| 4.9.0-rc1 core ordinary decide | Its handler reduces the Decidable instance in the frontend, then returns a proof term whose kernel check recomputes the decision. | M's separately timed declaration rechecks omit this frontend stage; their rate is not a complete tactic cost. No 2× overhead is measured. |
| 4.9.0-rc1 mkAuxLemma | A type-indexed auxiliary-lemma cache with level-parameter matching already exists; its table is not serialized in .olean. | Generic auxiliary-lemma caching is older native behavior. Its presence alone does not show the ordinary decide handler uses it. |
| 4.9.0-rc1 core grammar | The core decide syntax has no configuration argument; the native_decide route is separate. | Do not copy a modern +kernel option into the old control and call it an existing qualified baseline. Project-specific extensions were not surveyed. |
| 4.34.1 decide +kernel | The kernel route constructs a proof and calls mkAuxLemma, which can reuse an existing auxiliary declaration. | Static occurrences in the OpenAI release do not imply separate expensive checks or costs predicted by the 4.9 sample. |
| 4.34.1 mkAuxLemma | The key includes type, privacy and defeq flags, with level-parameter matching; the table remains local to the environment branch. | No cross-request hit rate, corpus timing, generic failure cache or new reuse mechanism is established. |

The 4.9 handler is in ElabTerm.lean. A request for the modern Decide.lean path
at that tag returns 404; that is a path/version mismatch, not absence of the
tactic. The actual old handler and parser were then inspected. Conversely,
BuiltinTactic.lean does not contain the old handler. These lookups do not
justify feature-negative conclusions from a missing filename.

## Primary sources inspected

- [4.9 ordinary/native handlers](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Elab/Tactic/ElabTerm.lean#L330), lines 330–383.
- [4.9 grammar](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Parser/Tactic.lean#L114), lines 114–129.
- [4.9 auxiliary cache](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/Meta/Tactic/AuxLemma.lean#L11), lines 11–38.
- [4.34 kernel route](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Elab/Tactic/Decide.lean#L65), lines 65–112.
- [4.34 cache implementation](https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Meta/Tactic/AuxLemma.lean#L14), lines 14–74.

## Manuscript disposition

Add one short Evaluation explanation of the omitted frontend phase, with one
exact-version primary citation. Preserve all previous citations and the frozen
Related-work section. Do not assert a version-to-version speedup, upgrade the
retained control, replace original candidates, or change the paper mainline.
Full 11.007 s remains the observed sample process clock; 2.894 s remains the
extra warm-recheck subtotal inside it. No stage percentage is inferred.

The no-axiom outputs remain actual native evidence for the five bounded
sample theorems. They do not cover the full grid or every compiled dependency
of a different released corpus. Official source inspection verifies the
intended code path; it is not a fresh run of the installed binary.

## Heartbeat-unit and counter-scope follow-up — self-review

Exact-tag public source inspection on 30 October 2026, without native execution:

| Boundary | Source finding | Interpretation |
|---|---|---|
| Public option to wrapper integer | Core.getMaxHeartbeats multiplies the public option by 1,000; Environment.addDecl passes this result to addDeclCore. | The public value 200,000 maps numerically to 200,000,000 at this wrapper. M instead supplies the literal 100,000,000 directly. This does not establish equal work allowances. |
| Meta/runtime observation | IO.getNumHeartbeats calls allocator get_num_heartbeats; the small allocator increments its heap counter on a small allocation. | This is the counter family observed by Lean metaprograms, not elapsed seconds, peak RSS, or a kernel-step count. The allocation build configuration matters. |
| Kernel checking | lean_add_decl scopes the kernel maximum; type checking/reduction invokes check_system, whose interrupt path increments a separate thread-local heartbeat counter. | The source uses a separate counter and increment event. The same word or integer scale does not make the two event counts interchangeable. |
| Scope and remaining allowance | scope_max_heartbeat changes/restores the maximum, not the counter itself. This bounded inspection did not establish every outer reset or starting count for the retained binary. | Do not call M's literal a fresh per-tactic allowance, a remaining-command allowance, or proof of budget parity. No conclusion about a particular sample's prior counter value is made. |

The thread macro defines file-local static storage for the interrupt counter
and allocator fallback counter; their same variable spelling does not identify
one shared counter. With the small allocator, its counter is a heap field.
No conversion from either counter to wall time or RSS is justified here.

Primary pinned files: [CoreM](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/CoreM.lean),
[AddDecl](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/Lean/AddDecl.lean),
[IO](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/runtime/io.cpp),
[allocator](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/runtime/alloc.cpp),
[interrupt counter](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/runtime/interrupt.cpp),
[thread macros](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/runtime/thread.h),
[kernel entry](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/kernel/environment.cpp),
and [type checker](https://github.com/leanprover/lean4/blob/v4.9.0-rc1/src/kernel/type_checker.cpp).
Function names, rather than line numbers from differently rendered HTTP views,
identify these source facts.

Disposition: add one sentence to the existing sample-method paragraph that
explicitly withholds remaining-heartbeat parity. Keep the literal API argument,
observed sample outcomes and measured clocks unchanged. No new bibliography
entry is needed for this limitation; the detailed source trail lives here.
This does not qualify failure replay, resource-failure monotonicity, a generic
speedup, or an original-candidate comparison. The mainline and RQs stay fixed.
