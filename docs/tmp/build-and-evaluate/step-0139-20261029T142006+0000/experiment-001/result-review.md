# Result review — malformed REPL diagnostics

## Reproduced fault and correction

Before-fix regression actually exited101: env=0/messages=[null] was Accepted,
not BackendError. See [raw failing test](before-fix.log) and
[resource/command provenance](before-fix.json). Recognized envelope alone did
not establish a recognizable diagnostic.

The classifier now requires known severity and string data for every message
entry, and string values for present message/error fields. Invalid fields
yield BackendError with an operational explanation and original JSON retained.
An earlier ordinary error cannot conceal a malformed entry. The raw payload
is retained and no new cache key or option is introduced. Valid trace/info/
warning/error controls retain their prior decisions.

The subprocess fixture executes two sequential identical malformed inputs with
reuse=true; each produces one physical attempt, no cache/coalescing, an
uncacheable BackendError, original response, and fully retired owned PID.
It is explicitly a Python protocol fixture, not native Lean proof checking.

## Validation and limitations

77 Rust workspace/all-target tests passed; 6 real-native contracts remain
ignored locally. Formatting, warning-denying clippy and rustdoc pass.
Commands and complete logs are adjacent, including the initial red test.
Approved support CPUs10–11; actual combined support/native sampled peak
10470031360 bytes, below48GiB at all sampled points; no support abort.
A one-second sample is not a hard quota and support work can affect concurrent
diagnostic wall time. No second Lean collection or production mutation ran.

The existing CI runs these tests and its native contracts after push; this
report does not predeclare CI success. Pinned native compatibility and whole
workload acceptance equivalence are different evidence scopes.

## Research disposition

This repairs a semantic guarantee prerequisite, not novelty, tactic-state
failure reuse, proven false targets, full-state hit rate or saved time.
The8031-cell measurement remains frozen on aee0932 collector/ae59c77 modules.
Do not hot-change it. Its complete data, operational failures and unsupported
states remain the next research result. All original negative routes remain
frozen. Root self-review only; no independent audit.
