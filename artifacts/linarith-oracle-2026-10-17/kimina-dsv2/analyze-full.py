"""Recompute the declared six DSV2 cells from returned SDK data and terminals.
Works on the public closed-cells mirror; original request payloads are unnecessary.
"""
import argparse
import collections
import gzip
import json
from pathlib import Path


def rows(path):
    if not path.exists():
        path = path.with_name(path.name + ".gz")
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as stream:
        return [json.loads(line) for line in stream if line.strip()]


def non_messages(row):
    return {k: v for k, v in row["result"].get("response", {}).items() if k != "messages"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    ids = json.loads((args.root / "source-ids.json").read_text())
    assert len(ids) == len(set(ids)) == 438
    observations = {}
    for rep in [1, 2, 3]:
        for method in ["native", "power"]:
            name = f"rep{rep}-{method}"
            directory = args.root / name
            term = json.loads((directory / "terminal.json").read_text())
            data = rows(directory / "results.jsonl")
            assert term["state"] == "complete"
            assert [x["proof_id"] for x in data] == ids
            assert len(data) == term["expected"] == term["returned"] == 438
            assert dict(collections.Counter(x["status"] for x in data)) == term["counts"]
            assert term["affinity"] == [16, 17, 18, 19]
            assert term["memory_limit_bytes"] == 51539607552
            assert not term["owned_live_descendants_after_shutdown"]
            if method == "native":
                assert term["native_engine"] == "tiered" and term["native_hybrid_override"] is None
            observations[name] = {"terminal": term, "rows": {x["proof_id"]: x for x in data}}
    reference = observations["rep1-native"]["rows"]
    fidelity = {}
    for name, observed in observations.items():
        data = observed["rows"]
        fidelity[name] = {
            "status_difference_IDs": [i for i in ids if data[i]["status"] != reference[i]["status"]],
            "non_message_difference_IDs": [i for i in ids if non_messages(data[i]) != non_messages(reference[i])],
            "raw_response_difference_IDs": [
                i for i in ids if data[i]["result"].get("response") != reference[i]["result"].get("response")],
        }
    pairs = []
    for rep in [1, 2, 3]:
        native = observations[f"rep{rep}-native"]
        power = observations[f"rep{rep}-power"]
        n, p = native["terminal"], power["terminal"]
        differences = [i for i in ids if native["rows"][i]["result"].get("response") != power["rows"][i]["result"].get("response")]
        details = []
        for ident in differences:
            nm = native["rows"][ident]["result"].get("response", {}).get("messages", [])
            pm = power["rows"][ident]["result"].get("response", {}).get("messages", [])
            details.append({
                "proof_id": ident,
                "native_status": native["rows"][ident]["status"],
                "power_status": power["rows"][ident]["status"],
                "native_message_severities": dict(collections.Counter(x.get("severity") for x in nm)),
                "power_message_severities": dict(collections.Counter(x.get("severity") for x in pm)),
            })
        pairs.append({
            "rep": rep, "order": ["native", "power"] if rep != 2 else ["power", "native"],
            "native_whole_seconds": n["whole_lifecycle_seconds"],
            "power_whole_seconds": p["whole_lifecycle_seconds"],
            "native_warm_seconds": n["warm_verify_seconds"],
            "power_warm_seconds": p["warm_verify_seconds"],
            "native_over_power_whole": n["whole_lifecycle_seconds"] / p["whole_lifecycle_seconds"],
            "native_over_power_warm": n["warm_verify_seconds"] / p["warm_verify_seconds"],
            "response_differences": details,
        })
    sums = {key: sum(x[key] for x in pairs) for key in [
        "native_whole_seconds", "power_whole_seconds", "native_warm_seconds", "power_warm_seconds"]}
    out = {
        "dataset": "All438official DeepSeek-Prover-V2 miniF2F proof outputs in retained4.27environment",
        "completed_observations": len(observations), "source_runs": sum(len(x["rows"]) for x in observations.values()),
        "pairs": pairs,
        "aggregate": {
            **sums,
            "native_over_power_whole": sums["native_whole_seconds"] / sums["power_whole_seconds"],
            "native_over_power_warm": sums["native_warm_seconds"] / sums["power_warm_seconds"],
            "whole_elapsed_reduction_fraction": 1 - sums["power_whole_seconds"] / sums["native_whole_seconds"],
            "pair_whole_ratio_range": [min(x["native_over_power_whole"] for x in pairs),
                                      max(x["native_over_power_whole"] for x in pairs)],
        },
        "counts": {k: v["terminal"]["counts"] for k, v in observations.items()},
        "cross_observation_fidelity_vs_first_native": fidelity,
        "scope": "Complete predeclared three-pair descriptive result; shared host and short root analysis/build co-tenancy, equal CPU eligibility rather than exclusive resources.48GiB is per-process address space, not aggregate fleet memory. No confidence interval, pure CPU/LP fraction, GPU benefit,4.31replication, universal acceleration or systems novelty follows. Root self-review only.",
    }
    destination = args.out or args.root / "full-summary.json"
    destination.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"source_runs": out["source_runs"], "aggregate": out["aggregate"],
                      "fidelity": fidelity}, indent=2))


if __name__ == "__main__":
    main()
