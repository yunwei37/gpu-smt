"""Compare closed native/SHRED cells, exposing all opaque-handle differences."""
import argparse
import collections
import gzip
import json
from pathlib import Path
import re

def rows(path):
    if not path.exists():
        path = path.with_name(path.name + ".gz")
    with (gzip.open(path, "rt") if path.suffix == ".gz" else path.open()) as stream:
        return [json.loads(line) for line in stream]

def verification_outcome(row):
    response = row["result"].get("response", {})
    if row["status"] not in ("valid", "lean_error", "sorry"):
        return "operational"
    if response.get("message") or response.get("error"):
        return "operational"
    if any(message.get("severity") == "error" for message in response.get("messages", [])):
        return "rejected"
    if response.get("sorries") or any("sorry" in message.get("data", "")
            for message in response.get("messages", []) if message.get("severity") == "warning"):
        return "incomplete"
    return "complete"

def analyze(root):
    data = {}
    terms = {}
    for method in ("native", "shred"):
        directory = root / ("rep1-" + method)
        terms[method] = json.loads((directory / "terminal.json").read_text())
        data[method] = rows(directory / "results.jsonl")
        term = terms[method]
        assert term["state"] == "complete"
        assert not term["owned_live_descendants_after_shutdown"]
        assert term["affinity"] == [4, 5, 6, 7]
        assert term["memory_limit_bytes"] == 51539607552
        assert term["lean_version"] == "v4.9.0-rc1"
        assert len(data[method]) == term["expected"] == term["returned"]
        assert dict(collections.Counter(row["status"] for row in data[method])) == term["counts"]
    ids = [row["proof_id"] for row in data["native"]]
    assert ids == [row["proof_id"] for row in data["shred"]]
    result = dict(scope="Closed source-native HTTP integration comparison; opaque env handles and all messages remain visible. Not snapshot/protocol transparency or a full population claim unless all original IDs are independently verified.",
        source_count=len(ids), conditions={}, status_differences=[], native_verification_differences=[],
        non_message_differences=[], raw_response_difference_IDs=[],
        cached_message_events={})
    for method, term in terms.items():
        result["conditions"][method] = {key:term[key] for key in [
            "counts", "whole_lifecycle_seconds", "whole_with_input_preparation_seconds",
            "warm_verify_seconds", "input_preparation_seconds", "joined_owned_descendants",
            "lean_version"]}
        result["conditions"][method]["native_verification_counts"] = dict(
            collections.Counter(verification_outcome(row) for row in data[method]))
    events = collections.Counter()
    for base, cache in zip(data["native"], data["shred"]):
        ident = base["proof_id"]
        if verification_outcome(base) != verification_outcome(cache):
            result["native_verification_differences"].append(dict(proof_id=ident,
                native=verification_outcome(base), shred=verification_outcome(cache)))
        if base["status"] != cache["status"]:
            result["status_differences"].append(dict(proof_id=ident,
                native=base["status"], shred=cache["status"]))
        before = base["result"].get("response", {})
        after = cache["result"].get("response", {})
        fields = {key:[before.get(key), after.get(key)] for key in set(before)|set(after)
                  if key != "messages" and before.get(key) != after.get(key)}
        if fields:
            result["non_message_differences"].append(dict(proof_id=ident, fields=fields))
        if before != after:
            result["raw_response_difference_IDs"].append(ident)
        for message in after.get("messages", []):
            events.update(re.findall(r"LEAN_PREFIX_CERT event=([a-z_]+)", message.get("data", "")))
    result["cached_message_events"] = dict(events)
    result["non_message_difference_fields"] = sorted({key for row in result["non_message_differences"] for key in row["fields"]})
    result["operational_statuses"] = {method:dict(collections.Counter(
        row["status"] for row in items if row["status"] not in ("valid", "lean_error", "sorry")))
        for method, items in data.items()}
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", type=Path, nargs="+")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = {str(root):analyze(root) for root in args.roots}
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({label:dict(sources=value["source_count"],
        status_differences=len(value["status_differences"]),
        non_message_fields=value["non_message_difference_fields"],
        events=value["cached_message_events"]) for label,value in result.items()}))
