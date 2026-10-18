# Official DSV2 proof corpus through Kimina HTTP

This tests current CPU-oracle transfer to Farkas' published reference corpus,
not another GPU kernel or a new underlying theorem benchmark. All 438 official
DeepSeek-Prover-V2 miniF2F proof files are acquired through the pinned
[Farkas recipe](https://raw.githubusercontent.com/lucifer1004/farkas/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/docs/corpus.md).
Original payloads and raw HTTP request logs remain in the owning Workspace:
`/workspaces/.agent-state/gpu-smt-dsv2-20261018/`.
Every source imports only Mathlib and Aesop. All bodies and failures are kept.

The first16functional preflight returns10valid/6Leanerror in each method,
with identical full SDK responses, actual numerical execution and complete
retirement. This is not a population performance result.
[Plan](plan.md), [self-review](plan-review.md),
[preflight result](preflight-result-review.md),
[actual full launch](full-launch.json) and
[executed source](kimina-http-executed.py) retain the protocol.
All three 438-source alternating pairs are complete. Aggregate whole time is
1264.966s native versus1194.906s Power: **1.058632x**, or **5.54% less elapsed**.
The warmed ratio is 1.061289x. Each cell returns 263 valid/175 Lean errors,
zero operational results, matching statuses/non-message fields and one
warning-only source difference. This is a modest different-prover transfer,
not a general 1.7x or a GPU result.
[Complete result and self-review](result-review.md),
[returned records](closed-cells/) and [all-source latency figure](completed-http-cdf.pdf)
retain all six observations. The [first-pair report](first-pair-result-review.md)
remains a historical checkpoint.

Both methods use the same existing4.27environment and compiled native
dependencies. The reference is adapted Farkas probe/restrict plus the
upstream helper's default tiered exact search and common omega. Power is the
current external AST/certificate frontend and CPU numerical portfolio.
An actual observation finds8REPLs/8native helpers with the hybrid flag absent,
CPU16--19 and48GiB. This is not an unmodified4.31Farkas replication and no
published upstream timing is used as a denominator. The underlying miniF2F
tasks overlap our other formal corpus; this is producer-output transfer.

## Reproduce

Acquire the official original files outside the checkout using the pinned
`scripts/farkas-corpus.py acquire --from-dsv2 --dest /path/to/original`.
Retain that revision's `scripts/replay_live.py`; its unchanged `strip_imports`
function is used by the ordinary input adapter:

```sh
python3 bench/lean-native/linarith-oracle/prepare-dsv2.py \
  --source-root /path/to/original --official-replayer /path/to/replay_live.py \
  --out /path/to/input.jsonl --source-paths /path/to/source-paths.json
```

Use the [public source build](../../../bench/lean-native/linarith-oracle/reproduction/README.md)
and the existing version-aligned Kimina/REPL/reference helper.
The exact retained machine paths are in full-launch.json; an equivalent run is:

```sh
python bench/lean-native/linarith-oracle/kimina-http.py \
  --kimina /path/to/kimina --build /path/to/oracle-build \
  --build-source bench/lean-native/linarith-oracle/reproduction \
  --repl /path/to/version-aligned-repl --reference /path/to/native-reference-helper \
  --support-python /path/to/highspy-environment/bin/python \
  --input /path/to/input.jsonl --out /path/to/new-raw-output \
  --methods native power --native-engine tiered --affinity 16 17 18 19 \
  --repetitions 3
python3 artifacts/linarith-oracle-2026-10-17/kimina-http/analyze.py \
  /path/to/new-raw-output --affinity 16 17 18 19
python3 bench/lean-native/linarith-oracle/analyze-http-boundaries.py /path/to/new-raw-output
```

The Python running the comparison needs the actual Kimina SDK/server and
psutil; the separate support Python needs highspy/NumPy. Driver defaults
retain the original Goedel experiment's hybrid reference and CPU20--23.
Changing these two explicit benchmark selections changes only new launches.
The older active process already loaded its frozen source; its scientific
protocol and native libraries were not changed.

For complete publication, preserve all six planned cells, every original
source ID/status, warm/lifecycle clocks, failures and actual retirement.
The current analyzer's closed-observed-cells status is not by itself proof
that the entire declared matrix finished. All reviews here are root self-review.

## Reproduce the published result without private source payloads

```sh
python3 artifacts/linarith-oracle-2026-10-17/kimina-dsv2/analyze-full.py \
  artifacts/linarith-oracle-2026-10-17/kimina-dsv2/closed-cells \
  --out /path/to/summary.json
python3 artifacts/linarith-oracle-2026-10-17/kimina-dsv2/plot-cdf.py
```

The first command uses only published SDK returns and receipts. The plot
requires Matplotlib and reads the full published HTTP timing projection.
All438sources per cell, including Lean errors, appear in the plot/CSV.
Completed HTTP attempt latency excludes waiting before SDK dispatch; it is
not a CPU/LP profile or a removable whole-wall fraction.

## Where the recorded numerical work occurs

All 579 recorded large-race rows map uniquely to original source IDs:
193 races on 37 sources in every repetition. The two largest native-body
sources remain multi-minute under Power, while their recorded large-race
wall sums are below 0.33 s and 0.04 s, respectively. These spans have distinct
boundaries; unrecorded small/native LP and Lean work are not zero.
[Exact join, data and interpretation](result-review.md#exact-source-attribution-of-the-recorded-numerical-races)
retain all 438 sources. This is diagnostic evidence against another narrow
large-LP detour, not an all-LP/GPU upper bound.
