# ProofServe

**A Lean verification service with a Kimina-compatible API.** Submit batches
of proof candidates and receive ordered results with original Lean diagnostics.

In a matched miniF2F run under the same four-core/48GiB resource budget,
ProofServe was **1.24× faster**, with identical final statuses and accepted IDs.

| 7,808 candidates | Elapsed | Accepted |
|---|---:|---:|
| Four warm Kimina REPLs | 25,176.49 s | 3,014 |
| ProofServe with Mathlib preparation | 20,323.01 s | 3,014 |

[Benchmark data and protocol](bench/lean-warm-resource/README.md) include
retry-order, CPU-eligibility and raw-diagnostic differences. The result is one
measured comparison; it is not a guarantee for every workload or isolated COW gain.

## Quick start

Full Mathlib container qualification is still open: the tested prepared path
times out even with a 180-second budget. The entrypoint now uses the existing
fresh-REPL default; that correction still needs a full image recheck.
[Qualification results](docs/releases/0.1.0.md#corrective-qualification-result-and-closeout).

The pinned Linux x86-64 recipe is available for testing:

~~~sh
docker build -t proofserve . && docker run --rm -p 127.0.0.1:3000:3000 proofserve
~~~

The recipe pins Lean 4.18.0, Mathlib and REPL at fixed revisions. You do not
need to supply a Lean installation or project. The first build downloads the
toolchain and Mathlib cache. CPU and memory defaults are discovered automatically;
research CPU IDs and a 48 GiB machine are not required.

Then submit a proof:

~~~sh
curl http://localhost:3000/check -H 'Content-Type: application/json' \
  -d '{"snippets":[{"id":"one","code":"import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num"}],"timeout":180}'
~~~

[Environment and resource options](docs/getting-started.md).

## Python client

~~~sh
pip install ./clients/python
python examples/check_batch.py
~~~

~~~python
from proofserve import Client

response = Client("http://localhost:3000").check(
    [{"id": "one", "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num"},
     {"id": "two", "code": "example : False := by decide"}],
    timeout=180,
)
for result in response["results"]:
    print(result["id"], result["response"], result["error"])
~~~

No Python runtime dependencies. The core /check shape follows Kimina:
snippets, timeout, reuse and ordered raw results. An absent transport error
alone is not acceptance: inspect Lean messages and sorries.
[Client](clients/python/README.md) · [API scope](docs/api.md).

## Rust crates and CLI

~~~sh
cargo build --release --locked -p proofserve
target/release/proofserve --help
~~~

| Package | Role |
|---|---|
| proofserve-core | Requests, outcomes and extension traits |
| proofserve-engine | Admission, scheduling, resource accounting and reuse |
| proofserve-lean | Native Lean REPL and source backends |
| proofserve | HTTP service and CLI |

[Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md) ·
[Changelog](CHANGELOG.md) · [Prepared release notes](docs/releases/0.1.0.md) ·
[Apache-2.0](LICENSE).

Version 0.1.0 is being prepared. No published registry image, crates.io package
or stable binary release is advertised here. The corrected Docker recipe still needs full environment qualification.
[Research status and retained results](docs/research-status.md) ·
[Reproduction](bench/README.md) · [Paper](docs/paper/main.tex).

Research inputs and failed/partial results remain in the repository; they are
excluded from published crate packages and Docker build context.
