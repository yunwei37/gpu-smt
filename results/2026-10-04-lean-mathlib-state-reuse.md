# Real Mathlib proofs with established Lean environment reuse

Official Lean checking of 52 complete published Mathlib proofs and controlled
negative/incomplete variants finished in three passes per mode. Every decision
matched its expected category. An established REPL with environment backtracking
avoided repeating the validated source prefix and had a median corpus makespan
of 7.893 s versus 114.891 s for cold Lean. Substantial run variability limits
performance inference. This is a real-library frontend experiment, extending
the earlier fixed export-fixture prototype; it is not a new REPL design or a
collected agent candidate stream.

## Workload, state and correctness

Source is [Mathlib/Data/Nat/GCD/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/Mathlib/Data/Nat/GCD/Basic.lean),
revision `d13f23b723b8a846827a245b89c10fc7d3f11612`, Lean 4.34.1.
`bench/lean-source-trace` elaborates the original file normally and emits
parser-observed byte spans. It reported no errors. The harness selects 52
theorem/lemma commands from those spans, retaining complete original imports,
source prefixes, proof bodies and intervening commands. Counts are observed
source-command counts, not inferred export declarations.

For each theorem, candidates run in this order:

1. `by exact (0 : Nat)`: a controlled type error, expected rejection.
2. `by sorry`: incomplete, kept distinct from rejection and acceptance.
3. The exact published original proof: expected acceptance.

Lean accepts `sorry` with a warning; the harness checks warnings and REPL
`sorries`, rather than treating exit 0 or an environment ID as proof completion.
All 468 original-proof checks accepted, 468 mutations rejected and 468 `sorry`
variants were marked incomplete across nine complete runs. Each name, variant,
decision and complete response is retained. This finite subset does not prove
general semantic equivalence or certify all of Mathlib. The source's imported
compiled environments are shared dependencies of all modes.

The baseline is the existing [leanprover-community/repl](https://github.com/leanprover-community/repl),
which already supports persistent commands/tactics, environment IDs, backtracking
and pickling. We used its v4.34.0 source at
`193cf4bb9a22bb3fc6d25774f0fe6a70db1fd6ee`, built with a local Lean 4.34.1
toolchain override to match Mathlib (no v4.34.1 REPL tag was available).
These gains are evidence for established warm state reuse, not novelty from
reimplementing it. Pickling was not measured.

## Compared paths and observed elapsed times

`bench/lean_repl_workload.py` uses one CPU, affinity 0, checking enabled.
Every candidate sees only the original source prefix preceding its theorem;
the theorem under test and later results are not imported in advance.

| path | state lifetime | corpus makespans, seconds | median |
|---|---|---|---:|
| cold Lean | fresh process, complete prefix + candidate each job | 108.073 / 281.176 / 114.891 | 114.891 |
| REPL fresh command | process per theorem's three candidates, each reconstructing full prefix | 496.751 / 212.413 / 216.642* | 216.642 |
| REPL validated prefix | one process, all variants branch from the previous validated environment | 6.745 / 17.434 / 7.893 | 7.893 |

`*` The final fresh-command pass was interrupted after 59 responses. Its original
records remain intact. A separate resumed invocation reran that full 156-job
pass, producing 216.642 s. The other eight completed runs were not repeated.
The summary explicitly identifies this resumed run; its local repeat index 0
does not duplicate the initial pass. The 59 partial responses are excluded from
complete-run counts and elapsed comparisons.

The ratios of medians are 14.56× cold/prefix and 27.45× fresh-command/prefix.
They compare this harness's fixed-corpus frontend makespans, including process
setup, imports, prefix proof construction/elaboration/checking, responses,
recording and teardown. They are not isolated kernel speedups, export replay,
per-request latency under arrival load, or evidence of maximum attainable Lean
acceleration. There is no theorem search beyond replaying original tactics.

Rejected and incomplete variants never advance the validated prefix. Only the
original accepted proof supplies the next environment ID. Between-proof aliases,
variables and other commands are included in each branch. Thus the saving is
avoided re-elaboration/rechecking of an already accepted prefix plus warm imports,
rather than a result cache that returns old decisions without checking candidates.
Per-call response times are retained; makespan/job is only amortized throughput.

Mode order was reversed in the middle repeat. Full cold times varied by 2.60×,
prefix by 2.58× and fresh command by 2.34×. The contemporaneous pressure snapshot
shows CPU contention and recent memory pressure; other work was not isolated.
VeruSAGE capture/replay ran on affinity 8–15 / 8 concurrently, and the final
fresh pass ran after session interruption. These observations cannot identify
the cause of each timing difference or support confidence intervals from three
trials. CPU 0 is in the higher maximum-clock group; CPU 8 is in a lower-clock
group. Do not compare Lean and SMT per-core costs as equivalent hardware.

## A negative memory/lifetime result

An initial fresh-command design kept one REPL for the entire corpus while
creating a new imported environment for every command. REPL retains returned
environments for backtracking; this design accumulated tens of GiB, reaching
71.6 GiB in a process RSS sample (75,092,744 KiB). It was stopped gracefully through the
experiment parent; raw partial records are retained. Its partial timing is not
used as a speedup baseline.

The bounded fresh-command baseline releases a process after each theorem's
three variants. Completed prefix runs sampled approximately 0.78–0.85 GiB RSS;
bounded fresh-command samples reached about 3.87 GiB. These are sampled
post-response RSS values, not process peak RSS, isolated memory use or fleet
PSS. The unbounded lifetime failure is a practical caution for serving many
fresh imported states, not a claim that ordinary REPL prefix reuse has that
memory behavior.

## Reproduction

Pinned source, spans, all candidates/contexts, versions, hashes, complete
responses, interruption records, build logs and summaries are retained in
`artifacts/lean-state-2026-10-04`. Existing checkouts/builds stay in the owning
workspace. New output directories are required to keep runs distinct.

```bash
# Build the parser-span tracer in bench/lean-source-trace:
PATH=/root/.elan/bin:$PATH lake build
# From the pinned Mathlib checkout with cached dependencies:
PATH=/root/.elan/bin:$PATH lake env \
  /workspaces/repository/bench/lean-source-trace/.lake/build/bin/sourceTrace \
  Mathlib/Data/Nat/GCD/Basic.lean > /tmp/gcd-spans.json
PATH=/root/.elan/bin:$PATH lake env printenv LEAN_PATH
# Store the preceding value as {"LEAN_PATH":"..."} in /tmp/mathlib-env.json.
# From /workspaces/repository, with the pinned REPL built using Lean 4.34.1:
python3 bench/lean_repl_workload.py \
  --source /tmp/lean-kernel-arena/_build/tests/work/mathlib/src/Mathlib/Data/Nat/GCD/Basic.lean \
  --spans /tmp/gcd-spans.json --repl /tmp/lean-repl/.lake/build/bin/repl \
  --env-json /tmp/mathlib-env.json --cores 0 --repeat 3 --out /tmp/mathlib-replay
```

The cold path's explicit `end Nat` matches this selected file's namespace;
the harness does not claim arbitrary-file scope reconstruction. Scope-aware
candidate extraction and additional modules are needed for broader datasets.
The strongest current CPU serving baseline is established prefix/environment
reuse, rather than cold processes. Next workload work should collect actual
candidate streams and measure environment growth, cancellation, queueing and
proof completeness. LeanDojo's [official repository](https://github.com/lean-dojo/LeanDojo)
marks its original package deprecated and points to v2; its
[dataset documentation](https://leandojo.org/leandojo.html) is a lead, not a
stack installed or a workload result in this experiment.
