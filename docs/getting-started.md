# Getting started

## Pinned environment

From the repository root:

~~~sh
docker build -t proofserve . && docker run --rm -p 127.0.0.1:3000:3000 proofserve
~~~

The recipe targets Linux x86-64 and fixes these inputs:

| Component | Version |
|---|---|
| Rust |1.98.1|
| Lean |4.18.0|
| Mathlib |aa936c36e8484abd300577139faf8e945850831a (v4.18.0)|
| Lean REPL |2f0a3cb876b045cc0fe550ca3a625bc479816739|

Both upstream Lean toolchain files select 4.18.0. Dependencies and cache are
downloaded at build time. The full Docker build is pending its first bounded
qualification attempt; see the release notes for the actual result.
No image is published. The .dockerignore excludes research data and reports
without moving or deleting them.

## Resources

The CLI discovers eligible CPUs and visible cgroup-v2 ancestor CPU quotas.
Its startup sampled-RSS budget is80% of current available memory, bounded by
remaining visible cgroup-v2 memory capacity. Explicit --cpus, --worker-cores and
--memory-gib select a specific measurement/deployment point. Existing research
captures keep their original explicit resource points.

The resource monitor samples owned RSS; it is not a kernel hard memory limit.
Cgroup-v1 controller limits are not currently auto-discovered.
The existing operational watchdog is not a semantic assumption of the research
mechanisms; native heartbeats/limits and rejection semantics are analyzed separately.

## An existing Lean project

Build the Rust executable, then from your Lean project:

~~~sh
lake env ../proofserve/target/release/proofserve serve \
  --repl ../repl/.lake/build/bin/repl --project . \
  --environment your-toolchain-and-project-version
~~~

Paths are relative to that project. This advanced path requires a matching
REPL; Docker supplies it automatically. The environment ID identifies the
immutable backend/toolchain/project context used for cache separation.

## Batch results

Install with pip install ./clients/python, then run examples/check_batch.py.
The /check API preserves IDs, input order, original Lean errors and sorries.
Debug/infotree extensions and persistent remote env handles are outside the
current compatibility scope. The typed /v1/verify endpoint provides explicit
accepted/rejected/incomplete/operational outcomes.

Use all-candidate mode for RL rewards. First-success mode can cancel siblings
after a checked same-task success; cancelled candidates are not RL rewards.
The service alone does not certify a tactic-failure/read-set cache.
