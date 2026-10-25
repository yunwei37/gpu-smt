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
