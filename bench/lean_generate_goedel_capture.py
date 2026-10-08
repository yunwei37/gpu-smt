#!/usr/bin/env python3
"""Capture actual Goedel-policy completions with a Blackwell-capable engine.

Prompt, extraction, n=32, temperature=1, top_p=.95 and token settings follow
Goedel-Prover d80349d93a80305765492014f0b395cec46e5023/eval/step1_inference.py.
SGLang and serial generation replace the obsolete vLLM dependency/batching;
candidate equality or reproduction of published proving accuracy is not claimed.
This generates workload inputs, not GPU Lean checking or verification results.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

MODEL = "Goedel-LM/Goedel-Prover-SFT"
MODEL_REVISION = "5b03a13d14265d438048ffd4620f28f637f85313"
DEFAULT_HEADER = "import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n"


def prompt_for(data):
    return ("Complete the following Lean 4 code with explanatory comments preceding each line of code:\n\n```lean4\n"
            + data.get("header", DEFAULT_HEADER)
            + data.get("informal_prefix", "") + data["formal_statement"])


def extract_code(text):
    match = re.search(r"```lean4\n(.*?)\n```", text, re.DOTALL)
    return match.group(1) if match else "None"


def append(path, value):
    with path.open("a") as out:
        out.write(json.dumps(value, ensure_ascii=False) + "\n")
        out.flush()
        os.fsync(out.fileno())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-path", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model-cache", type=Path, required=True)
    ap.add_argument("--split", default="test")
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--prepare-only", action="store_true", help="CPU source/prompt preparation; not inference")
    args = ap.parse_args()
    if args.n < 1:
        ap.error("--n must be positive")
    data = [json.loads(line) for line in args.input_path.read_text().splitlines() if line.strip()]
    rows = [row for row in data if args.split == "none" or str(row["split"]) == args.split]
    if not rows:
        raise RuntimeError("No selected original tasks")
    args.out.mkdir(parents=True, exist_ok=False)
    inputs = [prompt_for(row) for row in rows]
    (args.out / "selected_tasks.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    (args.out / "prompts.json").write_text(json.dumps(inputs, ensure_ascii=False, indent=2) + "\n")
    provenance = dict(command=sys.argv, model=MODEL, model_revision=MODEL_REVISION,
                      input_sha256=hashlib.sha256(args.input_path.read_bytes()).hexdigest(),
                      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      tasks=len(rows), samples_per_task=args.n, seed=1,
                      policy_adaptation="SGLang serial generation; no vLLM sample-identity claim",
                      prepared_only=args.prepare_only)
    if args.prepare_only:
        (args.out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        print("prepared", len(rows), "prompts; no model or verifier executed")
        return
    import huggingface_hub
    import sglang as sgl
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError("An assigned RTX5090 is required")
    devices = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    if len(devices) != 1 or "5090" not in devices[0]:
        raise RuntimeError("Expected exactly one assigned RTX5090, got " + repr(devices))
    provenance.update(sglang_version=sgl.__version__, torch_version=torch.__version__,
                      cuda_version=torch.version.cuda, devices=devices,
                      huggingface_hub_version=huggingface_hub.__version__)
    (args.out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    model_path = huggingface_hub.snapshot_download(
        MODEL, revision=MODEL_REVISION, cache_dir=str(args.model_cache),
        allow_patterns=["*.json", "*.safetensors"])
    engine = sgl.Engine(model_path=model_path, dtype="bfloat16", tp_size=1,
                        random_seed=1, context_length=4096, max_running_requests=1,
                        max_total_tokens=8192, mem_fraction_static=0.8,
                        cuda_graph_max_bs=1)
    records, codes = [], []
    try:
        for task_index, (row, prompt) in enumerate(zip(rows, inputs)):
            completed = dict(row, model_input=prompt, model_outputs=[], full_code=[])
            for sample in range(args.n):
                identity = dict(task_index=task_index, sample=sample,
                                name=row.get("problem_id", row.get("name")),
                                submitted_ns=time.time_ns(), prompt=prompt)
                append(args.out / "generation-events.jsonl", dict(event="submitted", **identity))
                try:
                    output = engine.generate(prompt, {"temperature": 1.0, "top_p": 0.95,
                                                       "max_new_tokens": 2048})
                except BaseException as exc:
                    append(args.out / "generation-events.jsonl",
                           dict(event="exception", response_ns=time.time_ns(),
                                error_type=type(exc).__name__, error=str(exc), **identity))
                    raise
                code = extract_code(prompt + output["text"])
                append(args.out / "generation-events.jsonl",
                       dict(event="response", response_ns=time.time_ns(), raw_output=output,
                            extracted_code=code, **identity))
                completed["model_outputs"].append(output["text"])
                completed["full_code"].append(code)
                codes.append(dict(name=identity["name"], code=code))
            records.append(completed)
            append(args.out / "completed-task-records.jsonl", completed)
            print("completed", task_index + 1, "of", len(rows), "tasks", flush=True)
        (args.out / "full_records.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
        (args.out / "to_inference_codes.json").write_text(json.dumps(codes, ensure_ascii=False, indent=2) + "\n")
    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()
