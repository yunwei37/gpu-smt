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
