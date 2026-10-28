# Repair monitor retention without changing admission semantics

Prune only identities that strict native stat confirms are gone or have a changed
birth. Keep every live known descendant,including those no longer discoverable
under its original parent. A stat access error remains an error;do not silently
discard memory. No RSS/CPU/AS/forecast/deadline/scheduling default changes.

Regression tests use actual owned helper processes,wait for readiness,then check
exit/reap pruning and live/wrong-birth accounting. Run existing workspace tests,
clippy and format checks. No Lean candidate collection while FIFO remains active;
the existing combined helper/tree monitor protects supporting builds/tests.
The current frozen binary remains unchanged;future native qualification and
warm pairing must use the repaired source and retain initial failures.
