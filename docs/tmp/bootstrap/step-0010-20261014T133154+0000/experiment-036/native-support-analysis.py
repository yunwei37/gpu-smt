from pathlib import Path
import collections
import csv
import json

root = Path(__file__).resolve().parent
for tag in ["prelude", "mathlib49-prefix", "v3-prelude", "v3-mathlib49-prefix", "v3-official-init"]:
    rows = list(csv.DictReader((root / f"native-support-{tag}.csv").open()))
    assert [int(x["declaration_index"]) for x in rows] == list(range(len(rows)))
    bodies = [x for x in rows if x["kind"] != "native-only"]
    assert all(int(x["native_body_thread_cpu_ns"]) > 0 for x in bodies)
    positive = [x for x in bodies if x["host_positive"] == "1"]
    assert all(x["host_reason"] == "0" for x in positive)
    total_ns = sum(int(x["native_body_thread_cpu_ns"]) for x in bodies)
    positive_ns = sum(int(x["native_body_thread_cpu_ns"]) for x in positive)
    reasons = collections.defaultdict(lambda: {"count": 0, "body_thread_cpu_ns": 0})
    for row in bodies:
        reason = reasons[row["host_reason"]]
        reason["count"] += 1
        reason["body_thread_cpu_ns"] += int(row["native_body_thread_cpu_ns"])
    result = {
        "input": tag,
        "declarations": len(rows),
        "bodies": len(bodies),
        "host_positive": len(positive),
        "body_thread_cpu_s": total_ns / 1e9,
        "positive_body_thread_cpu_s": positive_ns / 1e9,
        "positive_fraction_of_body_thread_cpu": positive_ns / total_ns,
        "positive_fraction_of_body_count": len(positive) / len(bodies),
        "reasons": dict(collections.Counter(x["host_reason"] for x in bodies)),
        "reason_costs": dict(reasons),
        "max_steps": max(int(x["host_steps"]) for x in bodies),
        "limits": (
            "Host positives are unqualified prospective answers. "
            "Per-body thread CPU sums are not check wall removed, a strict "
            "Amdahl bound, source-verification gain, or GPU evidence."
        ),
    }
    (root / f"native-support-{tag}-analysis.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(tag, "bodies", len(bodies), "positive", len(positive),
          "body_cpu_fraction", positive_ns / total_ns)
