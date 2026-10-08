#!/usr/bin/env python3
"""Reconcile named AutoVerus stages with published saved source files.

These stages are NOT a count of native verifier calls. Native calls inside
debugging, Houdini and scoring may lack log/source records entirely.
Saved annotated files are not asserted to equal original temporary input bytes.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

LOG = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) (INFO|WARNING|ERROR): (.*)$")


def analyze(raw, out):
    cohort = raw / "generated/autoverus/autoverus-generated"
    out.mkdir(parents=True, exist_ok=False)
    summary = {}
    with (out / "events.jsonl").open("w") as events:
        for folder in sorted(cohort.iterdir()):
            totals = Counter()
            for log in sorted(folder.glob("*.time")):
                totals["logs"] += 1
                intermediate = folder / ("intermediate-" + log.stem)
                totals["logs_with_intermediate_dir"] += int(intermediate.is_dir())
                totals["logs_with_final_source"] += int(log.with_suffix(".rs").is_file())
                refinements = 0
                per_log = Counter()
                for lineno, line in enumerate(log.read_text(errors="replace").splitlines(), 1):
                    m = LOG.match(line)
                    if not m:
                        continue
                    timestamp, level, message = m.groups()
                    kind, saved = None, None
                    match = re.fullmatch(r"Checking candidate (\d+-\d+)", message)
                    if match:
                        kind, saved = "named_inference_stage", match[1] + ".rs"
                    match = re.fullmatch(r"Working on merge-(\d+)\.rs", message)
                    if match:
                        kind, saved = "named_merge_stage", "merged-" + match[1] + ".rs"
                    if message.startswith("refining with "):
                        kind, saved = "named_refinement_stage", f"refine-{refinements}.rs"
                        refinements += 1
                    if message.startswith("Running houdini on "):
                        kind = "houdini_stage"
                    if message == "finished!":
                        kind = "finished_message"
                    if kind is None:
                        continue
                    row = dict(log=str(log.relative_to(raw)), line=lineno,
                               timestamp=timestamp, level=level, message=message, kind=kind)
                    totals[kind] += 1
                    per_log[kind] += 1
                    if saved is not None:
                        source = intermediate / saved
                        row["expected_saved_source"] = str(source.relative_to(raw))
                        row["saved_source_present"] = source.is_file()
                        if source.is_file():
                            row["saved_source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
                            totals[kind + "_saved"] += 1
                        else:
                            totals[kind + "_missing"] += 1
                    events.write(json.dumps(row) + "\n")
                totals["logs_with_named_inference"] += int(per_log["named_inference_stage"] > 0)
                totals["logs_with_finished_message"] += int(per_log["finished_message"] > 0)
            sources = list(folder.rglob("*.rs"))
            totals["saved_rs_files"] = len(sources)
            totals["saved_rs_with_compilation_error_label"] = sum(
                bool(re.search(r"//.*Compilation Error: True", p.read_text(errors="replace")))
                for p in sources)
            summary[folder.name] = dict(totals)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("raw", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    analyze(args.raw, args.out)


if __name__ == "__main__":
    main()
