# E1082 — publicly buildable current oracle source
Scope: package the actual measured Rust/Lean implementation and a portable
build/verification entrypoint; keep frozen capture libraries, sources, resource
settings and all experiment outputs intact. This is reproduction/compatibility
work within the ongoing RQ4 experiment, not new systems novelty.
Read user-instruction/questions/InitialNarrative and current result first.
All work/review is root only, explicitly self-review.

Publish the entire currently executed numerical crate plus the Lean4.27
adaptation and necessary C shims. Preserve upstream Apache2 license/notices
and name modified derivations. Build in a fresh output directory, using normal
Rust/Lean tools and a caller-supplied Mathlib project; do not mutate the retained
Mathlib native libraries used by active captures. No private workspace path in
public build logic and no new service, scheduler, clone or checkout.

Verify source-body correspondence, real compilation, existing meaningful
numeric tests and actual released accepted/rejected Lean candidates.
Functional qualification is not a new timing result or a byte-identical
executable promise. Current full-version Goedel/formal captures remain separate.
Portable compiler/linkage differences must be reported honestly; they cannot
replace the measured implementation without fresh qualification.
