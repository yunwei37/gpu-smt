"""Offline analyses of three existing directions;no native execution."""
from pathlib import Path
import collections
import gzip
import importlib.util
import json
import math
import sys

sys.dont_write_bytecode = True
ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
assert (ROOT / "Cargo.toml").exists()


def read(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(gzip.decompress(raw) if str(path).endswith(".gz") else raw)


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


# Direction1:disjoint source partitions,not overlapping tactic-cost sums.
profiles = read("artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json")
target_keys = ("tactic execution|Mathlib.Tactic.intervalCases",
               "tactic execution|Lean.Parser.Tactic.simpAll")
groups = {}
for row in profiles:
    if not row["has_body_profile_data"]:
        category = "body_unobserved"
    else:
        entered = [any(row["components"].get(key, {}).get(field, 0) > 0
                       for field in ("calls", "open_frames")) for key in target_keys]
        category = ("both" if all(entered) else "interval_only" if entered[0]
                    else "simp_all_only" if entered[1] else "neither_observed")
    key = (row["baseline_status"], category)
    group = groups.setdefault(key, dict(sources=0, baseline_cumulative_HTTP_seconds=0,
                                       sources_with_open_target_frame=0, missing_baseline_body_clocks=0, source_ids=[]))
    group["sources"] += 1
    group["missing_baseline_body_clocks"] += row["baseline_reported_body_seconds"] is None
    group["baseline_cumulative_HTTP_seconds"] += row["baseline_HTTP_seconds"]
    group["sources_with_open_target_frame"] += any(
        row["components"].get(k, {}).get("open_frames", 0) for k in target_keys)
    group["source_ids"].append(row["source_id"])
failure = dict(rows=[dict(baseline_status=k[0], observed_target_group=k[1], **v)
                     for k, v in sorted(groups.items())],
               total_sources=len(profiles), native_executions=0,
               scope="selected480 baseline-fixed source partitions;HTTP spans overlap across candidates;not total wall fractions or ordinary-exception eligibility")
assert sum(g["sources"] for g in groups.values()) == 480
save("failure-partitions.json", failure)

# Direction2:paired task costs in the already frozen observed work model.
tasks = read("artifacts/candidate-scheduling-2026-10-25/source-cost-crossfit-20261026/per-task.json.gz")
task_rows = []
for task in tasks:
    fifo = task["policies"]["fifo"]["frozen_attempt_seconds"]
    task_rows.append(dict(task_id=task["task_id"], solvable=task["observed_solvable"],
                          fifo_seconds=fifo, policies={
        name: dict(seconds=p["frozen_attempt_seconds"],
                   delta_seconds=p["frozen_attempt_seconds"] - fifo,
                   fifo_over_policy_ratio=fifo / p["frozen_attempt_seconds"])
        for name, p in task["policies"].items()}))
ranked = sorted(task_rows, key=lambda row: (-row["fifo_seconds"], row["task_id"]))
tailsets = {"all": ranked, "baseline_slowest_10pct_tasks": ranked[:math.ceil(len(tasks) * .10)],
            "baseline_slowest_1pct_tasks": ranked[:math.ceil(len(tasks) * .01)]}
scheduling = dict(tasks=len(tasks), native_executions=0, model="frozen summed observed attempt work",
                  scope="task-level first-success only;not RL all-candidate rewards,actual rescheduling,latency or general Amdahl ceiling",
                  groups={})
for label, rows in tailsets.items():
    fifo = sum(row["fifo_seconds"] for row in rows)
    policies = {}
    for policy in tasks[0]["policies"]:
        changed = [row["policies"][policy]["delta_seconds"] for row in rows]
        total = sum(row["policies"][policy]["seconds"] for row in rows)
        policies[policy] = dict(seconds=total, fifo_over_policy_ratio=fifo / total,
                                improved_tasks=sum(d < -1e-6 for d in changed),
                                regressed_tasks=sum(d > 1e-6 for d in changed),
                                unchanged_tasks=sum(abs(d) <= 1e-6 for d in changed),
                                maximum_added_seconds=max(changed),
                                maximum_saved_seconds=-min(changed))
    scheduling["groups"][label] = dict(tasks=len(rows), solvable=sum(row["solvable"] for row in rows),
        fifo_seconds=fifo, policies=policies, task_ids=[row["task_id"] for row in rows])
save("scheduling-task-tails.json", scheduling)
save("scheduling-per-task.json", task_rows)

# Direction3:new overlap geometry from the retained native trace.
base = "artifacts/lean-code-verification-2026-10-25/leanmlir-native-20261027T025426Z"
profile = read(base + "/original-file-profile/native-trace.json.gz")
prior = read(base + "/analysis.json")
spec = importlib.util.spec_from_file_location("existing_labels", ROOT / "bench/lean-code-verification/analyze-verina.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
intervals = {"all": [], "verify": [], "solver": []}
labels = {"Meta.Tactic.sat: Verifying LRAT certificate": "verify",
          "Meta.Tactic.sat: Running SAT solver": "solver"}
for thread in profile["threads"]:
    samples = thread["samples"]
    assert samples["weightType"] == "tracing-ms"
    nearest = {}
    for index in range(thread["stackTable"]["length"]):
        label = helper.label(thread, index)
        parent = thread["stackTable"]["prefix"][index]
        assert parent is None or parent < index
        nearest[index] = label if label.startswith(("Meta.Tactic.sat:", "Meta.Tactic.bv:")) else nearest.get(parent)
    for index, weight in enumerate(samples["weight"]):
        assert math.isfinite(weight) and weight >= 0
        if not weight:
            continue
        stack = samples["stack"][index]
        assert index > 0 and samples["stack"][index - 1] == stack
        lo, hi = samples["time"][index - 1], samples["time"][index]
        assert hi >= lo and abs(hi - lo - weight) <= .001
        intervals["all"].append((lo, hi))
        kind = labels.get(nearest[stack])
        if kind:
            intervals[kind].append((lo, hi))


def merge(rows):
    result = []
    for lo, hi in sorted(rows):
        if not result or lo > result[-1][1]:
            result.append([lo, hi])
        else:
            result[-1][1] = max(result[-1][1], hi)
    return result


def seconds(rows):
    return sum(hi - lo for lo, hi in rows) / 1000


def intersection(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if hi > lo:
            result.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result


unions = {key: merge(rows) for key, rows in intervals.items()}
duration = {key: seconds(rows) for key, rows in unions.items()}
overlap = seconds(intersection(unions["verify"], unions["solver"]))
for phase, name in [("verify", "Meta.Tactic.sat: Verifying LRAT certificate"),
                    ("solver", "Meta.Tactic.sat: Running SAT solver")]:
    assert abs(duration[phase] - prior["profile_interval_union_seconds"]["phase:" + name]) < 1e-6
bins = {}
for phase in ("verify", "solver"):
    events = collections.defaultdict(int)
    for lo, hi in intervals[phase]:
        events[lo] += 1
        events[hi] -= 1
    histogram = collections.defaultdict(float)
    count = 0
    previous = None
    peak = 0
    for when, delta in sorted(events.items()):
        if previous is not None and count:
            histogram[count] += (when - previous) / 1000
        count += delta
        peak = max(peak, count)
        assert count >= 0
        previous = when
    assert count == 0
    bins[phase] = dict(peak_simultaneously_labelled_trace_lanes=peak,
                      seconds_at_least_two_lanes=sum(v for k, v in histogram.items() if k >= 2),
                      seconds_by_labelled_lane_count=dict(sorted(histogram.items())))
other = duration["all"] - seconds(merge(intervals["verify"] + intervals["solver"]))
geometry = dict(native_executions=0, profile_only_seconds={
    "all_trace_union": duration["all"], "verify_only": duration["verify"] - overlap,
    "solver_only": duration["solver"] - overlap, "both": overlap, "neither": other},
    lane_geometry=bins,
    scope="one instrumented module;labelled trace lanes include waits and are not CPU core demand,SAT batches or LRAT dependency independence;no transfer to uninstrumented clocks or speedup bound")
assert abs(sum(geometry["profile_only_seconds"][k] for k in ("verify_only", "solver_only", "both", "neither")) - duration["all"]) < 1e-6
save("code-verification-overlap.json", geometry)
print(json.dumps(dict(failure_rows=[{k:v for k,v in row.items() if k != "source_ids"} for row in failure["rows"]],
                      scheduling_groups=scheduling["groups"], geometry=geometry), indent=2))
