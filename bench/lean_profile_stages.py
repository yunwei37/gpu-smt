#!/usr/bin/env python3
"""Retain paired normal/disabled-check frontend profiles for pinned arena tests."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arena", default="/tmp/lean-kernel-arena")
    ap.add_argument("--lean", default="/root/.elan/bin/lean")
    ap.add_argument("--cores", default="0-7")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    runs = []
    for case in ["magma-list-deep-n36", "grind-ring-5"]:
        original = Path(args.arena)/"_build/tests/work/perf"/case/"src/Test.lean"
        source = original.read_text()
        for skip in [True, False]:
            modified = source.replace("set_option debug.skipKernelTC true", f"set_option debug.skipKernelTC {str(skip).lower()}")
            # Insert after the module header if present. The prior profile had
            # inserted before it, which produced a syntax error.
            lines = modified.splitlines(keepends=True)
            position = 1 if lines[0].strip() == "module" else 0
            lines.insert(position, f"set_option profiler true\nset_option debug.skipKernelTC {str(skip).lower()}\n")
            path = out/(case.replace("-", "_") + ("_skip" if skip else "_check") + ".lean")
            path.write_text("".join(lines))
            command = ["taskset", "-c", args.cores, "/usr/bin/time", "-f",
                       "wall=%e user=%U sys=%S rss_kib=%M",
                       args.lean, "+leanprover/lean4:v4.34.1", str(path)]
            start = time.perf_counter()
            result = subprocess.run(command, capture_output=True, text=True)
            wall = time.perf_counter()-start
            path.with_suffix(".stdout").write_text(result.stdout)
            path.with_suffix(".stderr").write_text(result.stderr)
            runs.append(dict(case=case, skip_kernel_tc=skip, command=command,
                             source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
                             returncode=result.returncode, wall_s=wall))
            (out/"runs.json").write_text(json.dumps(runs,indent=1)+"\n")
            print(case, "skip="+str(skip), result.returncode, round(wall,3), flush=True)
            if result.returncode:
                raise RuntimeError(f"profile failed; inspect {path.with_suffix('.stderr')}")


if __name__ == "__main__":
    main()
