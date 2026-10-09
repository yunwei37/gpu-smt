# Native prepared Z3 context: completed supporting behavior experiment

[Step0004](../../docs/tmp/bootstrap/step-0004-20261009T183603+0000/step-report.md), [exact experiment005 plan](../../docs/tmp/bootstrap/step-0004-20261009T183603+0000/experiment-005/plan.md), [plan review](../../docs/tmp/bootstrap/step-0004-20261009T183603+0000/experiment-005/plan-review.md) and [independent raw result review](../../docs/tmp/bootstrap/step-0004-20261009T183603+0000/experiment-005/result-review.md).

Complete normal matrix:156 captured public VeruSAGE solver streams ×6conditions ×3whole repetitions =2,808 normal response cells,7,920 checks,39,528 native requested frames. There are1,422 native launcher invocations,18 prepared parents,1,404 normal forked children and six additional canceled children; response-cell counts are not native-process counts. Separate real preflight ran six normal cells and one cancellation, and is readiness evidence only.

| Condition | Input/boundary | Observed comparison |
|---|---|---|
| source | unchanged same-source CLI, original stdin bytes | behavior reference, not performance competitor |
| fresh | owned lazy context, retained normalized full input | complete non-statistical response/stderr/exit parity |
| split | same owned context across native prefix EOF/suffix | same parity |
| branch | prepared parent, sequential original-order children | same parity |
| reverse | reversed sibling order | same parity |
| cancel | SIGKILL/reap selected child, then original-order children | same subsequent-sibling parity |

Every condition/repetition retains434UNSAT/6UNKNOWN/0SAT; every original response is compared individually. Five native model artifacts per condition/repeat match exact reference bytes, but they occur after UNKNOWN and are not certified satisfying models. No SAT/proof/core coverage exists in this cohort. Statistics remain raw diagnostic output and are the only frames excluded from exact identity. Same-source version responses match; previous release/build metadata differences remain a separate retained limitation.

All six full cancellations have actual wait4 SIGKILL status after a native check response. Selected58 has25checks: retained partial decisions1/6/1 across repetitions. Selected87 hasonecheck: its sole decision is already returned in each run, so killing can occur during later artifact/cleanup work. Pipe buffering and proc sampling affect the point reached. This is post-native-progress disposal followed by sibling response parity, not interruption inside solving or concurrent branch safety.

Preparation comprises two observed groups (106streams/108commands/9,464bytes;50streams/1command/30bytes) without verification, finite timers, parallel tactics, callbacks or input-directed stream replacement. One-task refusal guards and inspected native source qualify only this restricted runtime path. Generic fork/COW and byte-prefix sharing are not novelty or evidence of useful preparation cost. These selected captured solver streams are not full historical candidate traffic or source-level complete Verus verification. No service speed, fleet-memory advantage, general semantic equivalence, RQ closure or GPU result is inferred.

## Build and reproduce

Pinned unchanged official Z3 source ddb49568d3520e99799e364fb22f35fc67d887b1 and its existing static library/official shell registration objects remain under `/workspaces/.agent-state/gpu-smt-deps/z3-4.16.0-source`. The [prior artifact](../native-frontend-2026-10-09/README.md) records source retrieval/configuration/build and unchanged stock CLI. The new [build-driver.sh](build-driver.sh) links only this wrapper, without rebuilding or changing previous executables. Initial warning logs, pre-execution parser-flag alignment and final clean build are retained. [binary-hashes.txt](binary-hashes.txt) identifies executed products; binary/object remain on the owning PVC and are ignored, not deleted.

```sh
bash artifacts/native-prepared-2026-10-09/build-driver.sh
python3 -u bench/verus_native_prepared_probe.py artifacts/native-branch-2026-10-07/full --source artifacts/native-frontend-2026-10-09/z3-source --driver artifacts/native-prepared-2026-10-09/native-z3-prepared --cores 8 --repeat 3 --out artifacts/native-prepared-2026-10-09/reproduction
python3 tools/analyze_native_prepared_probe.py artifacts/native-prepared-2026-10-09/reproduction
```

Use a new output directory; existing partial/full data are never overwritten. First recover the prior input authority by extracting native-branch/full.tar.gz in that prior artifact folder. No new input parser or serialized command reconstruction is used: existing original/full/prefix/suffix bytes are copied. Existing command splitting is response-observation metadata only. The authoritative backend remains the native parser/solver.

Executed source snapshots include wrapper, runner, analyzer and imported response observer/metadata helper. Full and preflight provenance record every executable/source hash, exact argv, topology, actual affinity and load. All1,422 observed launcher affinities are[8]; affinity does not establish isolation. Load before1.39/1.83/1.69 and after2.09/2.12/1.85 remains an explicit non-isolated-host limitation. Whole launcher elapsed durations, wait4 costs and smaps receipts are secondary diagnostics; parent CPU starts before the recorded parse wall interval and cannot be called a matching stage decomposition. Summed RSS is not fleet PSS. No timing ratio is a service headline.

[full.tar.gz](full.tar.gz) and [preflight1.tar.gz](preflight1.tar.gz) retain complete raw/derived outputs in Git; [raw-archive-hashes.txt](raw-archive-hashes.txt) records exact archive hashes. Uncompressed257MiB full data remain on the owning PVC. From this artifact folder, extract each archive, then run `python3 ../../tools/analyze_native_prepared_probe.py full`. Analysis requires neither solver binaries nor a GPU; preserve raw bytes when recomputing derived outputs. The complete returned [result review](../../docs/tmp/bootstrap/step-0004-20261009T183603+0000/experiment-005/result-review.md) recomputes every normal output and cancellation receipt independently.

The existing RTX5090 generation Job remains separate and externally pending; no device allocation/output is created by this CPU experiment. Strong warm/cache/native-snapshot competitors, real candidate streams and complete heterogeneous verification remain required by the paper.
