# Interval first-stage mapping implementation and pending native comparison

Selected fixed RQ2: "Does branching from prepared native state preserve verifier
responses and requested artifacts while isolating candidates and cancellation?"

This is a user-requested direction1 component implementation/behavior-risk
diagnostic, not a standalone state-branching experiment or answer to RQ2.
Source transformation must be qualified before it can enter that service.
The fixed paper population, accepted-set requirement and metrics do not change.

Question: can interval construction invoke only the first pruning stage while
preserving surviving goals and the later native stage suffix? The old callback
requires every leaf closed and moves the entire closer inside all interval
traversals. This new opt-in map is a different implementation, not a failure
certificate, global goal refutation or transparent timeout shortcut.

Use retained Mathlib4.9 Methods and original48 native AST. Retain the old module
and prepared data. New map collects surviving goals in traversal order; use
native all_goals for continuation recovery/error logging; restore entry state on
propagated construction error. Interleave only the first post-interval tactic,
leaving the exact original suffix outside. Control sources import the same new
module without replacing native tactics.

Current allowed execution: definition compilation, offline source preparation,
native grammar inspection (never elaborate candidate proofs), byte-inverse and
stage-suffix checks. Sample controller/compiler plus the active sole fullpair
within48GiB on CPU11; withdraw only new compiler on pressure. Do not alter the
loaded fullpair release, old module qualification or start another acquisition.

Pending sole-slot execution: native controls vs mapped variants including open
survivors, stage order, recovery, nested Nat/Int, outer goals and rollback; then
original48 import-control/map matched native invocations. Measure full command
costs, outcomes, timeout/resource failures, and actual memory. A compiler/parser
pass does not establish parity, performance, failing-branch soundness or
inevitable timeout. Any recovered elaboration error remains a native rejection,
not an accepted proof. All original cohort outcomes and original71 reliable
failure coverage remain unknown until executed. Existing closed-tail0/71 is
frozen and not extended. No CPU oracle work, competitor or extra full capture.
