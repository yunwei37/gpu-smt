#!/usr/bin/env python3
"""Fetch pinned public SMT-LIB benchmarks from GitHub.

This is intentionally separate from the benchmark runner so paper results can
record the exact upstream revision while keeping third-party benchmark files
out of this repository.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request


def raw_url(repo: str, revision: str, path: str) -> str:
    quoted = "/".join(urllib.parse.quote(part) for part in path.split("/"))
    return (
        f"https://raw.githubusercontent.com/{repo}/{revision}/{quoted}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).with_name("real_smt_manifest.json"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/real-smt"),
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)

    index = []
    for item in data["benchmarks"]:
        url = raw_url(item["repo"], item["revision"], item["path"])
        dest = args.out / f'{item["name"]}.smt2'
        print(f"fetch {item['name']}: {url}")
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "gpu-smt-benchmark-fetcher/0.1"},
        )
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            content = response.read()
        dest.write_bytes(content)
        index.append(
            {
                **item,
                "url": url,
                "local_path": str(dest),
                "bytes": len(content),
            }
        )

    (args.out / "index.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
