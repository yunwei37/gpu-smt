#!/usr/bin/env python3
"""Finite authored native differential,not a population/performance runner.

One candidate per naturally retiring process. A 15s wall classification stops
further dispatch after a late exit;no signal or watchdog is used. Fixtures have
a finite native heartbeat budget. Hits use an in-candidate producer and do not
measure cache opportunity. The classifier is limited to these authored proofs.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

PREFIX = "[gpu-smt-failure-diff] "
MODES = ("native", "original", "default_off", "record", "replay")
CASES = (
    ("assumption_fallback", "True", "first | failure_probe assumption | exact True.intro", "accepted", True),
    ("assumption_rejected", "False", "failure_probe assumption", "rejected", True),
    ("simp_rejected", "False", "failure_probe simp_all only", "rejected", True),
    ("mutation_fallback", "True", "first | failure_probe differentialMutation | exact True.intro", "accepted", True),
    ("mutation_rejected", "True", "failure_probe differentialMutation", "rejected", True),
    ("simp_logged_error", "True", "failure_probe simp_all only [differentialUnknownLemma]", "rejected", False),
    ("simp_open_return", "False", "failure_probe simp_all (config := { failIfUnchanged := false }) only; done", "rejected", False),
    ("normal_success", "True", "failure_probe exact True.intro", "accepted", False),
    ("incomplete_fallback", "True", "first | failure_probe assumption | sorry", "incomplete", True),
    ("heartbeat_limit", "True", "failure_probe differentialHeartbeat", "heartbeat_limit", False),
)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def run(lean, source, output, env, logs):
    command = [str(lean), "--json", "-T", "5000", "-o", str(output), str(source)]
    start = time.monotonic()
    with logs.with_suffix(".stdout").open("wb") as stdout, logs.with_suffix(".stderr").open("wb") as stderr:
        proc = subprocess.Popen(command, env=env, stdout=stdout, stderr=stderr)
        ticks = None
        try:
            stat = Path(f"/proc/{proc.pid}/stat").read_text()
            ticks = int(stat[stat.rindex(")") + 2:].split()[19])
        except (OSError, ValueError, IndexError):
            pass
        proc.wait()  # No killing timeout helper;retirement precedes dispatch.
    row = dict(command=command, pid=proc.pid, start_ticks=ticks, exit=proc.returncode,
               elapsed_seconds=time.monotonic() - start, retired=True,
               stdout=logs.with_suffix(".stdout").read_text(),
               stderr=logs.with_suffix(".stderr").read_text())
    row["late"] = row["elapsed_seconds"] > 15
    write_json(logs.with_suffix(".json"), row)
    if row["late"]:
        raise RuntimeError("late finite unit retired naturally;stop further dispatch")
    return row


def analyze(row):
    diagnostics = [json.loads(line) for line in row["stdout"].splitlines() if line.strip()]
    events, other = [], []
    for line in row["stderr"].splitlines():
        if line.startswith(PREFIX):
            events.append(json.loads(line[len(PREFIX):]))
        elif line.strip():
            other.append(line)
    if other:
        raise RuntimeError("unexpected native stderr;operational result,not rejection")
    audits = [event for event in events if event.get("event") == "proof_audit"]
    if len(audits) > 1:
        raise RuntimeError("duplicate native theorem audit")
    data = "\n".join(message.get("data", "") for message in diagnostics)
    if "(deterministic) timeout" in data:
        status = "heartbeat_limit"
    elif row["exit"] == 1 and any(message.get("severity") == "error" for message in diagnostics):
        status = "rejected"
    elif row["exit"] == 0 and len(audits) == 1 and audits[0].get("found"):
        # These authored proofs have no helper theorem hiding sorry.
        status = "incomplete" if audits[0].get("direct_sorry") else "accepted"
    else:
        raise RuntimeError("unclassified native exit;do not fabricate a verdict")
    return dict(status=status, exit=row["exit"], diagnostics=diagnostics,
                proof_audit=audits[0] if audits else None,
                hits=sum(event.get("event") == "hit" for event in events), events=events)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case", choices=[case[0] for case in CASES])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    out = args.out.resolve()
    if not out.is_relative_to(Path("/workspaces")) and not os.environ.get("GITHUB_ACTIONS"):
        parser.error("local unit output must be on the existing Workspace PVC")
    out.mkdir(parents=True, exist_ok=False)
    common = out / "modules"
    common.mkdir()
    env = os.environ.copy()
    env["LEAN_PATH"] = str(common)
    for name, source in (
        ("FailureTransition", root / "native/lean/failure-replay/FailureTransition.lean"),
        ("DifferentialSupport", root / "native/lean/failure-replay/tests/DifferentialSupport.lean"),
    ):
        result = run(args.lean, source, common / (name + ".olean"), env, out / ("build-" + name))
        if result["exit"] != 0:
            raise RuntimeError("unit support compile failed;raw result retained")
    cases = [case for case in CASES if args.case is None or case[0] == args.case]
    rows = []
    write_json(out / "scope.json", dict(scope="finite authored native differential",
        native_heartbeat_limit=5000, wall_classification_seconds=15,
        signals=False, watchdog=False, one_candidate_per_process=True,
        forced_same_input_producer=True, cross_candidate_cache=False, performance_claim=False))
    for name, target, body, expected, expect_hit in cases:
        source = out / (name + ".lean")
        compared = []
        for mode in MODES:
            # Authored single-line fixtures only. Equal-width blanks remove our
            # marker for the native reference,retaining inner tactic coordinates.
            selected = body.replace("failure_probe", " " * len("failure_probe")) if mode == "native" else body
            code = "import DifferentialSupport\nset_option maxHeartbeats 5000\n"
            code += "theorem candidateProof : " + target + " := by " + selected + "\n#audit_candidate\n"
            source.write_text(code)
            (out / (name + "-" + mode + ".source.lean")).write_text(code)
            env["GPU_SMT_FAILURE_DIFF_MODE"] = mode
            native = run(args.lean, source, out / (name + "-" + mode + ".olean"), env, out / (name + "-" + mode))
            row = dict(case=name, mode=mode, expected_status=expected, **analyze(native))
            rows.append(row)
            compared.append(row)
            write_json(out / "results.partial.json", rows)
        reference = compared[0]
        for row in compared:
            if row["status"] != expected:
                raise AssertionError(f"{name}/{row['mode']}:expected {expected},got {row['status']}")
            for field in ("status", "exit", "diagnostics", "proof_audit"):
                if row[field] != reference[field]:
                    raise AssertionError(f"{name}/{row['mode']}:native {field} differs;raw retained")
            if row["hits"] != int(expect_hit and row["mode"] == "replay"):
                raise AssertionError(f"{name}/{row['mode']}:unexpected actual hit count")
        print(name, reference["status"], "all five modes identical", flush=True)
    write_json(out / "result.json", dict(complete=True, cases=len(cases), cells=len(rows),
        compared_fields=["status", "exit", "complete_json_diagnostics", "native_theorem_audit"],
        accepted_cases=[row["case"] for row in rows if row["mode"] == "native" and row["status"] == "accepted"],
        forced_replay_hits=sum(row["hits"] for row in rows), rows=rows))


if __name__ == "__main__":
    main()
