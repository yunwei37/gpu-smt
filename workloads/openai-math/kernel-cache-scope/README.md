# What a goal-type census can and cannot count

Native SDK: Lean4.34.1, commit5045d0056413266e57c625dcd7c365b10e377c52.
Source inspected directly in the installed pinned SDK:
[Decide.lean lines104–118](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Elab/Tactic/Decide.lean#L104)
and [AuxLemma.lean](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Meta/Tactic/AuxLemma.lean#L14).

doKernel builds a decide proof and calls mkAuxLemma for expectedType, using
ambient-ordered level parameters and async=false around that call.
AuxLemmaKey contains type, isPrivate (!env.isExporting), and defeq.
Lookup also requires equal ordered level-parameter lists. Private contexts
may reuse a public matching entry. The local environment extension is not
serialized into .olean; its documentation promises reuse in the same
environment branch and points to realizeConst for cross-branch deduplication.

Consequences for the 1,354,379 source occurrences:
- Global equal printed annotations do not imply equal elaborated Expr values.
  The same spelling may refer to different constants in different namespaces.
- Equal Expr values in separate modules/branches are not automatically one
  existing cache computation. Module identity alone can also omit branch
  scope; global and per-file text counts are neither exact runtime misses
  nor complete proof-checking costs.
- A private declaration's name is not a direct observation of the producer
  environment's isExporting flag. Our serialized-theorem census deliberately
  distinguishes that observed name flag from actual cache eligibility.
- The defeq flag and level-parameter order matter. For the inspected
  doKernel call, mkAuxLemma uses its default defeq=false.
- Merely loading an already checked declaration avoids rechecking that
  declaration, but does not mean a new decide call in a fresh module hits
  the old nonserialized local cache.

The measured [135-object census](../native-type-keys-135/) contains45source
decide+kernel calls,45recognized direct proof helpers and45distinct native
Expr types. It does not establish whole-repository cache miss count or
weighted CPU work. The [16 repeated annotations](../repeated-goal-probe/)
still require their real imports before native elaboration; no replacement
axioms or generated proofs are used. Whole-repository distinct native goals,
cache-miss count, and kernel-compute cost remain unknown. Earlier text-only
881,548 explicit annotations/489,445 global strings/472,831 unresolved calls
must retain those lexical qualifications.
