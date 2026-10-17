"""Describe observed successful oracle branches and fallback telemetry.
Nested invocation-wall timers are not CPU fractions or a GPU speedup bound.
"""
from pathlib import Path
import argparse, collections, gzip, json

HEADER = "import Mathlib\nimport Aesop\n"
ROOT = Path("/workspaces/repository")
INPUT = ROOT / "artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl"

def spread(values):
    if not values:
        return None
    values = sorted(values)
    return {"observations": len(values), "min": values[0],
            "median": values[len(values)//2],
            "p95": values[int(.95*(len(values)-1))], "max": values[-1]}

def analyze(cell, inputs=INPUT):
    terminal = json.loads((cell / "terminal.json").read_text())
    body_ids = collections.defaultdict(list)
    for line in inputs.open():
        item = json.loads(line)
        if not item["code"].startswith(HEADER):
            raise ValueError("unexpected original source header")
        body_ids["\n\n" + item["code"][len(HEADER):]].append(item["proof_id"])
    raw = next((cell / name for name in ["oracle.jsonl", "oracle.jsonl.gz"]
                if (cell / name).exists()), None)
    if raw is None:
        raise FileNotFoundError("no diagnostic oracle telemetry")
    open_text = gzip.open if raw.suffix == ".gz" else open
    kinds = collections.Counter()
    success = fallback = malformed = missing = 0
    groups = {"direct": set(), "fallback": set()}
    unmatched = set()
    errors = collections.Counter()
    totals = collections.defaultdict(int)
    sizes = collections.defaultdict(list)
    with open_text(raw, "rt") as stream:
        for number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
            except ValueError:
                malformed += 1
                continue
            kind = row.get("ty", "(missing)")
            kinds[kind] += 1
            if kind not in ["direct-oracle", "direct-oracle-fallback"]:
                continue
            body = row.get("source")
            if body not in body_ids:
                unmatched.add(body)
            if kind == "direct-oracle-fallback":
                fallback += 1
                groups["fallback"].add(body)
                message = str(row.get("error", "(missing)")).splitlines()
                errors[message[0] if message else "(empty)"] += 1
                continue
            success += 1
            groups["direct"].add(body)
            oracle = row.get("oracle")
            if not isinstance(oracle, dict):
                missing += 1
                continue
            caller = ["export_ns", "search_roundtrip_ns", "check_ns"]
            nested = ["linear_ns", "products_ns", "lp_ns"]
            if not all(type(row.get(k)) is int for k in caller) or not all(
                    type(oracle.get(k)) is int for k in nested):
                missing += 1
                continue
            for key in caller:
                totals[key] += row[key]
            for key in nested:
                totals[key] += oracle[key]
            for key in ["facts", "atoms"]:
                if type(oracle.get(key)) is int:
                    sizes[key].append(oracle[key])
            cert = oracle.get("cert")
            if isinstance(cert, list):
                sizes["certificate_terms"].append(len(cert))
                sizes["selected_product_terms"].append(sum(
                    isinstance(x.get("origin"), list) and x["origin"][0] == "mul"
                    for x in cert))
    direct = groups["direct"] & body_ids.keys()
    fallbacks = groups["fallback"] & body_ids.keys()
    both = direct & fallbacks
    return {
        "receipt": terminal, "telemetry_kinds": dict(kinds),
        "successful_checked_branch_records": success,
        "fallback_attempt_records": fallback,
        "malformed_telemetry_lines": malformed,
        "success_records_without_complete_timer_fields": missing,
        "input_body_groups": len(body_ids),
        "ambiguous_input_body_groups": sum(len(ids)>1 for ids in body_ids.values()),
        "body_groups_with_observed_direct_check": len(direct),
        "body_groups_with_observed_fallback": len(fallbacks),
        "body_groups_with_both": len(both),
        "unmatched_telemetry_body_groups": len(unmatched),
        "fallback_errors": dict(errors),
        "successful_branch_wall_seconds": {k:v/1e9 for k,v in totals.items()},
        "successful_branch_size_distributions": {k:spread(v) for k,v in sizes.items()},
        "body_group_source_ids": [
            {"proof_ids": body_ids[b], "direct": b in direct, "fallback": b in fallbacks}
            for b in body_ids if b in direct or b in fallbacks],
        "scope": (
            "Only observed checked contradiction branches have timers. A tactic can "
            "produce several branch checks and later fall back; record counts are "
            "not a mutually exclusive success rate. Source bodies identify groups, "
            "not individual repeated candidate instances. Failed/unsupported paths "
            "lack these timers and their cost is unknown, never zero. Rust linear/"
            "products/LP timers are nested inside Lean search roundtrip; do not "
            "add parent and child times. Serialized/overlapping invocation wall "
            "is not total CPU, a complete wall fraction, or an ideal GPU bound. "
            "Headline whole times already include all failed work and fallback. "
            "Native response agreement must be checked separately."
        )}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cell", type=Path)
    parser.add_argument("--input", type=Path, default=INPUT)
    args = parser.parse_args()
    result = analyze(args.cell, args.input)
    (args.cell / "oracle-analysis.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ["receipt", "body_group_source_ids"]}, indent=2))

if __name__ == "__main__":
    main()
