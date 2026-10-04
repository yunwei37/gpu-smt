#!/usr/bin/env python3
"""Compare fresh processes with persistent official replay, without result reuse.

Fixed correctness fixtures are a throughput proxy, not an agent candidate stream.
Every job retains its input identity, decision and dispatch-to-response time.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time

from lean_export_batch import expand, run_one


def decision(result: dict) -> str:
    if result["timed_out"]:
        return "timeout"
    if result["returncode"] == 0 and result["stdout"].startswith("Accepted "):
        return "accepted"
    if result["returncode"] == 1:
        return "rejected"
    return "error"


def digest(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def persistent_chunk(binary: str, cores: str, jobs: list[tuple[int, str]], timeout: float) -> list[dict]:
    records = []
    with subprocess.Popen(["taskset", "-c", cores, binary], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, text=True, bufsize=1) as proc:
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)
        try:
            for job_id, path in jobs:
                start = time.perf_counter()
                proc.stdin.write(path + "\n")
                proc.stdin.flush()
                if not selector.select(timeout):
                    raise TimeoutError(f"persistent response timed out: {path}")
                line = proc.stdout.readline()
                if not line:
                    raise RuntimeError(f"persistent process exited: {proc.poll()}")
                record = json.loads(line)
                if record["path"] != path:
                    raise RuntimeError("response identity mismatch")
                record.update(job_id=job_id, response_s=time.perf_counter()-start)
                records.append(record)
            proc.stdin.close()
            proc.wait(timeout=timeout)
            if proc.returncode != 0:
                raise RuntimeError(f"persistent process exited: {proc.returncode}")
        finally:
            selector.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    return records


def run(mode: str, files: list[str], width: int, args: argparse.Namespace) -> dict:
    start = time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=width) as pool:
        if mode == "persistent":
            chunks = [list(enumerate(files))[i::width] for i in range(width)]
            results = list(pool.map(lambda c: persistent_chunk(args.persistent, args.cores, c, args.timeout), chunks))
            records = [r for chunk in results for r in chunk]
        else:
            def cold(job):
                i, path = job
                r = run_one(args.official, args.cores, path, args.timeout)
                return dict(job_id=i, path=path, status=decision(r), response_s=r["wall"],
                            returncode=r["returncode"], message=r["stderr"])
            records = list(pool.map(cold, enumerate(files)))
    makespan = time.perf_counter()-start
    records.sort(key=lambda r: r["job_id"])
    values = sorted(r["response_s"] for r in records)
    quantile = lambda p: values[min(len(values)-1, int(p*(len(values)-1)))]
    return dict(mode=mode, width=width, jobs=len(files), makespan_s=makespan,
                throughput_jobs_per_s=len(files)/makespan,
                amortized_ms_per_job=makespan*1000/len(files),
                response_p50_ms=quantile(.5)*1000, response_p95_ms=quantile(.95)*1000,
                response_max_ms=max(values)*1000, records=records)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--official", required=True)
    ap.add_argument("--persistent", required=True)
    ap.add_argument("--inputs", nargs="+", required=True)
    ap.add_argument("--cores", default="8-23")
    ap.add_argument("--widths", default="1,8,16")
    ap.add_argument("--duplicate", type=int, default=20)
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--timeout", type=float, default=3600)
    ap.add_argument("--json", required=True)
    args = ap.parse_args()
    files = expand(args.inputs, args.duplicate)
    widths = [int(w) for w in args.widths.split(",")]
    if not files or min(widths) < 1 or args.duplicate < 1 or args.repeat < 1:
        ap.error("need inputs and positive widths/repeats")
    manifest = {f: dict(sha256=digest(f), bytes=Path(f).stat().st_size) for f in set(files)}
    runs = []
    baseline = None
    for rep in range(args.repeat):
        for width in widths:
            # Alternate order to reduce systematic warm-cache/order bias.
            for mode in (["cold", "persistent"] if rep % 2 == 0 else ["persistent", "cold"]):
                r = run(mode, files, width, args)
                r["repeat"] = rep
                identities = [(x["path"], x["status"]) for x in r["records"]]
                if baseline is None:
                    baseline = identities
                r["mismatches_vs_first_run"] = sum(a != b for a, b in zip(baseline, identities))
                r["errors"] = sum(x["status"] not in ("accepted", "rejected") for x in r["records"])
                runs.append(r)
                print(mode, width, rep, round(r["makespan_s"], 4), "s",
                      round(r["throughput_jobs_per_s"], 1), "jobs/s",
                      r["mismatches_vs_first_run"], "mismatches", flush=True)
                payload = dict(command=sys.argv, settings=vars(args), affinity=sorted(os.sched_getaffinity(0)),
                               binaries={p: digest(p) for p in (args.official, args.persistent)},
                               inputs=manifest, runs=runs)
                Path(args.json).write_text(json.dumps(payload, indent=1)+"\n")
    return int(any(r["errors"] or r["mismatches_vs_first_run"] for r in runs))


if __name__ == "__main__":
    raise SystemExit(main())
