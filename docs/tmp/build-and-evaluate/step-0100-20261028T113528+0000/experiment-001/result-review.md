# Reply before retirement deadline — root self-review

The old prepared backend demonstrably returns Timeout when a complete accepted
native reply arrives within the response budget but retirement is acknowledged
later. The same protocol control fails the intended assertion on old source.
The fresh backend already preserves its timely native result while charging
retirement, so this is a backend contract inconsistency.

The fix stores a complete received reply, with its receipt deadline checked,
and waits for a valid retirement acknowledgement before returning. A timely
reply is retained if retirement crosses the deadline. Late native replies stay
Timeout; cancellation stays Cancelled; malformed retirement stays an error.
No proof execution budget, runtime flag, memory or CPU setting is increased.
Every owned child is reaped before unregistering. Existing wait4 peak metadata
is also preserved through delayed retirement; no new observer is introduced.

Two real-child/Unix-socket regression tests cover accepted, rejected and
incomplete replies, late replies, cancellation, malformed acknowledgement,
retirement cost and metadata. The modeled peak field in this fixture is not
a measured native memory value. The fixture is not Lean and does not prove
that this bug caused the real2507/7230 timeouts.

Final workspace targets pass (64 tests; five real-Lean controls remain locally
ignored), as do doctest, format, clippy and docs. The release rebuild succeeds.
Old expected failure and every raw log remain. Own-tree support peaks remain
below48GiB, with no pressure abort or monitor error. Real native CI and the
next unchanged24 qualification remain required; tests are not throughput.

The manuscript and public resource contract now state this boundary explicitly.
Scientific contract/four RQs are unchanged. Root self-review, not independent
auditing or a complete paper acceptance claim.
