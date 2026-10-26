# Preserve runtime failures as operational outcomes

Three exact native response envelopes from the completed original71 simp_all
diagnostic run are regression inputs in
[the fixture](../../../crates/gpu-smt-lean/tests/fixtures/source-runtime-failures.json).
They exit1 with no JSON proof-error messages. The old source frontend returned
rejected; the corrected source returns backend_error, preserves each full
native response, and gives an explicit missing-error-diagnostic explanation.
Historical captures are untouched. A runtime crash is not a proof that a
candidate is false or an early-failure method.

The observed-response regression fails before the fix (red-001, cargo101),
then all4 library tests pass (green-001). Seven single-CPU process/transport
tests pass. The first transport invocation also attempted an existing test
requiring two eligible CPUs; its CPU-list unwrap fails under this support
runner's single CPU11 affinity. That failed log is retained; transport-002
explicitly skips this inapplicable test. No new two-CPU watchdog qualification
is claimed. Clippy with warnings denied and formatting both pass.

An initial support-runner invocation failed before cargo because its artifact
parent was absent; setup-failure.txt preserves this detail. The existing
step0062 support runner is reused with the current interval48 controller,
CPU11 and the same1s combined-tree RSS sampling. Recorded combined peak is
49,195,057,152 bytes (45.816 GiB), below the48GiB budget; no support abort or
monitor error. Compilation/tests can contend with the active capture and
are not an isolated performance run. The native collection and its CLI binary
are unchanged; the native body executes zero additional diagnostic candidates.
All receipt/source/log bytes are retained, with lossless gzip of closed streams.

This is a real bug repair and dependency qualification, not an additional
scientific result, full-population parity or independent audit. Root self-review.
