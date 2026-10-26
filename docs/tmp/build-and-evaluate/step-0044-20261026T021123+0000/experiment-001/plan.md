# Retain complete native diagnostic events outside bounded stderr tails

The real source backend drains stderr but retains only64KiB. The23simp_all and
48interval instrumentation emit structured stage events there; tail-only Capture
cannot support complete per-request attribution. Implement optional Rust
per-attempt stderr files, named by actual PID/birth and linked from backend
events. Keep normal stdout/stderr classification, defaults and resource/cleanup
paths unchanged. A log I/O failure is operational, never proof acceptance.
No source/prover rewrite, diagnostic-signal reinterpretation or new service.

Forward all stderr bytes to an asynchronous file while maintaining the existing
bounded response tail. Flush before attempt completion and report complete/error
provenance; do not claim fsync/power-loss durability. Caller supplies an existing
directory, original source remains byte-exact, measurement uses reuse=false.
Public configured builders may compose argv/original-file/log directory without
adding fields to existing NativeLean literals. CLI option explicitly requested
by the diagnostic invocation, no logging directory/file by default.

Real subprocess fixture produces >64KiB valid event rows to prove head/tail
retention, exact bytes and PID/birth attribution. A missing directory checks
operational failure/reaping. Existing pinned-native file contract also exercises
configured logging; compile locally and execute existing CI. No additional
Workspace native candidate group while the sole full pair runs. Monitor combined
full+development RSS under48GiB and useCPU10–11 for ordinary checks.
