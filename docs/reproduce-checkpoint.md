# Reproduce retained verification experiments

The [current evaluation](evaluation.md) owns results, open requirements and
the current research resource point. [Buildable arithmetic source](../bench/lean-native/linarith-oracle/reproduction/README.md)
has a real functional qualification; [the current whole-population service plan](../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/README.md)
defines the active comparison. Historical receipts are evidence, not commands
to restart interrupted collectors. No useful extra end-to-end GPU gain has
been demonstrated over the strongest measured CPU composition.

## Current official HTTP comparison

The [existing capture CLI](../bench/lean-native/linarith-oracle/kimina-http.py)
needs the retained Kimina app and SDK Python environment, the arithmetic
build.json/native libraries, a compatible native-loader REPL, the measured
strong native-reference executable, and a Python environment with NumPy and
highspy1.15.1for the CPU support process. The build metadata records its own
Lean/Mathlib paths; do not replace them with a different cached version.
This is the declared source-native comparison, not arbitrary Lean input
support or a single-command fresh-machine installer.

### Dependency source and patches

The recorded Kimina archive pin is fb2393d, without Git metadata in the
retained dependency. The source before the declared repair and executed
snapshots are preserved. Apply the patches below in order only to those
matching before-sources in a separate, unused dependency copy. The current
running dependency already has them; do not patch it or apply them twice.

    cd "$KIMINA"
    patch --batch --forward -p1 < "$REPOSITORY/artifacts/linarith-oracle-2026-10-17/shred-closing/stream-recovery-20261019/kimina-transport-logging.patch"
    patch --batch --forward -p1 < "$REPOSITORY/artifacts/linarith-oracle-2026-10-17/shred-closing/aggregate-budget-20261019/kimina-aggregate-budget.patch"

The first patch preserves blank-line-framed responses beyond the default
asyncio line size and removes costly automatic regex highlighting. The second
tracks actual live REPL lifetimes, source ownership, resource exits and reap.
The independent parent watchdog is in the public capture's memory_budget.py.

[Actual two-patch replay](../artifacts/linarith-oracle-2026-10-17/daily-maintenance-20261019-kimina-patch-replay.json)
starts from the published before-sources in a temporary owning-Workspace
fixture. Both commands return0and all four resulting source files match the
executed snapshots byte-for-byte, with valid Python syntax. The fixture is
removed. This proves the published patch sequence reconstructs those sources,
not that an arbitrary latest upstream installation or a new native benchmark
has been qualified.

### Replay original source records

Use original JSONL records with proof_id and code. The frozen Goedel adapter
expects the code's common Mathlib/Aesop imports, adding the declared native
or Power module while preserving theorem bodies. Example input is the
[original selected1,000](../artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl).
The released29,750source set and exact IDs are linked by the current full plan;
the different Lean4.9formal workload uses its separate recorded adapter.

From the research repository root, with the chosen paths supplied by the
caller, the existing matched native/Power interface is:

    "$KIMINA/.venv/bin/python" bench/lean-native/linarith-oracle/kimina-http.py \
      --kimina "$KIMINA" --build "$BUILD" \
      --build-source bench/lean-native/linarith-oracle/reproduction \
      --repl "$NATIVE_REPL" --reference "$NATIVE_REFERENCE" \
      --support-python "$SUPPORT_PYTHON" --input "$INPUT" --out "$NEW_OUTPUT" \
      --methods native power --repetitions 3 --affinity 8 9 10 11

