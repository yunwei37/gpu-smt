# Plan — preserve native runtime failures as operational outcomes

2026-10-26; BUILD_AND_EVALUATE; root thread only; parent step0065.
RQ2 asks whether branching preserves verifier responses and requested artifacts
while isolating candidates and cancellation. This is a repair dependency of
that comparison, not a new research experiment or contribution.

Actual original71 experimental data contain three native exit1 responses with
empty JSON diagnostic arrays. The source adapter currently maps every nonzero
exit to Rejected, conflating runtime recursion failures with proof errors.
Use those three exact retained response envelopes as regression input, first
demonstrate the defect, then require a recognized JSON error to establish
Rejected. Unknown nonzero exits become BackendError, with raw payload retained.
Existing logical-error, admission, resource and protocol controls must keep
their distinct outcomes. No native source or historical status is rewritten.

Run library/transport regressions and clippy on CPU11. No new Lean collection,
no logger/parser/observer expansion, and no rebuild of the active CLI.
Measure this support process plus the active owned capture tree; terminate
support work first on budget pressure. Capture remains the sole native group.
Record compiler/test clocks and overlap. Publish at a complete repair boundary.
Then continue interval48 actual completion and original lean-mlir, and use
existing simp23 evidence/source to assess a sufficient detector, never hashes
or runtime crashes as proof. Self-review only, no independent audit.
