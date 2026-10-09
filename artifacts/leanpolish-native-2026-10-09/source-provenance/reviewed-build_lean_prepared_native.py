#!/usr/bin/env python3
"""Compile declared thin glue with the unmodified official Lean toolchain."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sysroot", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent.parent
    args.out.mkdir(parents=True, exist_ok=True)
    c = args.out / "LeanPreparedNative.c"
    obj = args.out / "lean_prepared_fork.o"
    native = args.out / "LeanPreparedNative"
    commands = [[str(args.sysroot / "bin/lean"), "-c", str(c), str(repo / "bench/LeanPreparedNative.lean")],
                ["g++", "-std=c++17", "-O2", "-fPIC", "-I" + str(args.sysroot / "include"), "-c",
                 str(repo / "bench/lean_prepared_fork.cpp"), "-o", str(obj)],
                [str(args.sysroot / "bin/leanc"), "-O3", "-o", str(native), str(c), str(obj)]]
    versions = {"lean": subprocess.check_output([str(args.sysroot / "bin/lean"), "--version"], text=True),
                "g++": subprocess.check_output(["g++", "--version"], text=True)}
    for command in commands:
        print(json.dumps(command), flush=True)
        subprocess.run(command, cwd=repo, check=True)
    hashes = {}
    for path in (repo / "bench/LeanPreparedNative.lean", repo / "bench/lean_prepared_fork.cpp", c, obj, native):
        with path.open("rb") as file:
            hashes[str(path)] = hashlib.file_digest(file, "sha256").hexdigest()
    args.receipt.write_text(json.dumps({"commands": commands, "cwd": str(repo), "versions": versions,
                                       "sha256": hashes}, indent=2) + "\n")


if __name__ == "__main__":
    main()
