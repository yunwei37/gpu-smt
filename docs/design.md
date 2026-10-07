# Design frontier

BOOTSTRAP; intended design is not implemented or frozen. Current hypothesis: retain exact native preparation in immutable states, then isolate each candidate in a disposable branch. Independent job history, scope, solver configuration and request resource semantics matter separately from logical assertions.

Root owns the [Initial Narrative and RQs](idea-story.md). The proposed mechanism needs supported quiescent boundaries in both Z3 and Lean, bounded shared-state placement and complete cancellation behavior. A native library driver or REPL hook is acceptable implementation glue but must not be described as transparent reuse of an untouched executable. Fallback must preserve native behavior; fallback on UNKNOWN alone cannot detect the observed reverse UNKNOWN-to-UNSAT change.

No claim of novelty for fork/COW, warm REPL, flat arrays or delayed substitution. Mandatory closest-work grounding is complete and shows high overlap; native safety, observable qualification and consequential differentiation remain unresolved. The first full API-constructor probe fails original-interface qualification, so its branch is a diagnostic path and cannot enter the service. A GPU checker direction is retained as a serious competing route, pending measured dynamic work and critical paths. RTX 5090 only.
