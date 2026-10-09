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
    ap.add_argument("--runtime-source", type=Path, required=True)
    ap.add_argument("--uv-source", type=Path, required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent.parent
    args.out.mkdir(parents=True, exist_ok=True)
    c = args.out / "LeanPreparedNative.c"
    obj = args.out / "lean_prepared_fork.o"
    uv_obj = args.out / "lean_prepared_uv.o"
    threads_obj = args.out / "lean_prepared_threads.o"
    native = args.out / "LeanPreparedNative"
    commands = [[str(args.sysroot / "bin/lean"), "-c", str(c), str(repo / "bench/LeanPreparedNative.lean")],
                ["g++", "-std=c++17", "-O2", "-fPIC", "-I" + str(args.sysroot / "include"), "-c",
                 str(repo / "bench/lean_prepared_fork.cpp"), "-o", str(obj)],
                ["g++", "-std=c++17", "-O2", "-fPIC", "-I" + str(args.sysroot / "include"), "-c",
                 str(repo / "bench/lean_prepared_threads.cpp"), "-o", str(threads_obj)],
                [str(args.sysroot / "bin/clang"), "-x", "c++", "-std=c++17", "-O2", "-fPIC",
                 "-DLEAN_MULTI_THREAD", "-isystem", "/usr/include/c++/14", "-isystem", "/usr/include/x86_64-linux-gnu/c++/14",
                 "-isystem", str(args.sysroot / "include/clang"),
                 "-I" + str(args.sysroot / "include"), "-I" + str(args.runtime_source / "src"),
                 "-I" + str(args.uv_source / "include"), "-c", str(repo / "bench/lean_prepared_uv.cpp"), "-o", str(uv_obj)],
                [str(args.sysroot / "bin/leanc"), "-O3", "-rdynamic", "-Wl,--wrap=initialize_libuv",
                 "-Wl,--wrap=pthread_create", "-Wl,--wrap=pthread_detach", "-Wl,--wrap=pthread_join",
                 "-o", str(native), str(c), str(obj), str(uv_obj), str(threads_obj)]]
    versions = {"lean": subprocess.check_output([str(args.sysroot / "bin/lean"), "--version"], text=True),
                "g++": subprocess.check_output(["g++", "--version"], text=True)}
    for command in commands:
        print(json.dumps(command), flush=True)
        subprocess.run(command, cwd=repo, check=True)
    hashes = {}
    for path in (repo / "bench/LeanPreparedNative.lean", repo / "bench/lean_prepared_fork.cpp",
                 repo / "bench/lean_prepared_uv.cpp", repo / "bench/lean_prepared_threads.cpp", c, obj, uv_obj, threads_obj, native):
        with path.open("rb") as file:
            hashes[str(path)] = hashlib.file_digest(file, "sha256").hexdigest()
    args.receipt.write_text(json.dumps({"commands": commands, "cwd": str(repo), "versions": versions,
                                       "sha256": hashes}, indent=2) + "\n")


if __name__ == "__main__":
    main()
