"""Whole closed-trace reuse census; no native replay or performance claim."""
from pathlib import Path
import argparse, collections, decimal, gzip, json, statistics, sys, time, zipfile
from datetime import datetime, timezone

def freeze(value):
    if value is None: return ("null",)
    if type(value) is bool: return ("bool", value)
    if type(value) is int: return ("int", value)
    if isinstance(value, decimal.Decimal): return ("number", value.as_tuple())
    if isinstance(value, str): return ("str", value)
    if isinstance(value, list): return ("list", tuple(map(freeze, value)))
    if isinstance(value, dict): return ("object", tuple((key, freeze(item)) for key, item in value.items()))
    raise TypeError(type(value).__name__)

def distribution(values):
    ordered = sorted(values)
    if not ordered: return {"n": 0}
    return {"n": len(ordered), "min": ordered[0], "median": statistics.median(ordered),
            "p95_lower_rank": ordered[int(.95 * (len(ordered)-1))], "max": ordered[-1]}

def dump_lines(path, rows):
    with gzip.open(path, "wt", encoding="utf8") as output:
        for row in rows: output.write(json.dumps(row) + "\n")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Real archived coefficients exceed the Python default 4300-digit reader limit.
    # This applies only to this read-only analysis process, not any verifier/runtime.
    sys.set_int_max_str_digits(0)
    started = time.monotonic()
    originals = [json.loads(line) for line in args.inputs.read_bytes().splitlines() if line.strip()]
    input_codes = collections.defaultdict(list)
    for row in originals: input_codes[row["code"]].append(row["index"])
    source_codes = {}; source_rows = []; key_ids = {}; groups = []; events = []
    kinds = collections.Counter(); outcomes = collections.Counter(); malformed = []
    dimensions = []; hypothesis_counts = []; coefficient_entries = []; durations = []
    bytes_read = 0; lines_read = 0; integer_coefficients = 0; other_coefficients = 0; max_bits = 0
    with zipfile.ZipFile(args.archive) as archive:
        names = [name for name in archive.namelist() if name.endswith("/oracle.jsonl")]
        if len(names) != 1: raise ValueError("Expected one discovered oracle.jsonl member: " + repr(names))
        member = names[0]; declared_bytes = archive.getinfo(member).file_size
        with archive.open(member) as stream:
            for raw in stream:
                lines_read += 1; bytes_read += len(raw)
                if not raw.strip(): kinds["blank"] += 1; continue
                try: row = json.loads(raw, parse_float=decimal.Decimal)
                except (ValueError, UnicodeDecodeError) as error:
                    malformed.append({"line": lines_read, "error_type": type(error).__name__, "error": str(error)[:240]}); continue
                if not isinstance(row, dict): kinds["non_object_json"] += 1; continue
                if "lp" not in row: kinds["metadata:" + str(row.get("ty", "untyped"))] += 1; continue
                kinds["lp"] += 1
                source = row.get("source"); sid = -1
                if isinstance(source, str):
                    if source not in source_codes:
                        sid = len(source_rows); source_codes[source] = sid
                        source_rows.append({"source_id": sid, "characters": len(source),
                            "exact_input_indices": input_codes.get(source, [])})
                    sid = source_codes[source]
                lp = row["lp"]; key = freeze(lp)
                if key not in key_ids:
                    gid = len(groups); key_ids[key] = gid
                    groups.append({"group_id": gid, "first_trace_line": lines_read, "count": 0,
                                   "successful": 0, "failed": 0, "other_outcome": 0,
                                   "sources": set(), "earliest_success_end_ns": None})
                gid = key_ids[key]; group = groups[gid]; group["count"] += 1
                if sid >= 0: group["sources"].add(sid)
                outcome = "successful" if row.get("ok") is True else "failed" if row.get("ok") is False else "other_outcome"
                group[outcome] += 1; outcomes[outcome] += 1
                start = row.get("start_ns"); elapsed = row.get("elapsed_ns")
                timed = type(start) is int and type(elapsed) is int and elapsed >= 0
                if timed:
                    durations.append(elapsed)
                    end = start + elapsed
                    if outcome == "successful":
                        old = group["earliest_success_end_ns"]
                        group["earliest_success_end_ns"] = end if old is None else min(old, end)
                events.append({"trace_line": lines_read, "group_id": gid, "source_id": sid,
                               "outcome": outcome, "start_ns": start if timed else None,
                               "elapsed_ns": elapsed if timed else None})
                if isinstance(lp, dict):
                    if type(lp.get("maxVar")) is int: dimensions.append(lp["maxVar"])
                    hyps = lp.get("hyps")
                    if isinstance(hyps, list):
                        hypothesis_counts.append(len(hyps)); entries = 0
                        for hyp in hyps:
                            if not isinstance(hyp, list) or len(hyp) != 2 or not isinstance(hyp[1], list): continue
                            entries += len(hyp[1])
                            for coefficient in hyp[1]:
                                if isinstance(coefficient, list) and len(coefficient) == 2:
                                    value = coefficient[1]
                                    if type(value) is int:
                                        integer_coefficients += 1; max_bits = max(max_bits, abs(value).bit_length())
                                    else: other_coefficients += 1
                        coefficient_entries.append(entries)
    assert bytes_read == declared_bytes
    pairs = {(event["group_id"], event["source_id"]) for event in events if event["source_id"] >= 0}
    prior_success_events = [
        event for event in events
        if event["outcome"] == "successful" and event["start_ns"] is not None
        and groups[event["group_id"]]["earliest_success_end_ns"] is not None
        and groups[event["group_id"]]["earliest_success_end_ns"] < event["start_ns"]]
    prior_complete_success = len(prior_success_events)
    prior_success_elapsed_sum = sum(event["elapsed_ns"] for event in prior_success_events)
    repeated = [group for group in groups if group["count"] > 1]
    source_exact = [source for source in source_rows if source["exact_input_indices"]]
    prefix = args.output
    query_path = prefix.with_name(prefix.name + "-queries.jsonl.gz")
    group_path = prefix.with_name(prefix.name + "-groups.jsonl.gz")
    source_path = prefix.with_name(prefix.name + "-sources.jsonl.gz")
    dump_lines(query_path, events)
    dump_lines(group_path, ({**group, "sources": sorted(group["sources"])} for group in groups))
    dump_lines(source_path, source_rows)
    result = {
        "utc": datetime.now(timezone.utc).isoformat(), "archive": str(args.archive),
        "member": member, "input_source": str(args.inputs), "input_attempt_rows": len(originals),
        "declared_uncompressed_log_bytes": declared_bytes, "processed_log_bytes": bytes_read,
        "trace_lines": lines_read, "row_kinds": dict(kinds), "malformed_rows": malformed,
        "query_outcomes": dict(outcomes), "lp_queries": len(events), "unique_ordered_lp_problems": len(groups),
        "repeated_problem_groups": len(repeated),
        "repeated_occurrences_beyond_first": sum(group["count"] - 1 for group in groups),
        "queries_in_repeated_groups": sum(group["count"] for group in repeated),
        "successful_repeats_beyond_first_success": sum(max(0, group["successful"] - 1) for group in groups),
        "successful_queries_with_prior_completed_success_same_lp": prior_complete_success,
        "cross_logged_source_text_problem_groups": sum(len(group["sources"]) > 1 for group in groups),
        "distinct_lp_source_pairs": len(pairs),
        "distinct_source_texts": len(source_rows), "source_texts_exactly_matching_input_code": len(source_exact),
        "queries_with_unknown_source": sum(event["source_id"] < 0 for event in events),
        "reported_maxVar": distribution(dimensions), "hypothesis_rows": distribution(hypothesis_counts),
        "coefficient_entries": distribution(coefficient_entries),
        "integer_coefficient_entries": integer_coefficients, "other_coefficient_entries": other_coefficients,
        "largest_integer_coefficient_bits": max_bits, "logged_oracle_elapsed_ns": distribution(durations),
        "sum_logged_oracle_elapsed_ns": sum(durations),
        "sum_logged_elapsed_ns_prior_success_repeats": prior_success_elapsed_sum,
        "repeat_associated_fraction_of_parsed_logged_call_wall_sum": prior_success_elapsed_sum / sum(durations) if sum(durations) else None,
        "integer_reader_scope": "Python integer-string digit restriction disabled only in this offline reader after actual 15955-digit coefficient parse failure; no verifier/SDK/logger/runtime-policy change.",
        "query_rows": str(query_path), "all_groups": str(group_path), "source_mapping": str(source_path),
        "analysis_wall_seconds": time.monotonic() - started,
        "identity": "Exact parsed structural LP identity, preserving object/list order, relations, variable indices, coefficients and all fields. No hypothesis/variable reorder, mathematical canonicalization, rounded coefficients or source filtering.",
        "scope": "Read-only whole closed profile log census, not an executed cache, GPU batch, Meta-query reuse measurement or verifier performance experiment. Per-call elapsed wall intervals can overlap; their sum is not CPU work, whole time or savings. Prior-success-ended-before-start is an observed timestamp predicate, not an actual cache hit or availability/independence proof; worker identities and publication overhead are absent. Logged sources need exact input-code matching; telemetry can omit failures, and LP records do not cover every source/Meta operation. This route differs from E032's plain compiled-original route; no transfer of CPU shares or GPU/Amdahl bound."
    }
    prefix.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ["processed_log_bytes", "trace_lines", "row_kinds",
        "lp_queries", "unique_ordered_lp_problems", "repeated_occurrences_beyond_first",
        "successful_repeats_beyond_first_success", "successful_queries_with_prior_completed_success_same_lp",
        "cross_logged_source_text_problem_groups", "distinct_source_texts", "source_texts_exactly_matching_input_code",
        "analysis_wall_seconds"]}))
if __name__ == "__main__": main()
