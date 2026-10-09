#!/usr/bin/env python3
"""Run the pinned native Lean adapter; retain every response and resource sample."""
import argparse
import datetime
import hashlib
import json
import os
import signal
from pathlib import Path
import subprocess
import threading
import time


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def group_sample(group):
    processes = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        pid = int(entry.name)
        try:
            if os.getpgid(pid) != group:
                continue
            fields = {}
            for line in (entry / "smaps_rollup").read_text().splitlines():
                key, sep, value = line.partition(":")
                if sep and key in {"Pss", "Rss", "Private_Clean", "Private_Dirty", "Shared_Clean", "Shared_Dirty"}:
                    fields[key] = int(value.split()[0])
            fields.update(pid=pid, threads=len(list((entry / "task").iterdir())))
            processes.append(fields)
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return {"timestamp": utc(), "monotonic_ns": time.monotonic_ns(),
            "load": os.getloadavg(), "processes": processes,
            "fleet_pss_kib": sum(p.get("Pss", 0) for p in processes)}


def run_cell(args, out, jobs, mode, workers, rep):
    cell = out / f"rep{rep}-{mode}-p{workers}"
    cell.mkdir()
    (cell / "responses").mkdir()
    records = [{"base": j["base"], "input": str((args.inputs / j["input"]).resolve()),
                "output": str((cell / "responses" / f"{j['index']:06d}.json").resolve())} for j in jobs]
    input_path = cell / "native-input.jsonl"
    input_path.write_text("".join(json.dumps(r) + "\n" for r in records))
    mask = ",".join(str(c) for c in args.cpus[:workers])
    command = ["/usr/bin/time", "-v", "-o", str((cell / "time.txt").resolve()),
               "taskset", "-c", mask, str(args.native.resolve()), mode, str(workers),
               str(input_path.resolve()), str(args.sysroot.resolve())]
    env = dict(os.environ, LEAN_NUM_THREADS=str(workers), LEAN_PATH=args.lean_path)
    receipt = {"command": command, "cwd": str((args.inputs / "bases").resolve()),
               "LEAN_NUM_THREADS": str(workers), "LEAN_PATH": args.lean_path,
               "affinity": mask, "start_utc": utc(), "expected_jobs": len(jobs),
               "native_sha256": hashlib.file_digest(args.native.open("rb"), "sha256").hexdigest(),
               "source_jobs_sha256": hashlib.file_digest((args.inputs / "jobs.jsonl").open("rb"), "sha256").hexdigest()}
    (cell / "receipt.json").write_text(json.dumps(receipt, indent=2))
    start = time.monotonic_ns()
    with (cell / "stdout.bin").open("wb") as stdout, (cell / "stderr.bin").open("wb") as stderr:
        process = subprocess.Popen(command, cwd=args.inputs / "bases", env=env,
                                   stdout=stdout, stderr=stderr, start_new_session=True)
        stop = threading.Event()

        def sample():
            with (cell / "resource-samples.jsonl").open("w") as target:
                while not stop.is_set():
                    target.write(json.dumps(group_sample(process.pid)) + "\n")
                    target.flush()
                    stop.wait(0.1)

        observer = threading.Thread(target=sample, daemon=True)
        observer.start()
        exitcode = process.wait()
        # Reap only this benchmark's process group after an abnormal host exit;
        # otherwise surviving owned children could contaminate the next cell.
        # No other workspace or project's process is touched.
        orphan_cleanup = False
        if exitcode != 0:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                orphan_cleanup = True
            except ProcessLookupError:
                pass
        stop.set()
        observer.join()
    receipt.update(exitcode=exitcode, finish_utc=utc(), wall_ns=time.monotonic_ns() - start,
                   owned_group_cleanup=orphan_cleanup,
                   observed_responses=len(list((cell / "responses").glob("*.json"))))
    (cell / "receipt.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps({"cell": str(cell), **receipt}), flush=True)
    return exitcode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--native", type=Path, required=True)
    ap.add_argument("--sysroot", type=Path, required=True)
    ap.add_argument("--lean-path", required=True)
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, nargs="+", default=[1, 4, 8])
    ap.add_argument("--cpus", type=int, nargs="+", default=list(range(8)))
    ap.add_argument("--modes", nargs="+", choices=["logical", "fork", "fresh"], default=["logical", "fork"])
    ap.add_argument("--repetitions", type=int, default=3)
    ap.add_argument("--case-indices", type=int, nargs="+")
    args = ap.parse_args()
    for p in ["native", "sysroot", "inputs", "out"]:
        setattr(args, p, getattr(args, p).resolve())
    if any(w <= 0 or w > len(args.cpus) for w in args.workers):
        ap.error("positive workers must fit the provided affinity")
    if len(args.cpus) != len(set(args.cpus)) or not set(args.cpus) <= os.sched_getaffinity(0):
        ap.error("invalid affinity")
    jobs = [json.loads(line) for line in (args.inputs / "jobs.jsonl").read_text().splitlines()]
    if args.case_indices is not None:
        indices = set(args.case_indices)
        jobs = [j for j in jobs if j["index"] in indices]
        if len(jobs) != len(indices):
            ap.error("missing case indices")
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "selected-jobs.jsonl").write_text("".join(json.dumps(j) + "\n" for j in jobs))
    failures = []
    for rep in range(args.repetitions):
        order = args.modes if rep % 2 == 0 else list(reversed(args.modes))
        scales = args.workers if rep % 2 == 0 else list(reversed(args.workers))
        for workers in scales:
            for mode in order:
                if run_cell(args, args.out, jobs, mode, workers, rep):
                    failures.append((rep, mode, workers))
    (args.out / "terminal.json").write_text(json.dumps({"failures": failures, "finish_utc": utc()}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
