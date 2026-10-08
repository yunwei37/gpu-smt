# Native preparation transport controls

These are **dependency controls**, not actual generated candidate streams, an integrated real preflight, a service result or an RQ answer. They exercise exact pinned Lean4.9/Mathlib/REPL and the raw capture/comparison path. Their timings remain diagnostic observations only.

| Retained pair | Constructed inputs | Observed outcome per path | Strict protected-field comparison |
|---|---|---|---|
| controls-native-transport/fresh + warm-line-buffered | Two original ProofNet rows with the same name and different headers; sorry/error for each | 2 incomplete,2 rejected | 4 equal; no missing invocation/result or integrity issue |
| controls-native-fallback/fresh + warm | Original Unicode header sorry/error; two literal None extraction failures | 1 incomplete,3 rejected | 4 equal; no missing invocation/result or integrity issue |

Both pairs retain original input bytes, source/task identity, exact native request/response/stderr, events, terminal process/setup/replacement records and per-input analyses. Top-level nonnegative integer env and per-sorry proofState handles are allocation identities that this policy never continues; every other native field, including goals/messages/positions, remains protected. Equality of these controls does not establish general semantic equivalence. Warm rootless fallback is a fresh native environment inside the current bounded process, not a new process or result cache.

The original `controls-native-transport/warm` run returned no header response bytes on its persistent pipe. Root gracefully interrupted its owned supervisor; exit143 and partial/raw/unlaunched records are retained. It is an unsuccessful setup attempt, excluded from all qualified comparisons. Exact native Main.repl prints responses without explicit stdout flush. Warm now uses installed stock `stdbuf -oL` and includes launcher overhead in the recorded complete clocks. Source/options/byte frame/deadline/oracle remain unchanged. Fresh retains the original lake/REPL EOF path. Executed sources are under `executed-source/`; the exact pre-repair source has SHA616e7e03e2244fc2d7d39d856ffa9b9a2d42ed5d89fa6e1504aa94f3c72ba563. Current runners subsequently add only environment/load provenance. These controls do not consume or replace real model→native preflight attempts.

For a fresh reproduction after [exact dependency restoration](../lean-candidate-source-2026-10-07/native-setup/README.md), from repository root:

```bash
capture_root=/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture
export PATH="$capture_root/lean-4.9.0-rc1-linux/bin:$PATH"
export LEAN_NUM_THREADS=1
export XDG_CACHE_HOME="$capture_root/cache"
control_out=$(mktemp -d artifacts/lean-preparation-2026-10-07/reproduction-XXXXXX)
for cohort in native-transport native-fallback; do
  control_input=artifacts/lean-candidate-source-2026-10-07/${cohort}-controls
  taskset -c 0 python3 bench/lean_capture_fresh.py \
    --codes "$control_input/to_inference_codes.json" \
    --lake "$capture_root/lean-4.9.0-rc1-linux/bin/lake" \
    --workspace "$capture_root/mathlib4" --workers 1 --timeout 300 \
    --out "$control_out/$cohort/fresh"
  taskset -c 0 python3 bench/lean_capture_warm.py \
    --codes "$control_input/to_inference_codes.json" \
    --tasks "$control_input/selected_tasks.json" \
    --lake "$capture_root/lean-4.9.0-rc1-linux/bin/lake" \
    --workspace "$capture_root/mathlib4" --timeout 300 --retire-after 2 \
    --out "$control_out/$cohort/warm"
  python3 tools/analyze_lean_preparation.py \
    --fresh "$control_out/$cohort/fresh" --warm "$control_out/$cohort/warm" \
    --out "$control_out/$cohort/analysis"
done
```

Read `terminal_complete`, integrity issues, observed native-call coverage and each comparison/outcome separately; terminal records alone do not certify parity or validity. The single-CPU controls differ deliberately from the4CPU source build. `cpu-topology.json/txt` records the observed owning-container topology; affinity0 does not establish isolation, physical-core exclusivity or equal host load. No memory measurement, normal kernel/frontend stage split, GPU execution or acceleration claim follows.

The actual generated-candidate experiment remains under the [approved plan](../../docs/tmp/bootstrap/step-0002-20261007T224656+0000/experiment-002/plan.md), with normally assignedRTX5090 model preflight still pending at this checkpoint. Existing generation entrypoint/input identities remain unchanged.
