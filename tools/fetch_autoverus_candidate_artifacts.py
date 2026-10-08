#!/usr/bin/env python3
"""Fetch the published main AutoVerus candidate cohort and native context.

Artifact acquisition only, not a research experiment or verifier result.
Uses the original public archive; no repository checkout is created.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request

REVISION = "cbf9c0c6337b224fd8e5b7cb4e01ae65c0f98bc1"
BASE = "https://api.github.com/repos/microsoft/verus-proof-synthesis"


def selected(path):
    return (path.startswith("generated/autoverus/autoverus-generated/")
            or path.startswith("benchmarks/Verus-Bench/")
            or path in {"README.md", "README-artifact-evaluation.md", "LICENSE"}
            or (path.startswith("autoverus/")
                and (path.endswith(".py") or path.endswith("README.md"))))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    req = urllib.request.Request(BASE + "/git/trees/" + REVISION + "?recursive=1",
                                 headers={"User-Agent": "gpu-smt-source-research"})
    raw_tree = urllib.request.urlopen(req, timeout=60).read()
    (args.out / "tree.json").write_bytes(raw_tree)
    tree = json.loads(raw_tree)
    if tree.get("truncated"):
        raise RuntimeError("Official tree is truncated")
    expected = {r["path"]: r for r in tree["tree"]
                if r["type"] == "blob" and selected(r["path"])}
    url = "https://codeload.github.com/microsoft/verus-proof-synthesis/tar.gz/" + REVISION
    seen = set()
    with urllib.request.urlopen(url, timeout=60) as response:
        with tarfile.open(fileobj=response, mode="r|gz") as archive:
            for member in archive:
                if not member.isfile() or "/" not in member.name:
                    continue
                name = member.name.split("/", 1)[1]
                if name not in expected:
                    continue
                rel = Path(name)
                if rel.is_absolute() or ".." in rel.parts:
                    raise RuntimeError("Unexpected archive path")
                source = archive.extractfile(member)
                payload = source.read()
                blob = hashlib.sha1(b"blob " + str(len(payload)).encode()
                                    + b"\0" + payload).hexdigest()
                if blob != expected[name]["sha"]:
                    raise RuntimeError("Official Git blob mismatch: " + name)
                target = args.out / "raw" / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
                seen.add(name)
                if len(seen) % 500 == 0:
                    print("retained", len(seen), "files", flush=True)
    missing = sorted(set(expected) - seen)
    (args.out / "acquisition.json").write_text(json.dumps(
        dict(revision=REVISION, archive_url=url, selected=len(expected),
             retained=len(seen), missing=missing,
             tree_sha256=hashlib.sha256(raw_tree).hexdigest()), indent=2) + "\n")
    print("retained", len(seen), "of", len(expected), "files", flush=True)
    if missing:
        raise RuntimeError("Missing selected public files")


if __name__ == "__main__":
    main()
