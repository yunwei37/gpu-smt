#!/usr/bin/env python3
"""Complete CLI/API/split/native-fork compatibility on captured Z3 streams.

Bootstrap evidence, not a service speedup benchmark. No added scopes. Every
group has a new single-threaded native parent that never checks a candidate.
Every fresh/split stream runs in a new process. All raw output is retained.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from analyze_smt_trace import command_head, lcp_len, split_commands


def emit(path, row):
    with path.open("a") as out: out.write(json.dumps(row) + "\n")


def jobs_and_groups(root):
    jobs, groups = [], {}
    for line in (root / "runs.jsonl").read_text().splitlines():
        task = json.loads(line)
        for path in sorted((root / "traces" / task["task_id"]).glob("*.smt2")):
            commands = split_commands(path.read_text())
            options = []
            for command in commands:
                if command_head(command) != "set-option": break
                options.append(command)
            group = hashlib.sha256("\n".join(options).encode()).hexdigest()
            job = dict(index=len(jobs), trace=str(path), task_id=task["task_id"], group=group, commands=commands)
            jobs.append(job)
            groups.setdefault(group, []).append(job)
    if not jobs: raise ValueError("No streams found")
    return jobs, groups


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--z3", type=Path, required=True)
    ap.add_argument("--driver", type=Path, required=True)
    ap.add_argument("--libz3", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cores", default="8")
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--one", action="store_true", help="One real preflight stream")
    args = ap.parse_args()
    if args.repeat < 1: ap.error("Positive --repeat required")
    args.out.mkdir(parents=True, exist_ok=False)
    jobs, groups = jobs_and_groups(args.run_dir)
    inputs = args.out / "inputs"
    inputs.mkdir()
    prefixes = {}
    forbidden = {"push", "pop", "reset", "reset-assertions", "exit", "echo"}
    for group, members in groups.items():
        prefix = members[0]["commands"][:]
        for job in members[1:]: prefix = prefix[:lcp_len(prefix, job["commands"])]
        for i, c in enumerate(prefix):
            h = command_head(c)
            if h in forbidden or h.startswith("check-") or h.startswith("get-"):
                prefix = prefix[:i]; break
        prefixes[group] = prefix
        (inputs / (group + ".prefix")).write_text("\n".join(prefix) + "\n")
    if args.one:
        jobs = jobs[:1]
        groups = {jobs[0]["group"]: jobs}
    for job in jobs:
        n = str(job["index"])
        (inputs / (n + ".full")).write_text("\n".join(job["commands"]) + "\n")
        (inputs / (n + ".suffix")).write_text("\n".join(job["commands"][len(prefixes[job["group"]]):]) + "\n")
        (inputs / (n + ".original")).write_bytes(Path(job["trace"]).read_bytes())
        job["expected_checks"] = sum(command_head(c) in {"check-sat", "check-sat-assuming"} for c in job["commands"])
    emit(args.out / "provenance.jsonl", dict(command=sys.argv,
         hashes={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                 [args.z3, args.libz3, args.driver, Path(__file__), Path(__file__).with_name("native_z3_branch.cpp"),
                  Path(__file__).resolve().parents[1] / "tools/analyze_smt_trace.py"]},
         version=subprocess.check_output([str(args.z3), "--version"], text=True),
         affinity_before=sorted(os.sched_getaffinity(0)), streams=len(jobs),
         groups={g: dict(sessions=len(js), prefix_commands=len(prefixes[g])) for g, js in groups.items()}))
    refs, summary = {}, []
    for repeat in range(args.repeat):
        modes = ["executable", "fresh", "split", "branch"]
        if repeat % 2: modes.reverse()
        for mode in modes:
            folder = args.out / f"{mode}-{repeat}"
            folder.mkdir()
            execution_failures = []
            print(f"repeat={repeat} mode={mode} streams={len(jobs)}", flush=True)
            if mode == "branch":
                for group, members in groups.items():
                    out = folder / group
                    command = ["taskset", "-c", args.cores, str(args.driver), "branch",
                               str(inputs / (group + ".prefix")), str(out)]
                    command += [str(inputs / (str(j["index"]) + ".suffix")) for j in members]
                    begin = time.perf_counter()
                    proc = subprocess.run(command, capture_output=True, text=True)
                    (folder / (group + ".stdout")).write_text(proc.stdout)
                    (folder / (group + ".stderr")).write_text(proc.stderr)
                    child_statuses = re.findall(r"^child\t([0-9]+)\tstatus\t([0-9]+)", proc.stdout, re.M)
                    if proc.returncode or proc.stderr or len(child_statuses) != len(members) or any(int(s) for _, s in child_statuses):
                        execution_failures.append(group)
                    emit(args.out / "processes.jsonl", dict(repeat=repeat, mode=mode, group=group,
                         command=command, returncode=proc.returncode, seconds=time.perf_counter() - begin))
                    for i, j in enumerate(members): j["output_path"] = out / (str(i) + ".stdout")
            else:
                for job in jobs:
                    n = str(job["index"])
                    output = folder / (n + ".stdout")
                    command = ["taskset", "-c", args.cores]
                    if mode == "executable":
                        command += [str(args.z3), "-in", "-smt2"]
                    elif mode == "fresh":
                        command += [str(args.driver), "fresh", str(inputs / (n + ".full")), str(output)]
                    else:
                        command += [str(args.driver), "split", str(inputs / (job["group"] + ".prefix")),
                                    str(inputs / (n + ".suffix")), str(output)]
                    begin = time.perf_counter()
                    proc = subprocess.run(command, capture_output=True, text=True,
                                          input=(inputs / (n + ".original")).read_text() if mode == "executable" else None)
                    if proc.returncode or proc.stderr: execution_failures.append(job["index"])
                    if mode == "executable": output.write_text(proc.stdout)
                    else: (folder / (n + ".driver-stdout")).write_text(proc.stdout)
                    (folder / (n + ".stderr")).write_text(proc.stderr)
                    emit(args.out / "processes.jsonl", dict(repeat=repeat, mode=mode, index=job["index"],
                         command=command, returncode=proc.returncode, seconds=time.perf_counter() - begin))
                    job["output_path"] = output
            differences, missing, incomplete, checks = [], [], [], 0
            for job in jobs:
                path = job["output_path"]
                if not path.exists(): missing.append(job["index"]); continue
                text = path.read_text()
                decisions = re.findall(r"^(sat|unsat|unknown)\s*$", text, re.M)
                checks += len(decisions)
                complete = len(decisions) == job["expected_checks"]
                if not complete: incomplete.append(job["index"])
                if mode == "executable" and complete: refs.setdefault(job["index"], decisions)
                reference = refs.get(job["index"])
                agreement = complete and reference is not None and decisions == reference
                if reference is not None and not agreement: differences.append(job["index"])
                emit(args.out / "decisions.jsonl", dict(repeat=repeat, mode=mode, index=job["index"],
                     trace=job["trace"], output=str(path), decisions=decisions, reference=reference,
                     expected_checks=job["expected_checks"], complete=complete, agreement=agreement,
                     original_sha256=hashlib.sha256(Path(job["trace"]).read_bytes()).hexdigest(),
                     output_sha256=hashlib.sha256(text.encode()).hexdigest()))
            row = dict(repeat=repeat, mode=mode, streams=len(jobs), checks=checks,
                       differing_streams=differences, missing_streams=missing,
                       incomplete_streams=incomplete, execution_failures=execution_failures)
            summary.append(row)
            print(json.dumps(row), flush=True)
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__": main()
