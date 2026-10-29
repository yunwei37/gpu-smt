#!/usr/bin/env python3
"""Offline analysis of unchanged completed inputs; never a rejection detector."""
import collections
import gzip
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POINT = ROOT / "artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"

def analyze():
    with gzip.open(POINT / "warm/results.json.gz", "rt") as stream:
        raw = json.load(stream)
    by_id = {row["id"]: row for row in raw["results"]}
    tasks = []
    for task, interpretation in [
        ("amc12a_2020_p10", "Known false universal statement: n=1; certificate not yet checked here."),
        ("imo_1982_p1", "Known false universal statement: bumped floor(n/3); certificate not yet checked here."),
        ("amc12a_2020_p4", "True finite-cardinality statement; not refuted by these controls."),
        ("mathd_numbertheory_427", "True divisor-sum statement; false prose arithmetic is not the Lean goal."),
    ]:
        candidates = [c for c in raw["original_candidates"] if c["task_id"] == task]
        assert len(candidates) == 32
        pattern = re.compile(r"\btheorem\s+" + re.escape(task) + r"\b")
        headers = collections.defaultdict(list)
        unmatched = []
        for candidate in candidates:
            source = candidate["code"]
            match = pattern.search(source)
            if match is None or ":= by" not in source[match.start():]:
                unmatched.append({"id": candidate["id"], "source": source})
                continue
            header = source[match.start():].split(":= by", 1)[0]
            headers[header].append(candidate["id"])
        assert len(headers) == 1
        attempts = [a for c in candidates for a in raw["attempts"][c["id"]]]
        tasks.append({
            "task": task, "interpretation": interpretation,
            "candidates": len(candidates),
            "exact_text_headers": [{"header": h, "ids": ids} for h, ids in headers.items()],
            "unmatched_sources": unmatched,
            "statuses": dict(collections.Counter(by_id[c["id"]]["status"] for c in candidates)),
            "admitted_attempt_envelopes_seconds_sum": math.fsum(a["wall_seconds"] for a in attempts),
            "exclusive_envelopes_seconds_sum": math.fsum(a["wall_seconds"] for a in attempts if a["exclusive"]),
        })
    points = sorted(set(range(12)) | set(range(1978, 1987)) | set(range(9997, 10003)))
    def model(n):
        return 661 if n == 1982 else n // 3
    tested = [(m, n) for m in points for n in points]
    assert all(max(0, model(m+n) - model(m) - model(n)) in (0, 1) for m, n in tested)
    assert (model(2), model(3), model(9999), model(1982)) == (0, 1, 3333, 661)
    assert sum(d for d in [1]) != 13
    return {
        "population": 7808, "source": str(POINT.relative_to(ROOT)),
        "tasks": tasks,
        "finite_integer_sanity": {"pairs": len(tested), "all_pass": True,
            "scope": "Finite arithmetic check only; not proof of the infinite hypothesis or execution of Lean certificates."},
        "lean_certificate_execution": "pending: one owned native collection already active",
        "limits": [
            "Text/task association is descriptive and is not a parser, context guard or production matcher.",
            "No mathematical-falsity label authorizes rejecting source containing additional axioms or overridden behavior.",
            "Known false statements are prior work, not our novelty; no benchmark correction is made.",
            "Overlapping admitted attempt envelopes are not end-to-end wall time, CPU sums, Amdahl fractions or predicted savings.",
            "Original timeout and resource-failure labels are preserved; no result is silently reclassified.",
        ],
    }

if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
