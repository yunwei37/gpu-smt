#!/usr/bin/env python3
"""Capture ordinary pinned Lean module CLI runs and stock --profile controls.

No native checking options are changed except enabling the stock profiler at its
default 100ms display threshold. CPU0/-j1/LEAN_NUM_THREADS=1 are fixed. GNU time
CPU/maxRSS and whole-invocation driver wall are separate raw quantities.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

MODULES = ["Mathlib/" + name for name in (
    "Algebra/Group/Basic.lean", "Algebra/Polynomial/Basic.lean",
    "Data/Nat/Prime.lean", "LinearAlgebra/FiniteDimensional.lean",
    "Analysis/SpecialFunctions/Trigonometric/Basic.lean",
    "MeasureTheory/Integral/IntervalIntegral.lean")]


def identity(path):
    data = Path(path).read_bytes()
    return dict(path=str(Path(path).absolute()), resolved=str(Path(path).resolve()),
                bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def save(path, data):
    with open(path, "xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def load_snapshot():
    return dict(loadavg=Path("/proc/loadavg").read_text().strip(),
                wall_ns=time.time_ns(), monotonic_ns=time.monotonic_ns())


def child_affinity():
    os.sched_setaffinity(0, {0})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--lake", required=True)
    parser.add_argument("--lean", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--preflight", action="store_true", help="first real module, once per path")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("repeats must be positive")
    workspace = args.workspace.resolve(strict=True)
    lake, lean = shutil.which(args.lake), shutil.which(args.lean)
    if not lake or not lean:
        parser.error("lake and lean must be executable")
    lake, lean = os.path.abspath(lake), os.path.abspath(lean)
    time_binary = Path("/usr/bin/time")
    if not os.access(time_binary, os.X_OK):
        parser.error("stock /usr/bin/time is required")
    if 0 not in os.sched_getaffinity(0):
        parser.error("fixed CPU0 is unavailable in this process affinity; no CPU substitution is permitted")
    source_ids = {module: identity(workspace / module) for module in MODULES}
    environment = dict(os.environ)
    environment.update(LEAN_NUM_THREADS="1", LC_ALL="C",
                       PATH=str(Path(lean).parent) + os.pathsep + os.defpath,
                       XDG_CACHE_HOME=os.path.abspath(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache"))))
    selected = MODULES[:1] if args.preflight else MODULES
    cells = [(rep, module, mode) for rep in range(1, (1 if args.preflight else args.repeats) + 1)
             for module in selected
             for mode in (("normal", "profile") if rep % 2 else ("profile", "normal"))]
    args.out.mkdir(parents=True, exist_ok=False)
    for module in MODULES:
        target = args.out / "sources" / module
        target.parent.mkdir(parents=True, exist_ok=True)
        save(target, (workspace / module).read_bytes())
    signals = []
    previous = {}
    for number in (signal.SIGINT, signal.SIGTERM):
        def receive(signum, _frame):
            signals.append(dict(signal=signum, wall_ns=time.time_ns(), monotonic_ns=time.monotonic_ns()))
        previous[number] = signal.signal(number, receive)
    terminal_indices = []
    with open(args.out / "events.jsonl", "x", encoding="utf-8") as events:
        sequence = 0

        def event(kind, **fields):
            nonlocal sequence
            events.write(json.dumps(dict(event=kind, sequence=sequence, wall_ns=time.time_ns(),
                                         monotonic_ns=time.monotonic_ns(), **fields)) + "\n")
            sequence += 1
            events.flush()
            os.fsync(events.fileno())

        provenance_paths = [Path(__file__), Path(lake), Path(lean), time_binary,
                            workspace / "lean-toolchain", workspace / "lake-manifest.json",
                            workspace / "lakefile.lean"]
        event("run", cwd=str(workspace), preflight=args.preflight, repeats=1 if args.preflight else args.repeats,
              cells=[dict(index=i, repeat=r, module=m, mode=v) for i, (r, m, v) in enumerate(cells)],
              sources=source_ids, provenance=[identity(p) for p in provenance_paths if p.is_file()],
              environment={k: environment.get(k) for k in ("PATH", "XDG_CACHE_HOME", "LEAN_NUM_THREADS",
                          "LC_ALL", "LEAN_PATH", "LEAN_SYSROOT", "ELAN_HOME", "ELAN_TOOLCHAIN")},
              affinity=[0], parent_affinity=sorted(os.sched_getaffinity(0)), python=sys.version,
              profile_threshold="stock default100ms; short scopes still accumulate",
              checking="ordinary default trust; no checking disable; no output emission flags",
              timing_scope="whole time+lake+lean invocation; no kernel-stage partition")
        try:
            for index, (repeat, module, mode) in enumerate(cells):
                if signals:
                    event("not_launched", index=index, repeat=repeat, module=module, mode=mode,
                          reason="supervisor_signal")
                    continue
                folder = args.out / f"cell-{index:03d}"
                folder.mkdir()
                native = [lake, "env", lean, "-j1", "--json"]
                if mode == "profile":
                    native.append("--profile")
                native.append(module)
                command = [str(time_binary), "-v", "-o", str((folder / "time.txt").absolute()), *native]
                before = load_snapshot()
                event("launch_intent", index=index, repeat=repeat, module=module, mode=mode,
                      command=command, native_command=native, source=source_ids[module], load=before)
                proc = None
                error = None
                status = "launch_error"
                begin = time.monotonic_ns()
                end = None
                try:
                    with open(folder / "stdout.bin", "xb", buffering=0) as stdout, \
                         open(folder / "stderr.bin", "xb", buffering=0) as stderr:
                        proc = subprocess.Popen(command, cwd=workspace, env=environment,
                                                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                                start_new_session=True, preexec_fn=child_affinity)
                        event("launched", index=index, pid=proc.pid, pgid=proc.pid, affinity=[0])
                        status = "exited"
                        while proc.poll() is None:
                            if signals:
                                status = "interrupted"
                                os.killpg(proc.pid, signal.SIGTERM)
                                try:
                                    proc.wait(timeout=2)
                                except subprocess.TimeoutExpired:
                                    os.killpg(proc.pid, signal.SIGKILL)
                                break
                            time.sleep(.02)
                        proc.wait()
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        end = time.monotonic_ns()
                        for stream in (stdout, stderr):
                            os.fsync(stream.fileno())
                except Exception:
                    error = traceback.format_exc()
                    if proc:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        proc.wait()
                    end = time.monotonic_ns()
                result = dict(index=index, repeat=repeat, module=module, mode=mode, status=status,
                              command=command, native_command=native, returncode=proc.returncode if proc else None,
                              invocation_wall_ns=end - begin if end else None, begin_ns=begin, end_ns=end,
                              error=error, load_before=before, load_after=load_snapshot(),
                              source=source_ids[module], source_after=identity(workspace / module),
                              files={name: identity(folder / name) for name in ("stdout.bin", "stderr.bin", "time.txt")
                                     if (folder / name).is_file()})
                save(folder / "result.json", json.dumps(result, indent=2).encode())
                event("result", **result)
                terminal_indices.append(index)
        except BaseException:
            event("supervisor_error", error=traceback.format_exc())
            raise
        finally:
            event("shutdown", signals=signals, terminal_indices=terminal_indices,
                  missing_indices=sorted(set(range(len(cells))) - set(terminal_indices)))
            for number, handler in previous.items():
                signal.signal(number, handler)
    return 128 + signals[0]["signal"] if signals else 0


if __name__ == "__main__":
    sys.exit(main())
