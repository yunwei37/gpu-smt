# Executable engine examples

Build cargo build -p gpu-smt-server, then from the Lean project supply your actual stock REPL and
matching project/toolchain identity:

    lake env /absolute/path/to/gpu-smt/target/debug/gpu-smt check \
      --repl /absolute/path/to/repl --project /absolute/path/to/project \
      --environment lean4-project-pin --cpus 8,9,10,11 --worker-cores 1 \
      --memory-gib 48 < /absolute/path/to/gpu-smt/examples/check.jsonl

The source inputs include an accepted core proof, a false decide attempt and
an admitted proof. These are correctness controls, not real generated workload
or performance evidence. Native environment setup/imports are required.

Use serve instead of check to expose local /check, /verify and /v1/verify.
See [API](../docs/api.md) for core Kimina schemas, explicit unsupported options
and differences between all-candidate RL and first-success consumers.
No service is deployed by building or running tests.

To capture a complete batch and compare engine policies, use the documented
[measure/compare commands](../docs/benchmarking.md). The input to measure is
one Batch object; check accepts one Batch per JSONL line. Keep stderr resource
logs and an external lifecycle clock alongside captured native results.


## First-success task ordering

The [first-success input](first-success.json) contains one solvable task and
one rejected-only task. An admitted proof is deliberately included: it remains
incomplete and cannot cancel its siblings. A checked winner may cancel remaining
same-task work; the rejected-only task still exhausts its candidates. Native
results remain in original input order. These are controls, not a benchmark.

    lake env /absolute/path/to/gpu-smt/target/debug/gpu-smt measure \
      --repl /absolute/path/to/repl --project /absolute/path/to/project \
      --environment lean4-project-pin --cpus 8,9,10,11 --worker-cores 1 \
      --memory-gib 48 --policy task-interleave \
      < /absolute/path/to/gpu-smt/examples/first-success.json \
      > first-success.capture.json 2> first-success.resources.jsonl

Use the same policy with mode all when every candidate reward is required;
it delegates FIFO and performs no first-success cancellation. Exact reuse
remains controlled by each candidate's reuse field.


Preview the policy through the public Rust traits without starting a verifier:

    cargo run -p gpu-smt-engine --example task_order \
      < examples/first-success.json

This prints candidate order only; it does not validate proofs, perform resource
admission or produce benchmark performance.

## Opt-in measured sibling memory

Library callers can pass Arc::new(TaskInterleave::new(TaskMemory::new(Fifo)))
as Engine::new's policy. Import the three policy types from gpu_smt_engine.
The compiled public TaskMemory example documents this composition; it does not
start a verifier. Existing CLI defaults and frozen collections are unchanged.
The executable now exposes TaskMemory::new(Fifo) as --policy task-memory for
check,measure and serve. It keeps FIFO ranking;the library composition above
also adds task interleaving. See the [matched measurement recipe](../docs/benchmarking.md#measured-same-task-memory-policy)
before starting a native comparison. Existing Capture.policy identifies the
chosen method;no extra collection tool is required.

The wrapper uses only measured physical-attempt peaks after retirement to
refresh same-task waiting reservations. It shares no native verdict, prefix or
certificate. Observations are separated by backend/resources and timeout;
unknown tasks keep their original forecast. Use a fresh wrapper per workload
or clear_memory. A heavy sibling can cause overreservation. Keep normal
admission/watchdog/exclusive retry and qualify on native workloads before any
performance claim; fixture tests are not that qualification.
[Existing official4.18nativeCI controls](../docs/tmp/build-and-evaluate/step-0072-20261027T044950+0000/experiment-001/result-review.md)
now execute actual feedback/raw-response checks,not original4.9performance.

## Matched native/prepared resource pair

Build the reusable API example with cargo build --release -p gpu-smt-server
--example resource_pair. Its --help documents eight positional inputs:one Batch
JSON,matching native REPL/project/prepared-host/sysroot/environment,one Config
JSON,and a fresh output directory. Run from that native project's lake env.
The example starts no verifier when invoked with --help.

Both conditions use the exact same Batch,Config,FIFO and native context.
The driver uses the existing Rust admission/watchdog/exclusive-retry path.
Capture compression is an owned gzip child and is always retired;gzip is a
runtime dependency of this example. Complete cell clocks include serialization
and compressor retirement;the inner Capture clock retains its narrower scope.
RSS/CPU-tick records keep missing process observations explicit. CPU tick rates
need the measured system CLK_TCK to interpret;leader count is not CPU busyness.

Only run when the owning collection slot is free. A four-core configuration
permits up to four workers subject to actual memory and cleanup. Supporting
fresh/prepared comparisons do not establish a strongest warm-service advantage
or novelty. [Prepared original-workload scope](../artifacts/engine-resource-pair-2026-10-25/preparation/README.md)
is distinct from executed performance.

The resource_pair example flushes attempts.jsonl after each physical backend
attempt and results.jsonl after each final consumer BatchEvent from the existing
stream API. These are different: watchdog classification and retry history can
change a backend cancellation into a final engine result. The consumer journal
preserves original indices, IDs, native responses, histories and elapsed clocks;
the complete Capture keeps original submission order.

A validated Complete event covers all consumer rows, not idle-backend shutdown
or whole-cell completion. EOF without Complete is partial. Capture/terminal
remain the whole-clock and lifecycle authority. A handled SIGINT/SIGTERM stops
the pair after cleanup and retains interrupted records; a journal I/O failure
also awaits owned retirement before returning an error. Flush is not fsync or
a power-loss guarantee. No automatic resume or reconstructed missing outcome
is implied.

Both paired conditions include consumer-journal I/O in their own cell clocks.
Older captures without results.jsonl remain unchanged; do not pool recording
versions or expect an in-progress old executable to gain this file. No active
collection should be rebuilt or restarted to adopt this observation change.
