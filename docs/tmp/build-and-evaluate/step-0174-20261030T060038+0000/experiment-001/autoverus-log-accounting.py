"""Read-only accounting of retained historical log labels; no verifier or generator."""
import argparse
import collections
import csv
import datetime
import json
from pathlib import Path
import re
import tarfile

STAMP = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) (?:INFO|WARNING|ERROR|DEBUG): (.*)$")
INFER = re.compile(r"Infer time: ([0-9.eE+-]+)s")

def aggregate(rows):
    span = sum(x["span_s"] for x in rows)
    inference = sum(x["logged_inference_s"] for x in rows)
    return dict(logs=len(rows), logger_span_s=span, logged_inference_s=inference,
                unattributed_residual_s=span-inference,
                logged_inference_over_logger_span=inference/span,
                inference_events=sum(x["inference_events"] for x in rows))

def analyze(archive, out):
    rows, timing_implementation_matches = [], []
    with tarfile.open(archive, "r:gz") as source:
        for member in source:
            if not member.isfile() or not member.name.endswith((".time", ".py")):
                continue
            text = source.extractfile(member).read().decode("utf-8", "replace")
            if member.name.endswith(".py"):
                if "Infer time:" in text:
                    timing_implementation_matches.append(member.name)
                continue
            stamps, durations, intervals = [], [], []
            for line in text.splitlines():
                match = STAMP.match(line)
                if not match:
                    continue
                stamp = datetime.datetime.strptime(match[1], "%Y-%m-%d %H:%M:%S")
                stamps.append(stamp)
                inference = INFER.fullmatch(match[2])
                if inference:
                    duration = float(inference[1])
                    assert duration >= 0
                    durations.append(duration)
                    end = stamp.replace(tzinfo=datetime.timezone.utc).timestamp()
                    intervals.append((end-duration, end))
            assert stamps and stamps[-1] >= stamps[0], member.name
            span = (stamps[-1]-stamps[0]).total_seconds()
            rows.append(dict(
                log=member.name, folder=member.name.split("autoverus-generated/")[1].split("/")[0],
                span_s=span, logged_inference_s=sum(durations), residual_s=span-sum(durations),
                inference_events=len(durations),
                finished=bool(re.search(r"^.* INFO: finished!$", text, re.M)),
                overlap_above_one_second=sum(a[1]-b[0] > 1 for a,b in zip(intervals,intervals[1:])),
            ))
    assert len(rows) == 196 and all(x["finished"] for x in rows)
    assert sum(x["inference_events"] for x in rows) == 1652
    assert all(x["residual_s"] >= -1 for x in rows)
    assert sum(x["overlap_above_one_second"] for x in rows) == 0
    out.mkdir(parents=True, exist_ok=False)
    with (out/"per-log.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(aggregate=aggregate(rows),
                  by_folder={k: aggregate([x for x in rows if x["folder"] == k])
                             for k in sorted({x["folder"] for x in rows})},
                  negative_residual_logs=[x for x in rows if x["residual_s"] < 0],
                  archived_python_inference_timer_implementation_matches=timing_implementation_matches,
                  exact_generation_to_verification_ratio=None,
                  limitations=[
                      "Historical Infer-time labels include observed API waits/retries; not pure model compute.",
                      "Logger endpoints have one-second resolution; two negative residuals remain retained.",
                      "Residual includes verification and other/unlogged work, not verified timing alone.",
                      "Archived current Python sources do not reconstruct the historical timer implementation.",
                      "No2026 replay clock or cross-node clock enters this historical logger denominator.",
                  ])
    (out/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    return result

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(analyze(args.archive,args.out),indent=2))
