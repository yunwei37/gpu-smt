#!/usr/bin/env python3
"""Analyze raw fresh/warm captures without treating wrapper booleans as truth.

No Lean source grammar or kernel-stage inference. Exact response comparison
ignores only top-level env and proofState handles within sorries, because this
policy never continues those handles. Full original JSON remains in each row.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import statistics

DEFAULT_HEADER = "import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(response):
    if not isinstance(response, dict):
        return response
    result = dict(response)
    if type(result.get("env")) is int and result["env"] >= 0:
        del result["env"]
    if isinstance(result.get("sorries"), list):
        result["sorries"] = [
            {k: v for k, v in item.items()
             if not (k == "proofState" and type(v) is int and v >= 0)}
            if isinstance(item, dict) else item
            for item in result["sorries"]]
    # Unknown/nested fields and malformed handles stay visible. Only the
    # documented native response handles, never continued here, are ignored.
    return result


def differences(a, b, path="$", limit=100):
    if type(a) is not type(b):
        return [path + " (type)"]
    if isinstance(a, dict):
        out = [path + "." + k + " (missing)" for k in sorted(set(a) ^ set(b))]
        for key in sorted(set(a) & set(b)):
            out.extend(differences(a[key], b[key], path + "." + key, limit))
        return out[:limit]
    if isinstance(a, list):
        out = [path + " (length)"] if len(a) != len(b) else []
        for i, (left, right) in enumerate(zip(a, b)):
            out.extend(differences(left, right, f"{path}[{i}]", limit))
        return out[:limit]
    return [] if a == b else [path]


def distribution(values):
    values = sorted(v for v in values if isinstance(v, (int, float)))
    if not values:
        return dict(n=0)
    def quantile(q):
        point = (len(values) - 1) * q
        left = int(point)
        right = min(left + 1, len(values) - 1)
        return values[left] + (values[right] - values[left]) * (point - left)
    return dict(n=len(values), min_ns=values[0], p50_ns=quantile(.5),
                p95_ns=quantile(.95), p99_ns=quantile(.99), max_ns=values[-1],
                mean_ns=statistics.mean(values), sum_ns=sum(values))


def task_grouping(tasks, codes):
    if not isinstance(tasks, list) or not tasks or not codes or len(codes) % len(tasks):
        raise ValueError("expected positive fixed samples per ordered task")
    width = len(codes) // len(tasks)
    names = []
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("task row is not an object")
        name = task.get("problem_id", task.get("name"))
        if not isinstance(name, (str, int)) or not isinstance(task.get("header", DEFAULT_HEADER), str):
            raise ValueError("task name/header is invalid")
        names.append(name)
    contexts = []
    for index, code in enumerate(codes):
        task_index, sample_index = divmod(index, width)
        if code.get("name") != names[task_index]:
            raise ValueError(f"source index {index} name disagrees with ordered task/sample group")
        contexts.append(dict(task_index=task_index, sample_index=sample_index,
                             original_task=tasks[task_index],
                             header=tasks[task_index].get("header", DEFAULT_HEADER)))
    return contexts, dict(task_count=len(tasks), samples_per_task=width,
                         unique_names=len(Counter(names)),
                         duplicate_names=[dict(name=n, count=c) for n, c in Counter(names).items() if c > 1])


def interpret(native, result, parse_error, family):
    status = result.get("status") if result else "missing_result"
    official = dict(pass_=False, complete=False, interpretation_error=None)
    producer_parseable = result and ((family == "fresh" and status == "exited" and not result.get("error"))
                                    or (family == "warm" and status == "response"))
    if producer_parseable and native is not None:
        try:
            errors = [m for m in native.get("messages", []) if m["severity"] == "error"]
            warnings = [m for m in native.get("messages", []) if m["severity"] == "warning"]
            passed = not errors
            complete = passed and not native.get("sorries", []) and not any(
                "declaration uses 'sorry'" in warning["data"] or "failed" in warning["data"]
                for warning in warnings)
            official.update(pass_=passed, complete=complete)
        except Exception as error:
            official["interpretation_error"] = repr(error)
    official["pass"] = official.pop("pass_")
    if not result:
        outcome = "missing_result"
    elif status in ("timeout", "interrupted", "launch_error", "transport_error"):
        outcome = status
    elif result.get("error"):
        outcome = "system_error"
    elif parse_error:
        outcome = "malformed_stdout"
    elif not isinstance(native, dict):
        outcome = "malformed_native_response"
    elif "message" in native or "error" in native:
        outcome = "native_system_error"
    elif family == "fresh" and result.get("returncode") != 0:
        outcome = "process_error"
    elif type(native.get("env")) is not int or native["env"] < 0:
        outcome = "non_command_response"
    elif not isinstance(native.get("messages", []), list) or not isinstance(native.get("sorries", []), list):
        outcome = "malformed_native_response"
    elif any(not isinstance(m, dict) or m.get("severity") not in ("error", "warning", "info") or
             not isinstance(m.get("data"), str) for m in native.get("messages", [])) or \
            any(not isinstance(s, dict) or not isinstance(s.get("goal"), str)
                for s in native.get("sorries", [])):
        outcome = "malformed_native_response"
    elif official["interpretation_error"]:
        outcome = "malformed_native_response"
    elif not producer_parseable:
        outcome = "unexpected_process_status"
    elif not official["pass"]:
        outcome = "rejected"
    elif not official["complete"]:
        outcome = "incomplete"
    else:
        outcome = "complete"
    return dict(outcome=outcome, official=official)


def load_run(folder, family):
    issues = []
    source_bytes = (folder / "codes.original.json").read_bytes()
    codes = json.loads(source_bytes)
    events = []
    event_bytes = (folder / "events.jsonl").read_bytes()
    for line_number, line in enumerate(event_bytes.splitlines(), 1):
        try:
            parsed = json.loads(line)
            if not isinstance(parsed, dict):
                raise ValueError("event is not a JSON object")
            events.append(parsed)
        except Exception as error:
            issues.append(dict(file="events.jsonl", line=line_number, error=repr(error)))
    if [e.get("sequence") for e in events] != list(range(len(events))):
        issues.append(dict(error="event sequence incomplete or reordered"))
    runs = [e for e in events if e.get("event") == "run"]
    shutdowns = [e for e in events if e.get("event") == "shutdown"]
    if len(runs) != 1 or len(shutdowns) != 1:
        issues.append(dict(error="expected exactly one run and shutdown", runs=len(runs), shutdowns=len(shutdowns)))
    run = runs[0] if runs else {}
    if run.get("codes_sha256") != digest(source_bytes) or run.get("count") != len(codes):
        issues.append(dict(error="run count/input hash does not match original source"))
    contexts, grouping = [], None
    if family == "warm":
        try:
            tasks_bytes = (folder / "tasks.original.json").read_bytes()
            if digest(tasks_bytes) != run.get("tasks_sha256"):
                issues.append(dict(error="task original bytes hash does not match run"))
            contexts, grouping = task_grouping(json.loads(tasks_bytes), codes)
            if run.get("samples_per_task") != grouping["samples_per_task"] or run.get("task_count") != grouping["task_count"]:
                issues.append(dict(error="run task/sample grouping differs from original ordered inputs"))
        except Exception as error:
            issues.append(dict(error="original task header evidence unavailable", detail=repr(error)))
    admitted = [e.get("source_index") for e in events if e.get("event") == "admitted"]
    if admitted != list(range(len(codes))):
        issues.append(dict(error="admission order/count differs from original list"))
    if contexts:
        for event in events:
            if event.get("event") in ("admitted", "header_match"):
                index = event.get("source_index")
                if type(index) is not int or index not in range(len(contexts)):
                    issues.append(dict(error="task grouping event source index out of range"))
                    continue
                if any(event.get(k) != contexts[index][k] for k in ("task_index", "sample_index")):
                    issues.append(dict(source_index=index, error="task grouping event disagrees with original order"))
                if event["event"] == "header_match":
                    header = contexts[index]["header"]
                    if event.get("header_sha256") != digest(header.encode()) or event.get("header_ascii") != header.isascii() or event.get("exact_prefix") != codes[index]["code"].startswith(header):
                        issues.append(dict(source_index=index, error="header observation disagrees with exact original task row"))
    all_results, by_index = [], defaultdict(list)
    for path in sorted(folder.rglob("result.json")):
        try:
            result = json.loads(path.read_bytes())
            for name, info in result.get("files", {}).items():
                raw_path = path.parent / name
                if not raw_path.is_file() or digest(raw_path.read_bytes()) != info.get("sha256") or raw_path.stat().st_size != info.get("bytes"):
                    issues.append(dict(file=str(raw_path.relative_to(folder)), error="raw hash/size mismatch"))
            native_path = path.parent / ("stdout.bin" if family == "fresh" else "response.bin")
            native, parse_error = None, None
            try:
                native_bytes = native_path.read_bytes()
                native = json.loads(native_bytes.decode("utf-8"))
            except Exception as error:
                native_bytes = native_path.read_bytes() if native_path.exists() else b""
                parse_error = repr(error)
            record = dict(result=result, native=native, raw_stdout_sha256=digest(native_bytes),
                          parse_error=parse_error, artifact=str(path.relative_to(folder)),
                          **interpret(native, result, parse_error, family))
            try:
                stdin_raw = (path.parent / "stdin.bin").read_bytes()
                record["stdin"] = json.loads(stdin_raw.decode("utf-8"))
                if not stdin_raw.endswith(b"\r\n\r\n"):
                    issues.append(dict(file=str(path.relative_to(folder)), error="stdin missing original CRLF blank delimiter"))
            except Exception as error:
                issues.append(dict(file=str(path.relative_to(folder)), error="stdin parse error", detail=repr(error)))
            all_results.append(record)
            index = result.get("source_index")
            if index is not None:
                by_index[index].append(record)
        except Exception as error:
            issues.append(dict(file=str(path.relative_to(folder)), error=repr(error)))
    for index, records in by_index.items():
        if type(index) is not int or index not in range(len(codes)) or len(records) != 1:
            issues.append(dict(source_index=index, error="duplicate/out-of-range candidate result", count=len(records)))
    result_events = [e for e in events if e.get("event") == "result"]
    if Counter(e.get("source_index") for e in result_events) != Counter(r["result"].get("source_index") for r in all_results):
        issues.append(dict(error="result events and result files do not reconcile"))
    event_result_counter = Counter(json.dumps({k: v for k, v in e.items()
                                   if k not in ("event", "sequence", "wall_ns", "monotonic_ns")}, sort_keys=True)
                                   for e in result_events)
    file_result_counter = Counter(json.dumps(r["result"], sort_keys=True) for r in all_results)
    if event_result_counter != file_result_counter:
        issues.append(dict(error="result event contents differ from result files"))
    replacements = [e for e in events if e.get("event") == "replacement"]
    for event in replacements:
        for name, info in event.get("files", {}).items():
            path = folder / event["session"] / name
            if not path.exists() or digest(path.read_bytes()) != info.get("sha256") or path.stat().st_size != info.get("bytes"):
                issues.append(dict(file=str(path.relative_to(folder)), error="session raw hash/size mismatch"))
        if event.get("unconsumed_stdout_bytes") and event.get("reason") not in ("timeout", "interrupted", "transport_error"):
            issues.append(dict(session=event.get("session"), error="unconsumed session stdout retained", bytes=event["unconsumed_stdout_bytes"]))
    indexed = [by_index.get(i, [])[0] if len(by_index.get(i, [])) == 1 else dict(result=None, native=None,
               **interpret(None, None, None, family)) for i in range(len(codes))]
    setup_headers = {(r["result"].get("session"), r["native"].get("env")): r.get("stdin", {}).get("cmd")
                     for r in all_results if r["result"].get("role") == "header_setup" and
                     isinstance(r["native"], dict) and type(r["native"].get("env")) is int}
    for index, row in enumerate(indexed):
        if row["result"] is None:
            continue
        expected_code = codes[index]["code"]
        env = None
        if row["result"].get("role") == "candidate_branch":
            env = row["result"].get("env_requested")
            header = setup_headers.get((row["result"].get("session"), env))
            if not isinstance(header, str) or not expected_code.startswith(header) or not header.isascii():
                issues.append(dict(source_index=index, error="branch has no exact ASCII source header setup"))
                continue
            if not contexts or header != contexts[index]["header"]:
                issues.append(dict(source_index=index, error="branch header differs from exact original task header"))
            expected_code = "".join(c if c in "\r\n" else " " for c in header) + expected_code[len(header):]
        expected = dict(cmd=expected_code, allTactics=False, ast=False, tactics=False, premises=False)
        if env is not None:
            expected["env"] = env
        expected_bytes = json.dumps(expected, ensure_ascii=False).encode() + b"\r\n\r\n"
        try:
            actual_bytes = (folder / row["artifact"]).parent.joinpath("stdin.bin").read_bytes()
        except OSError as error:
            issues.append(dict(source_index=index, error="missing submitted stdin", detail=repr(error)))
            continue
        if actual_bytes != expected_bytes:
            issues.append(dict(source_index=index, error="submitted stdin does not match original source/policy transform"))
    missing = [i for i, row in enumerate(indexed) if row["result"] is None]
    if shutdowns and (shutdowns[-1].get("result_indices") != sorted(by_index) or
                      shutdowns[-1].get("missing_result_indices") != missing):
        # Fresh writes sorted result indices; warm writes source order, both are increasing here.
        issues.append(dict(error="shutdown result completeness differs from retained files"))
    makespan = shutdowns[-1]["monotonic_ns"] - run["monotonic_ns"] if shutdowns and runs else None
    metrics = {}
    for label, records in [("all_candidates", indexed), ("all_native_calls_including_setup", all_results)]:
        metrics[label] = {}
        strata = defaultdict(list)
        for row in records:
            strata[row["outcome"]].append(row)
        for group, group_rows in [("all", records), *sorted(strata.items())]:
            metrics[label][group] = {key: distribution((r["result"] or {}).get(key) for r in group_rows)
                                    for key in ("invocation_elapsed_ns", "elapsed_ns", "capture_elapsed_ns")}
    whole_jobs = [e for e in events if e.get("event") == "whole_job_end"]
    metrics["whole_jobs"] = distribution(e.get("elapsed_ns") for e in whole_jobs)
    metrics["setup_calls"] = distribution(r["result"].get("invocation_elapsed_ns")
                                           for r in all_results if r["result"].get("role") == "header_setup")
    metrics["session_lifetimes"] = distribution(e.get("lifetime_ns") for e in replacements)
    metrics["observed_event_gaps"] = distribution(b["monotonic_ns"] - a["monotonic_ns"] for a, b in zip(events, events[1:]))
    observed_invocation_indices = sorted({e.get("source_index") for e in events
        if e.get("source_index") is not None and e.get("event") == ("launched" if family == "fresh" else "sent")})
    overview = dict(path=str(folder.resolve()), codes_sha256=digest(source_bytes),
                    task_sample_grouping=grouping,
                    events_sha256=digest(event_bytes), source_count=len(codes),
                    event_counts=dict(Counter(e.get("event") for e in events)),
                    outcomes=dict(Counter(r["outcome"] for r in indexed)),
                    missing_result_indices=missing, terminal_complete=bool(shutdowns) and not missing,
                    observed_invocation_indices=observed_invocation_indices,
                    missing_observed_invocation_indices=sorted(set(range(len(codes))) - set(observed_invocation_indices)),
                    whole_job_budget_exceeded_indices=[e["source_index"] for e in whole_jobs if e.get("nominal_budget_exceeded")],
                    integrity_issues=issues, makespan_ns=makespan,
                    timing_distributions=metrics, run_provenance=run,
                    setup_outcomes=dict(Counter(r["outcome"] for r in all_results if r["result"].get("role") == "header_setup")),
                    retained_session_tails=[dict(session=e.get("session"), reason=e.get("reason"),
                                                bytes=e.get("unconsumed_stdout_bytes"))
                                            for e in replacements if e.get("unconsumed_stdout_bytes")],
                    observed_intervals=dict(first_monotonic_ns=events[0].get("monotonic_ns") if events else None,
                                            last_monotonic_ns=events[-1].get("monotonic_ns") if events else None),
                    timing_scope="run→shutdown makespan includes setup, capture, lifecycle and teardown; invocation scopes differ in transport/launch; no kernel-stage inference")
    return codes, indexed, overview, events, contexts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fresh", type=Path, required=True)
    parser.add_argument("--warm", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    fresh_codes, fresh, fresh_summary, fresh_events, _ = load_run(args.fresh, "fresh")
    warm_codes, warm, warm_summary, warm_events, contexts = load_run(args.warm, "warm")
    input_match = fresh_codes == warm_codes
    counts = Counter()
    duplicate_counts = Counter(row["code"] for row in fresh_codes)
    args.out.mkdir(parents=True, exist_ok=False)
    with open(args.out / "per_input.jsonl", "x", encoding="utf-8") as stream:
        for index in range(max(len(fresh), len(warm))):
            left = fresh[index] if index < len(fresh) else None
            right = warm[index] if index < len(warm) else None
            code_match = index < len(fresh_codes) and index < len(warm_codes) and fresh_codes[index] == warm_codes[index]
            comparable = bool(code_match and left and right and isinstance(left["native"], dict) and
                              isinstance(right["native"], dict) and left["outcome"] in ("complete", "incomplete", "rejected") and
                              right["outcome"] in ("complete", "incomplete", "rejected"))
            delta = differences(canonical(left["native"]), canonical(right["native"])) if comparable else None
            classification = "equal" if comparable and not delta else "native_difference" if comparable else "not_comparable"
            counts[classification] += 1
            row = dict(source_index=index, input_record_equal=code_match,
                       original_task_context=contexts[index] if index < len(contexts) else None,
                       fresh_input=fresh_codes[index] if index < len(fresh_codes) else None,
                       warm_input=warm_codes[index] if index < len(warm_codes) else None,
                       fresh=left, warm=right, comparison=classification,
                       difference_paths=delta)
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    header_events = [e for e in warm_events if e.get("event") == "header_match"]
    summary = dict(fresh=fresh_summary, warm=warm_summary, input_records_equal=input_match,
                   original_input_bytes_equal=fresh_summary["codes_sha256"] == warm_summary["codes_sha256"],
                   comparison=dict(counts), exact_code_duplicates=dict(distinct_codes=len(duplicate_counts),
                   repeated_code_groups=sum(v > 1 for v in duplicate_counts.values()),
                   excess_records=sum(v - 1 for v in duplicate_counts.values())),
                   observed_headers=dict(distinct_matching_headers=len({e.get("header_sha256") for e in header_events if e.get("exact_prefix")}),
                   exact_prefix_records=sum(bool(e.get("exact_prefix")) for e in header_events),
                   ascii_eligible_records=sum(bool(e.get("exact_prefix") and e.get("header_ascii")) for e in header_events)),
                   comparison_policy="all fields strict except nonnegative integer top-level env and per-sorry proofState handles; nested/unknown/malformed fields retained; no continued handles",
                   official_interpretation="original Goedel pass/complete rules, including message-only/nonzero-exit quirks, retained separately from strict system labels")
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    table = ["# Raw Lean preparation capture analysis", "",
             "These are whole-call/corpus observations; no kernel-stage timing or equivalence claim.", "",
             "| Run | Inputs | Terminal complete | Makespan (s) | Integrity issues |", "|---|---:|---|---:|---:|"]
    for name, overview in (("fresh", fresh_summary), ("warm", warm_summary)):
        seconds = overview["makespan_ns"] / 1e9 if overview["makespan_ns"] is not None else None
        table.append(f"| {name} | {overview['source_count']} | {overview['terminal_complete']} | {seconds} | {len(overview['integrity_issues'])} |")
    table += ["", "| Response comparison | Count |", "|---|---:|"]
    table += [f"| {key} | {value} |" for key, value in sorted(counts.items())]
    table += ["", "| Run | Outcome | Records | Invocation p50 (ms) | Invocation p95 (ms) |", "|---|---|---:|---:|---:|"]
    for name, overview in (("fresh", fresh_summary), ("warm", warm_summary)):
        for outcome, count in sorted(overview["outcomes"].items()):
            times = overview["timing_distributions"]["all_candidates"][outcome]["invocation_elapsed_ns"]
            median = times.get("p50_ns", 0) / 1e6 if times["n"] else None
            p95 = times.get("p95_ns", 0) / 1e6 if times["n"] else None
            table.append(f"| {name} | {outcome} | {count} | {median} | {p95} |")
    table += ["", "Per-input source/native JSON and differences: `per_input.jsonl`. Full timing strata, system outcomes, provenance and reconciliation issues: `summary.json`.",
              "", "Primary scope is run→shutdown makespan, including setup and capture overhead. Invocation distributions include all retained outcomes; missing durations remain missing. Warm fallbacks create fresh native environments within a warm process."]
    (args.out / "tables.md").write_text("\n".join(table) + "\n")


if __name__ == "__main__":
    main()
