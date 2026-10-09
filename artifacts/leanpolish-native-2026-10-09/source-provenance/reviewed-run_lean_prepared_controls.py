#!/usr/bin/env python3
"""Stock Lean CLI controls on the same authentic whole-source edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean", type=Path, required=True)
    ap.add_argument("--lean-path", required=True)
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--files", nargs="+")
    ap.add_argument("--case-indices", nargs="+", type=int)
    args = ap.parse_args()
    args.inputs = args.inputs.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    jobs = [json.loads(x) for x in (args.inputs / "jobs.jsonl").read_text().splitlines()]
    files = sorted({j["base"] for j in jobs})
    if args.files:
        assert set(args.files) <= set(files)
        files = [f for f in files if f in args.files]
    controls = []
    for file in files:
        controls.append({"id": "original-" + str(len(controls)), "base": file,
                         "cwd": str(args.inputs / "bases"), "kind": "original"})
        js = [j for j in jobs if j["base"] == file]
        if args.case_indices:
            chosen = [j for j in js if j["index"] in args.case_indices]
        else:
            first_failure = next((j for j in js if j["recorded_outcome"] == "rejected_kernel"), js[0])
            first_success = next((j for j in js if j["recorded_outcome"] in {"chosen", "valid_not_chosen"}), None)
            if first_success is None:
                first_success = next((j for j in js if j["source_sha256"] != first_failure["source_sha256"]), first_failure)
            chosen = [first_failure, first_success] if first_success != first_failure else [first_failure]
        for j in chosen:
            # Maintain exactly the same relative source filename/module name.
            cwd = args.inputs / "candidates" / f"{j['index']:06d}"
            controls.append({"id": f"candidate-{j['index']:06d}", "base": file,
                             "cwd": str(cwd), "kind": "candidate", "index": j["index"]})
    (args.out / "selected-controls.json").write_text(json.dumps(controls, indent=2) + "\n")
    for control in controls:
        cell = args.out / control["id"]
        cell.mkdir()
        cmd = [str(args.lean.resolve()), "--json", "-Dinternal.cmdlineSnapshots=false",
               "-DElab.async=true", "-Ddebug.skipKernelTC=false", "-DmaxHeartbeats=800000", control["base"]]
        env = dict(os.environ, LEAN_PATH=args.lean_path, LEAN_NUM_THREADS="1")
        start = time.monotonic_ns()
        with (cell / "stdout.bin").open("wb") as stdout, (cell / "stderr.bin").open("wb") as stderr:
            result = subprocess.run(cmd, cwd=control["cwd"], env=env, stdout=stdout, stderr=stderr)
        receipt = {**control, "command": cmd, "LEAN_PATH": args.lean_path, "LEAN_NUM_THREADS": "1",
                   "exitcode": result.returncode, "wall_ns": time.monotonic_ns() - start,
                   "source_sha256": hashlib.sha256((Path(control["cwd"]) / control["base"]).read_bytes()).hexdigest()}
        (cell / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