The affinity shown is the current measured point; another host needs eligible
CPUs and must report its different point. The CLI's resource defaults and
[current resource authority](evaluation.md#current-resource-point) are used;
do not substitute an older per-worker48GiB or observer-off recipe.
Only one full collection runs at once. Output must be new. A real small
qualification precedes a full population run; --helpalone is not qualification.

The current three-alternating-pair driver adds byte-equal compression only
after each measured lifecycle closes. Its
[plan and executed preflight](../artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019/README.md)
are the authority for that exact matrix. Warm service, whole lifecycle,
shared released-input staging and archived export costs are separate.
SDKvalid, HTTP200and a live process are not genuine complete-proof counts.
Retain all original IDs, native messages, failures, memory samples and
retirement before interpreting a speed ratio.

The three build/check/HTTP --helpinterfaces execute successfully in the
retained environment. A fresh-machine full end-to-end reproduction remains
unvalidated. These usability and patch checks add no new benchmark result.

## Earlier arithmetic phase analysis from public files

Run from this repository's root with Python3. This recomputes the complete native
phase analysis from published compressed raw files, including the five uniquely
recoverable writer splices. It needs no Lean installation, GPU, private Workspace
state, model, network download or additional Python package. Outputs stay in an
OS temporary directory and are removed afterwards; allow roughly300MB temporary
disk and a few GiB memory.

~~~bash
python3 - <<'PY'
from pathlib import Path
import gzip, json, shutil, subprocess, tempfile

root = Path.cwd()
artifact = root / 'artifacts/linarith-oracle-2026-10-17'
raw = artifact / 'gpu-stage/full1000-baseline'
bench = root / 'bench/lean-native/linarith-oracle'
with tempfile.TemporaryDirectory(prefix='gpu-smt-public-cost-replay-') as name:
    cell = Path(name)
    for filename in ['solver-costs.jsonl.gz', 'responses.jsonl.gz']:
        shutil.copyfile(raw / filename, cell / filename)
    (cell / 'terminal.json').write_bytes(
        gzip.decompress((raw / 'terminal.json.gz').read_bytes()))
    subprocess.run([
        'python3', str(bench / 'recover-cost-log.py'),
        str(raw / 'oracle.jsonl.gz'), str(cell / 'oracle.jsonl'),
        str(cell / 'recovery.json')], check=True)
    subprocess.run([
        'python3', str(bench / 'analyze-cost.py'), str(cell),
        '--input', str(artifact / 'input-top1000.jsonl')], check=True)
    actual = json.loads((cell / 'cost-analysis.json').read_text())
    with gzip.open(raw / 'recovered-cost-analysis.json.gz', 'rt') as stream:
        expected = json.load(stream)
    assert actual == expected, 'Derived analysis differs from published result'
    print('All derived fields match:', len(actual['calls']), 'LP requests;',
          len(actual['per_source']), 'source profiles')
PY
~~~

The [actual replay receipt](../artifacts/linarith-oracle-2026-10-17/gpu-stage/full1000-baseline/public-replay-receipt.json)
records134640recovered Lean records,13414numeric requests and1000source profiles,
with all derived JSON fields matching. The retained raw log remains unchanged.
Four numeric calls still lack individual source IDs; reproducing the result
does not remove that limitation. Phase CPU, overlapping timeline occupancy and
conditional zero-work sensitivities retain their separate meanings.

This is offline data reproduction, not a fresh verification benchmark, a GPU
speedup or independent audit. To rerun verification, use the pinned native
build/runtime guide above; its private build paths and external dependencies
remain separate from this public-file analysis.

## Historical 4 October checkpoint

The sections below reproduce the older checkpoint. Its baseline and
metadata-GPU primitive timings describe their own narrower boundaries.

The measured checkpoint is `f989833`, historically recorded on `research/lean-acceleration`; this is provenance, not an instruction to switch the current `main` checkout. Its sources,
complete/partial results, proof contexts, packed GPU input, official reference
and SMT traces are retained in this repository. No new measurements are needed
to read or review those results. Hashes record provenance; these instructions
add no download, installation, startup or proof-acceptance hash gates.

The original `/tmp` checkouts, binaries and Lean environment file were lost in
the later container replacement. Historical paths in receipts describe the
measured environment, not dependencies available after recovery. The same PVC
also retains `/workspaces/.agent-state/gpu-smt-lean-dag` and
`/workspaces/.agent-state/gpu-smt-verusage-20261004/mixed100`. Repository archives
are sufficient to recover the selected GPU inputs and captured SMT streams.
Use new output directories; keep old results intact. The commands below assume
the current directory is `/workspaces/repository` unless a subshell changes it.

## GPU primitive and native CPU reference

Requires Python 3, a C++17 compiler with OpenMP, and `taskset` for CPU affinity.
On another host, select available CPUs and record that difference. The GPU
entrypoint additionally requires an assigned **RTX 5090** and matching
`libcuda.so.1` through the existing NVIDIA runtime/device-plugin path. No GPU is
required for extraction or CPU execution. Standard-dev does not itself assign
one. No GB300 run is requested.

```bash
mkdir -p /tmp/gpu-smt-reproduce/dag
tar -xzf artifacts/lean-state-2026-10-04/init-dag-inputs.tar.gz \
  -C /tmp/gpu-smt-reproduce/dag
g++ -O3 -std=c++17 -fopenmp bench/lean-dag/dag_bounds.cpp \
  -o /tmp/gpu-smt-reproduce/dag-bounds
taskset -c 1 /tmp/gpu-smt-reproduce/dag-bounds \
  /tmp/gpu-smt-reproduce/dag/init.dag \
  /tmp/gpu-smt-reproduce/dag/init.lean-reference.bin serial 1 7
# Only in a separately assigned RTX 5090 execution environment:
python3 bench/lean_dag_gpu.py \
  --ptx artifacts/lean-state-2026-10-04/dag_bounds.ptx \
  --input /tmp/gpu-smt-reproduce/dag/init.dag \
  --reference /tmp/gpu-smt-reproduce/dag/init.lean-reference.bin \
  --repeat 7 --json /tmp/gpu-smt-reproduce/dag-gpu.json
```

The archived PTX executes without the lost NVRTC installation. Rebuilding PTX
is optional: install the measured `nvidia-cuda-nvrtc-cu12==12.9.86` into a chosen
directory and pass its `libnvrtc.so.12` path with `--compile-only --nvrtc PATH
--ptx OUTPUT.ptx`. Regenerating the packed DAG from scratch requires the original
init NDJSON export, which is not included in this packed-input archive. Its
identity and pinned arena/exporter metadata are in the original artifacts.
`bench/lean_dag_pack.py INPUT.ndjson OUTPUT.dag` packs it; build
`looseBVarReference` in `bench/lean-persistent` and run it with input/output paths
to regenerate official Lean metadata. Install Lean 4.34.1 first for that build.

CPU timing excludes input loading. GPU host reading, context/JIT, upload,
resident computation and download are separate components. Compare equal
boundaries; the resident ratio is not an end-to-end proof-checking speedup.

## Real Mathlib source/state replay

Requires Git, Python 3, `taskset`, and elan-managed Lean **4.34.1**, with `lean`
and `lake` on PATH. Rebuild the two third-party dependencies at the measured
revisions; do not use an unpinned latest release. These are dependency sources,
not replacement checkouts of this research repository.

```bash
mkdir -p /tmp/gpu-smt-reproduce
git clone --no-checkout https://github.com/leanprover-community/mathlib4 \
  /tmp/gpu-smt-reproduce/mathlib
git -C /tmp/gpu-smt-reproduce/mathlib checkout --detach \
  d13f23b723b8a846827a245b89c10fc7d3f11612
(cd /tmp/gpu-smt-reproduce/mathlib && lake exe cache get)
git clone --no-checkout https://github.com/leanprover-community/repl \
  /tmp/gpu-smt-reproduce/repl
git -C /tmp/gpu-smt-reproduce/repl checkout --detach \
  193cf4bb9a22bb3fc6d25774f0fe6a70db1fd6ee
printf '%s\n' 'leanprover/lean4:v4.34.1' \
  > /tmp/gpu-smt-reproduce/repl/lean-toolchain
(cd /tmp/gpu-smt-reproduce/repl && lake build)
python3 - <<'PY'
import json, subprocess
from pathlib import Path
value = subprocess.check_output(
    ['lake', 'env', 'printenv', 'LEAN_PATH'],
    cwd='/tmp/gpu-smt-reproduce/mathlib', text=True).strip()
Path('/tmp/gpu-smt-reproduce/mathlib-env.json').write_text(
    json.dumps({'LEAN_PATH': value})+'\n')
PY
python3 bench/lean_repl_workload.py \
  --source artifacts/lean-state-2026-10-04/mathlib-gcd/source.lean \
  --spans artifacts/lean-state-2026-10-04/mathlib-gcd/command-spans.json \
  --repl /tmp/gpu-smt-reproduce/repl/.lake/build/bin/repl \
  --lean "$(command -v lean)" \
  --env-json /tmp/gpu-smt-reproduce/mathlib-env.json \
  --cores 0 --repeat 3 --out /tmp/gpu-smt-reproduce/mathlib-replay
```

Source and parser spans can be reused directly from the retained benchmark.
To regenerate spans, build `bench/lean-source-trace` with `lake build`, then run
its `.lake/build/bin/sourceTrace` via `lake env` from the pinned Mathlib checkout
on `Mathlib/Data/Nat/GCD/Basic.lean`. This performs normal source elaboration;
it is optional for replay of the saved source. The cache command is documented
in the [pinned Mathlib README](https://github.com/leanprover-community/mathlib4/blob/d13f23b723b8a846827a245b89c10fc7d3f11612/README.md).
The [pinned REPL README](https://github.com/leanprover-community/repl/blob/193cf4bb9a22bb3fc6d25774f0fe6a70db1fd6ee/README.md)
describes building/running it with the consuming project's `lake env`.

The harness is specific to this source's `Nat` scope. `sorry` is incomplete,
not a valid proof. The established REPL is the warm baseline; these instructions
do not claim a novel session protocol or a real generated-candidate stream.

## Real VeruSAGE solver replay and analysis

Analysis needs only Python 3 and archived inputs. Solver replay needs the
bundled **Z3 4.16.0** from Verus release `0.2026.09.27.3cf1832`, not an arbitrary
system Z3. Obtain the x86 Linux archive from the [pinned release](https://github.com/verus-lang/verus/releases/tag/release/0.2026.09.27.3cf1832)
and unpack it; set `VERUS_REPLAY_Z3` below to its executable. Solver-only replay
does not need Rust or a Verus build.

```bash
mkdir -p /tmp/gpu-smt-reproduce
tar -xzf artifacts/verusage-2026-10-04/mixed100-raw.tar.gz \
  -C artifacts/verusage-2026-10-04/mixed100
python3 tools/analyze_verus_jobs.py artifacts/verusage-2026-10-04/mixed100 \
  --json /tmp/gpu-smt-reproduce/verusage-analysis.json
VERUS_REPLAY_Z3=/path/to/unpacked/verus-x86-linux/z3
python3 bench/verus_session_replay.py artifacts/verusage-2026-10-04/mixed100 \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 3 \
  --out /tmp/gpu-smt-reproduce/verusage-replay
python3 bench/verus_scope_ablation.py \
  --run-dir artifacts/verusage-2026-10-04/mixed100 \
  --replay-dir artifacts/verusage-2026-10-04/session-replay \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 2 \
  --out /tmp/gpu-smt-reproduce/verusage-scope
python3 bench/verus_history_probe.py \
  --run-dir artifacts/verusage-2026-10-04/mixed100 \
  --replay-dir artifacts/verusage-2026-10-04/session-replay \
  --ablation-dir /tmp/gpu-smt-reproduce/verusage-scope \
  --z3 "$VERUS_REPLAY_Z3" --cores 8 --repeat 2 \
  --out /tmp/gpu-smt-reproduce/verusage-history
```

Extraction restores the original repository-relative paths used as query identities in
the retained ablation/replay baseline. Raw sources/logs/traces can instead be
read from the surviving agent-state PVC copy. The old capture shell wrapper
contains obsolete absolute paths; invoke `bench/run_verus_trace.py` to generate
a new wrapper if recapturing, rather than running that historical wrapper.

Full Verus recapture additionally requires the pinned Verus release and Rust
1.98.1. The old sampled JSONL is gone, but all 100 `ground_truth` source files,
task IDs, projects and task order are retained. Reconstruct the harness fields
without retrieving the 849-task dataset:

```bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path('artifacts/verusage-2026-10-04/mixed100')
with Path('/tmp/gpu-smt-reproduce/selected-tasks.jsonl').open('w') as out:
    for line in (root/'runs.jsonl').read_text().splitlines():
        row = json.loads(line)
        record = {'task_id': row['task_id'], 'project': row['project'],
                  'ground_truth': (root/'inputs'/f'{row["task_id"]}.rs').read_text()}
        out.write(json.dumps(record)+'\n')
PY
```

This recovers inputs used by the harness, not all unused original dataset
fields. Run `bench/run_verus_trace.py` with the recovered JSONL, pinned `--verus`
and `--real-z3`, `--limit 100 --verus-arg=--num-threads --verus-arg=1`, and a new
`--out` directory under affinity 8–15. Select the measured Rust toolchain through
`RUSTUP_TOOLCHAIN=1.98.1-x86_64-unknown-linux-gnu`. Full recapture remains distinct
from post-capture solver replay and does not cure the retained compatibility
failures or the prefix pool's SAT/UNSAT/UNKNOWN differences.

## Next research direction

At the 4 October checkpoint, the open questions concerned real candidate
streams against warm Lean reuse, incomplete proofs and memory growth, material
checker work after representation preparation, and the retained SMT
scope/history regressions. These are dated planning questions. Current route
decisions and unfinished captures are linked at the top of this page.
Full GPU Lean checking and a novel production SMT runtime were not
demonstrated by this historical checkpoint.


## GPU-stage correction — 2026-10-17T21:58:31.301721+00:00

CPU stage: 1.346679850013x; GPU stage in progress. Final continuation uses the better CPU/GPU oracle (>1.5x). Prior CPU-only closure and hourly deletion are superseded; historical data/receipts remain.
Existing prefix capture is preserved; no minute polling or delegation.
Complete all-branch attribution before admitting GPU implementation. Root self-review.
