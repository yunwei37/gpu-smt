# Public dynamic failure-cache integration — root self-review
The existing engine uses trait objects for pluggable backends,but the standalone
FailureCache has an implicit Sized constraint. Verify a public consumer using
dyn FailureReplayBackend and an exclusively owned Send/notSync state. First
compile that real public usage against current API;then remove only the
unnecessary Sized bounds.

Run asynchronous consumers to test actual in-flight record ownership and
metadata-lock separation:clear while two replays are suspended,live generation
change while suspended,and cancelling one consumer without affecting another.
Each transition still returns its native ordinary exception and charges once.
Fixtures are explicitly simulated,not native state replay qualification.
No production hook,backend implementation,dependency or runtime flag is added.

G10 development only,CPU6–7,compact one-job builds/outputs onPVC. Native captures
remain stopped on signal denial.12GiB/6GiB/API requirements remain unchanged.
Run focused public/old failure fixtures,all-target clippy,fmt,rustdoc,existing
full CI after publication. Preserve the red compiler result and all outcomes.
