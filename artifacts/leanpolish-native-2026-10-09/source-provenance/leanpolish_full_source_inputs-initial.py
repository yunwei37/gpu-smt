#!/usr/bin/env python3
"""Splice actual released menu requests into byte-identical original files.

This creates a new full-source verification workload, not historical native
tactic calls. Selection uses source paths, never measured timing or outcome.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import tarfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pools", type=Path, required=True)
    ap.add_argument("--runs", type=Path, required=True)
    ap.add_argument("--mathlib", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    rows = []
    with tarfile.open(args.pools) as archive:
        for member in sorted(archive.getmembers(), key=lambda m: m.name):
            if "mathlib_b" in member.name and member.isfile():
                rows.extend(json.loads(line) for line in archive.extractfile(member))
    # Lexicographically first (file, corpus) in each observed top-level domain;
    # all visited sites and menu entries for that pair are retained.
    chosen = {}
    for row in rows:
        domain = row["file"].split("/")[1]
        pair = (row["file"], row["corpus"])
        chosen[domain] = min(pair, chosen.get(domain, pair))
    pairs = set(chosen.values())
    selected = [r for r in rows if (r["file"], r["corpus"]) in pairs]
    sources = {}
    with tarfile.open(args.runs) as archive:
        for file, corpus in sorted(pairs):
            member = f"complete_menu/data/corpora/{corpus}/{file}"
            source = archive.extractfile(member).read()
            assert source == (args.mathlib / file).read_bytes(), member
            sources[file] = source
            target = args.out / "bases" / file
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source)
    jobs = []
    hashes = collections.Counter()
    for site_index, row in enumerate(selected):
        source = sources[row["file"]]
        begin, end = row["start_byte"], row["end_byte"]
        assert source[begin:end] == row["original"].encode(), (row["file"], begin)
        for candidate in row["candidates"]:
            if candidate["skipped"]:
                continue
            replacement = ("by " + candidate["menu_name"]).encode()
            text = source[:begin] + replacement + source[end:]
            index = len(jobs)
            relative = Path("candidates") / f"{index:06d}" / row["file"]
            path = args.out / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text)
            digest = hashlib.sha256(text).hexdigest()
            hashes[(row["file"], digest)] += 1
            jobs.append({"index": index, "base": row["file"], "input": str(relative),
                         "corpus": row["corpus"], "site_index": site_index,
                         "start_byte": begin, "end_byte": end,
                         "menu_idx": candidate["menu_idx"],
                         "menu_name": candidate["menu_name"], "source_sha256": digest,
                         "original_sha256": hashlib.sha256(source).hexdigest(),
                         "recorded_outcome": candidate["outcome"],
                         "recorded_timeout": candidate["timed_out"]})
    (args.out / "selected-pools.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in selected))
    (args.out / "jobs.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in jobs))
    summary = {"domains": chosen, "files": len(pairs), "visited_sites": len(selected),
               "empty_sites": sum(not r["candidates"] for r in selected),
               "entries": sum(len(r["candidates"]) for r in selected),
               "skipped": sum(c["skipped"] for r in selected for c in r["candidates"]),
               "jobs": len(jobs), "distinct_complete_sources": len(hashes),
               "duplicate_excess": sum(n - 1 for n in hashes.values()),
               "recorded_outcomes": dict(collections.Counter(j["recorded_outcome"] for j in jobs)),
               "bytes": sum(len(sources[j["base"]][:j["start_byte"]]) +
                            len(("by " + j["menu_name"]).encode()) +
                            len(sources[j["base"]][j["end_byte"]:]) for j in jobs)}
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
