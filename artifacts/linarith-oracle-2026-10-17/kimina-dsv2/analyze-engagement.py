"""Join closed numeric race source tags to original IDs; emit no proof payload."""
import argparse
import collections
import json
from pathlib import Path

def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def body(code):
    # The acquired corpus has exactly the two checked common import lines.
    lines = code.splitlines()
    assert [line for line in lines if line.startswith("import ")] == ["import Mathlib", "import Aesop"]
    return "\n".join(line for line in lines if not line.startswith("import ")).strip()

def analyze(inputs, raw, projection):
    items = read_rows(inputs)
    source_ids = [item["proof_id"] for item in items]
    assert len(source_ids) == len(set(source_ids)) == 438
    by_body = collections.defaultdict(list)
    for item in items:
        by_body[body(item["code"])].append(item["proof_id"])
    measured = json.loads(projection.read_text())
    result = {"scope": "All closed DSV2 large numeric races joined by exact source-body equality. Recorded race wall is not all LP, CPU or removable whole time; legacy gpu is CPU HiGHS. Root self-review.", "pairs": []}
    for rep in (1, 2, 3):
        races = collections.defaultdict(list)
        raw_rows = read_rows(raw / f"rep{rep}-power/lp-races.jsonl")
        for row in raw_rows:
            matches = by_body[row["source"].strip()]
            assert len(matches) == 1, "Missing or ambiguous actual source tag"
            races[matches[0]].append(row)
        assert len(raw_rows) == sum(map(len, races.values())) == 193
        cells = {method: {row["proof_id"]: row for row in measured["conditions"][f"rep{rep}-{method}"]["per_source"]} for method in ("native", "power")}
        assert all(set(cell) == set(source_ids) for cell in cells.values())
        sources = []
        for ident in source_ids:
            rows = races[ident]
            sources.append({
                "proof_id": ident,
                "status": cells["power"][ident]["status"],
                "native_body_seconds": cells["native"][ident]["reported_body_seconds"],
                "power_body_seconds": cells["power"][ident]["reported_body_seconds"],
                "recorded_large_races": len(rows),
                "recorded_race_whole_seconds_sum": sum(row["whole_ns"] for row in rows) / 1e9,
                "recorded_race_decision_seconds_sum": sum(row["decision_ns"] for row in rows) / 1e9,
                "recorded_race_retirement_seconds_sum": sum(row["retirement_ns"] for row in rows) / 1e9,
                "legacy_winners": dict(collections.Counter(row["winner"] for row in rows)),
            })
        groups = {}
        for engaged in (True, False):
            selected = [row for row in sources if bool(row["recorded_large_races"]) == engaged]
            groups["recorded_large_race" if engaged else "no_recorded_large_race"] = {
                "sources": len(selected),
                "native_body_seconds_sum_NOT_CPU_or_removable_wall": sum(row["native_body_seconds"] for row in selected),
                "power_body_seconds_sum_NOT_CPU_or_removable_wall": sum(row["power_body_seconds"] for row in selected),
            }
        result["pairs"].append({"rep": rep, "races": len(raw_rows), "unique_sources_with_recorded_large_race": sum(bool(rows) for rows in races.values()), "groups": groups,
            "native_ranked_top5": sorted(sources, key=lambda row: row["native_body_seconds"], reverse=True)[:5], "all_sources": sources})
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--projection", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.input, args.raw, args.projection)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps([{"rep": row["rep"], "races": row["races"], "sources": row["unique_sources_with_recorded_large_race"]} for row in result["pairs"]]))
