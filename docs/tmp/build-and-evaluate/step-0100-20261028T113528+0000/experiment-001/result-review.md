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

## Verified followthrough

The first-fix source a750aa3 completes engine CI40682324445, including real
native-repl-contract and Rust jobs, and benchmark-smoke40682324462. Metadata
is retained in first-fix-source-ci. These CI results belong to a750aa3.
A forward strict-receipt guard additionally requires the recorded timely flag
on the normal operation-complete path, avoiding a ready-IO/timer race. Its
workspace targets, clippy, format and release build pass separately; current
source CI must be checked after this forward commit.

The manuscript compiles in the owning Workspace (exit0,36 pages). The generated
PDF is rendered read-only; changed page5 and adjacent pages4/6 are visually
inspected without clipping or overlap. paper-check.json records the scope.
The four RQs, abstract/introduction and scientific contract are unchanged.
This is a targeted implementation description, not a full writing review.

The response/retirement fix remains unmeasured on the real24 candidates.
Preserve original300-second budgets and all reference clocks/failures. Native
CI and a separately pinned unchanged24 run follow; do not claim this caused
the previous2507/7230 timeouts or achieved full-population parity.
