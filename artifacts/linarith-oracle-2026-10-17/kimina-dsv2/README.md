# Official DSV2 proof corpus through Kimina HTTP

This tests current CPU-oracle transfer to Farkas' published reference corpus,
not another GPU kernel or a new underlying theorem benchmark. All438official
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
The complete438three-pair comparison is acquiring.

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
