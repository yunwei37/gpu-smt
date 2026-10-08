# RTX5090 dependency preflight for real Lean candidate capture

Status: requested2026-10-07 23:34UTC; outer coordination submitted Job coder/gpu-smt-candidate-5090-20261007 using the unchanged reviewed commands/version. Last reported2026-10-08T00:32Z: Pod gpu-smt-candidate-5090-20261007-2nlq9 Pending/FailedScheduling/Insufficient nvidia.com/gpu. Actual manifest is artifacts/lean-generated-2026-10-07/runtime-20261007-1740/runtime.yaml. No assigned device, runtime start, command log/exit or candidate result exists at root inspection. Do not duplicate this Job/request or interrupt other owners. This is workload generation, NOT GPU Lean checking or evidence of verification acceleration. The existing outer coordinator supplies normal assigned device/runtime resources; this file does not create a service, scheduler, Workspace or checkout.

## Concrete execution

Owning repository `/workspaces/repository`, retained existing gpu-smt-dev PVC. Run the actual prepared public script using one normally assigned RTX5090. Existing known runtime image is `lmsysorg/sglang@sha256:9ca30410d6280c09c8e6804525b8ba0ef598c456044e758819046f8ef3037020`; that receipt verifies its prior metadata runtime, not this untested inference path. Do not treat SGLang/PyTorch Blackwell support or memory fit as established until actual output. Preserve exact image identity, script/input SHA256, command, logs, exit, model revision and output files in this project.

From repository cwd, run the following sequentially with each command's stdout/stderr and exit retained. Stop on failure rather than overwrite outputs or silently switch hardware/model/precision:

```bash
python3 -u bench/lean_generate_goedel_capture.py --input-path artifacts/lean-candidate-source-2026-10-07/preflight-minif2f.jsonl --split test --n 1 --model-cache /workspaces/.agent-state/gpu-smt-deps/hf-models --out artifacts/lean-generated-2026-10-07/preflight-minif2f
python3 -u bench/lean_generate_goedel_capture.py --input-path artifacts/lean-candidate-source-2026-10-07/preflight-proofnet.jsonl --split test --n 1 --model-cache /workspaces/.agent-state/gpu-smt-deps/hf-models --out artifacts/lean-generated-2026-10-07/preflight-proofnet
```

Inputs are unchanged original first test rows mathd_algebra_478 and exercise_1_13b. Script embeds official prompt/extraction and pinned public model `Goedel-LM/Goedel-Prover-SFT` revision `5b03a13d14265d438048ffd4620f28f637f85313`. It fetches only JSON and safetensors from that pinned model into the retained dependency cache. Serial BF16 Engine: context4096, output max2048, temperature1/top_p0.95, global seed1, tp1, max_running_requests1, max_total_tokens8192, mem_fraction_static0.8. No published sample/accuracy equivalence to the obsolete vLLM producer is asserted.

Prepared executed-version identities (recheck before launch; changes require a new receipt): script SHA256 `fa58d102353466ed2a993cb6754850ac9d1eec3327f0b0f98018722f4b26ee15`; miniF2F first-row input `7bd365753a756d9fff30ea856f915999e7f99ce3b124c648b9439e1854a87ea7`; ProofNet first-row input `c9d37c7f60e31d6f33e5b56daae4cdafbda2ee8af1b19343efb460f47fa82099`. These are prepared file identities, not an execution receipt.

## Resources and ownership

- Exactly1 RTX5090,32GiB nominal VRAM; no B300/GB300 fallback. Existing NVIDIA device-plugin/runtime path only, with matching driver libraries. The script checks the actually assigned CUDA device name, not host sysfs/device visibility.
- Estimated host needs:4CPU/32GiB memory, about14GB retained public model assets. Original request observed about25GiB free during CPU build; at2026-10-08 after the completed build/control runs, df reports about23GiB free. Recheck actual free space before download. GPU model/runtime fit is a preflight question, not a guarantee. Do not impose or fabricate a research time limit; this finite two-completion preflight defines the requested work.
- Use the existing PVC affinity/routing appropriate to its owning Workspace; do not stop another project, alter production placement, expose credentials, create a replacement writer or probe/mount host devices.
- Retain any failed logs and partial outputs; cleanup only the temporary requested runtime after retrieval/exit. Preserve data/model cache on this project's disk. Root continues native-path work in the owning session.

## Completion and continuation

GPU dependency engagement succeeds only if both actual completions have raw generation events, official-compatible code lists and runtime provenance. Code extraction None is a retained model outcome, not generation failure. Runtime/import/OOM failures are dependencies with actual error/exit, not proof rejections. No native verification is performed in this GPU runtime; root submits those exact code bytes to the pinned native fresh/warm/oracle path. The exact toolchain build and eight constructed native control pairs have now completed; this establishes readiness only, not a generated preflight. Only that integrated engagement constitutes real experiment preflight. The complete430task/32sample experiment is a separate reviewed execution request after preflight/cost inspection, not authorized by assuming this request ran successfully.
