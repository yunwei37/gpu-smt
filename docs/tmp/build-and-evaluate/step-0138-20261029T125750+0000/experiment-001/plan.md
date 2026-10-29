# Rust source-backend panic classification regression

User requests Rust engine implementation/testing while the single native
measurement runs. Scope:classify_source runtime-fatal stderr precedence and
its regression/docs only;must not alter native source,requests,admission,
timeouts,cache identity,ordinary error handling or running measurement.
Current code returns Rejected when an earlier recognized JSON error precedes
a later native INTERNAL PANIC. That status is cacheable despite incomplete
native execution. A runtime panic must remain operational/uncacheable;ordinary
JSON errors without a panic remain rejected. Retain all original bytes.

Reproduce through the public Rust classifier using the actually observed
Nat.powpanic marker and an explicitly composed preceding JSON diagnostic.
This is a boundary fixture,not a claimed fresh source-CLI native capture.
Use the existing Rust workspace toolchain/target and tests,CPU11support with
combined own-memory sampling;no new native collection or dependency.
