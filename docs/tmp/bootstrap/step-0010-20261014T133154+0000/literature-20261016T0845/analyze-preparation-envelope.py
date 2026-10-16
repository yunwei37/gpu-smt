#!/usr/bin/env python3
"""Recompute same-capture request/body timing for an already retained native run.

No native workload is run. Nominal/error timers remain separate, and no CPU or
causal speedup fraction is inferred from overlapping per-request wall clocks.
"""
import argparse
import collections
import json
import math
from pathlib import Path
import zipfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive", type=Path, required=True)
    ap.add_argument("--terminal", type=Path, required=True)
    ap.add_argument("--event-scope", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    terminal = json.loads(args.terminal.read_text())
    events = json.loads(args.event_scope.read_text())["events"]
    prepared = set(events["prepared_ids"])
    reused = set(events["reused_ids"])
    counts = collections.Counter()
    durations = collections.defaultdict(float)
    headers, residual_errors, unmatched = [], [], []
    first_admission, last_response = None, None
    with zipfile.ZipFile(args.archive) as z:
        candidates = [n for n in z.namelist() if n.endswith("/results.jsonl")]
        if len(candidates) != 1:
            raise ValueError("expected exactly one original results stream")
        member = candidates[0]
        prefix = member.removesuffix("results.jsonl")
        with z.open(member) as f:
            for line in f:
                row = json.loads(line)
                pid = row["proof_id"]
                request = row["elapsed_seconds"]
                first_admission = min(first_admission or row["admitted_ns"], row["admitted_ns"])
                last_response = max(last_response or row["response_ns"], row["response_ns"])
                counts["all"] += 1
                counts["basic_" + row["basic"]] += 1
                durations["all_request_wall_sum"] += request
                payload = json.loads(z.read(prefix + row["raw_response"]))
                items = payload.get("results", [])
                item = items[0] if len(items) == 1 else {}
                identity = str(item.get("custom_id")) == pid
                value = (item.get("response") or {}).get("time")
                qualified = (identity and row["status_code"] == 200 and not item.get("error")
                             and row["basic"] in ["complete", "rejected"]
                             and isinstance(value, (int, float)) and not isinstance(value, bool)
                             and math.isfinite(value) and value >= 0)
                if qualified:
                    outside = request - value
                    counts["measured_body_timer"] += 1
                    durations["qualified_request_wall_sum"] += request
                    durations["qualified_body_io_wall_sum"] += value
                    durations["qualified_outside_body_wall_sum"] += outside
                    if outside < 0:
                        residual_errors.append(dict(proof_id=pid, request=request, body=value))
                else:
                    counts["unpartitioned"] += 1
                    durations["unpartitioned_request_wall_sum"] += request
                if pid not in prepared and pid not in reused:
                    unmatched.append(pid)
                if pid in prepared:
                    headers.append(dict(proof_id=pid, source_index=row["source_index"],
                        basic=row["basic"], request_seconds=request, body_timer_qualified=qualified,
                        reported_body_seconds=value if qualified else None,
                        nonbody_or_unpartitioned_seconds=request - value if qualified else request))
    header_envelope = sum(v["nonbody_or_unpartitioned_seconds"] for v in headers)
    whole = terminal["whole_seconds"]
    normalized = header_envelope / whole
    result = dict(archive=str(args.archive), terminal=str(args.terminal),
        scope="same-capture wall-clock accounting; not CPU fractions or measured causal speedup",
        whole_seconds=whole, counts=dict(counts), durations=dict(durations),
        header_events=len(headers), header_envelope_sum_seconds=header_envelope,
        header_envelope_normalized_by_whole=normalized,
        conditional_fixed_other_work_speedup=1 / (1 - normalized),
        qualified_body_share_of_qualified_request_sum=(
            durations["qualified_body_io_wall_sum"] / durations["qualified_request_wall_sum"]),
        before_first_admission_seconds=(first_admission - terminal["begin_ns"]) / 1e9,
        after_last_response_seconds=(terminal["end_ns"] - last_response) / 1e9,
        negative_residuals=residual_errors, unmatched_event_ids=unmatched, header_rows=headers)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "header_rows"}))


if __name__ == "__main__":
    main()
