#!/usr/bin/env python3
"""Run Verus/VeruSAGE-Bench while transparently capturing Z3 SMT-LIB sessions.

This harness relies on Verus's documented VERUS_Z3_PATH environment variable.
It creates an executable wrapper around tools/z3_capture.py, so Verus itself is
unmodified and every Z3 stdin session is recorded per task.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "tools" / "z3_capture.py"


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)[:180]


def find_exe(value: str) -> str:
    path = shutil.which(value) if os.path.sep not in value else value
    if not path or not Path(path).exists():
        raise FileNotFoundError(value)
    return str(Path(path).resolve())


def make_wrapper(path: Path) -> None:
    python = str(Path(sys.executable).resolve())
    path.write_text(
        "#!/bin/sh\n"
        f'exec "{python}" "{CAPTURE}" "$@"\n',
        encoding="utf-8",
    )
    path.chmod(0o755)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verus", required=True, help="path to Verus executable")
    parser.add_argument(
        "--real-z3",
        required=True,
        help="path to the real Z3 executable expected by this Verus build",
    )
    parser.add_argument(
        "--tasks-jsonl",
        type=Path,
        required=True,
        help="VeruSAGE-Bench tasks.jsonl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/verus-trace"),
    )
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--project",
        action="append",
        help="optional project code filter, repeatable",
    )
    parser.add_argument(
        "--source",
        choices=["ground_truth", "task"],
        default="ground_truth",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--verus-arg", action="append", default=[])
    args = parser.parse_args()

    verus = find_exe(args.verus)
    real_z3 = find_exe(args.real_z3)
    if not CAPTURE.exists():
        raise FileNotFoundError(CAPTURE)

    args.out.mkdir(parents=True, exist_ok=True)
    inputs = args.out / "inputs"
    logs = args.out / "logs"
    traces = args.out / "traces"
    inputs.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)
    traces.mkdir(exist_ok=True)

    wrapper = args.out / "z3-capture-wrapper"
    make_wrapper(wrapper)

    project_filter = set(args.project or [])
    records = []
    for line in args.tasks_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if project_filter and obj.get("project") not in project_filter:
            continue
        records.append(obj)
        if len(records) >= args.limit:
            break

    result_path = args.out / "runs.jsonl"
    success = 0
    timeout_count = 0
    total_start = time.perf_counter()

    with result_path.open("w", encoding="utf-8") as result_file:
        for index, record in enumerate(records):
            task_id = safe_name(
                str(record.get("task_id") or f"task-{index:05d}")
            )
            code = record.get(args.source)
            if not isinstance(code, str):
                raise ValueError(
                    f"task {task_id} has no string field {args.source!r}"
                )

            input_path = inputs / f"{task_id}.rs"
            input_path.write_text(code, encoding="utf-8")
            trace_dir = traces / task_id
            trace_dir.mkdir(exist_ok=True)

            env = os.environ.copy()
            env["VERUS_Z3_PATH"] = str(wrapper.resolve())
            env["GPU_SMT_REAL_Z3"] = real_z3
            env["GPU_SMT_TRACE_DIR"] = str(trace_dir.resolve())

            cmd = [
                verus,
                "--crate-type=lib",
                *args.verus_arg,
                str(input_path.resolve()),
            ]
            start = time.perf_counter()
            timed_out = False

            try:
                proc = subprocess.run(
                    cmd,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=args.timeout,
                    check=False,
                )
                returncode = proc.returncode
                stdout = proc.stdout
                stderr = proc.stderr
            except subprocess.TimeoutExpired as exc:
                timed_out = True
                timeout_count += 1
                returncode = None
                stdout = exc.stdout or ""
                stderr = exc.stderr or ""
                if isinstance(stdout, bytes):
                    stdout = stdout.decode("utf-8", errors="replace")
                if isinstance(stderr, bytes):
                    stderr = stderr.decode("utf-8", errors="replace")

            elapsed = time.perf_counter() - start
            if returncode == 0:
                success += 1

            (logs / f"{task_id}.stdout.txt").write_text(
                stdout,
                encoding="utf-8",
                errors="replace",
            )
            (logs / f"{task_id}.stderr.txt").write_text(
                stderr,
                encoding="utf-8",
                errors="replace",
            )

            trace_files = list(trace_dir.glob("*.smt2"))
            row = {
                "task_id": task_id,
                "project": record.get("project"),
                "source": args.source,
                "elapsed_s": elapsed,
                "returncode": returncode,
                "timed_out": timed_out,
                "z3_sessions": len(trace_files),
                "trace_bytes": sum(p.stat().st_size for p in trace_files),
            }
            result_file.write(json.dumps(row, sort_keys=True) + "\n")
            result_file.flush()
            print(json.dumps(row, sort_keys=True), flush=True)

    total_elapsed = time.perf_counter() - total_start
    summary = {
        "tasks": len(records),
        "success": success,
        "failed": len(records) - success - timeout_count,
        "timed_out": timeout_count,
        "total_elapsed_s": total_elapsed,
        "verus": verus,
        "real_z3": real_z3,
        "source": args.source,
    }
    (args.out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
