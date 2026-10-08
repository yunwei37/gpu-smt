#!/usr/bin/env python3
"""Bounded pinned-REPL logical-header-root control, with raw native capture.

Every matching candidate uses the original header env, never a prior candidate
env. This is an existing native mechanism, not a novelty or equivalence claim.
Timing includes native import/elaboration/check work without splitting stages.
The pinned native REPL prints response frames without flushing stdout; persistent
pipe transport requires stock stdbuf -oL for OS line-buffered stdout. Its launcher
overhead is included in the recorded complete clocks.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import select
import shutil
import signal
import subprocess
import sys
import time
import traceback

DEFAULT_HEADER = "import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    with open(path, "xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def file_info(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return dict(bytes=path.stat().st_size, sha256=h.hexdigest())


def wire(code, env=None):
    command = dict(cmd=code, allTactics=False, ast=False, tactics=False, premises=False)
    if env is not None:
        command["env"] = env
    return json.dumps(command, ensure_ascii=False).encode("utf-8") + b"\r\n\r\n"


class Session:
    def __init__(self, folder, command, workspace, timeout, event, interrupted):
        self.folder, self.timeout = folder, timeout
        self.event, self.interrupted = event, interrupted
        self.pending = b""
        self.proc = None
        self.closed = False
        folder.mkdir()
        self.stdout = open(folder / "stdout.bin", "xb", buffering=0)
        self.stderr = open(folder / "stderr.bin", "xb", buffering=0)
        self.begin = time.monotonic_ns()
        event("launch_intent", session=folder.name, command=command, cwd=str(workspace))
        try:
            self.proc = subprocess.Popen(command, cwd=workspace, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=self.stderr,
                                         start_new_session=True, bufsize=0)
            os.set_blocking(self.proc.stdin.fileno(), False)
            os.set_blocking(self.proc.stdout.fileno(), False)
            event("launched", session=folder.name, pid=self.proc.pid, pgid=self.proc.pid)
        except BaseException:
            self.close("launch_error")
            raise

    def read(self):
        data = os.read(self.proc.stdout.fileno(), 65536)
        if data:
            self.stdout.write(data)
            self.pending += data
        return data

    def close(self, reason):
        if self.closed:
            return
        self.closed = True
        if self.proc is not None:
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.proc.wait()
            # After killing the owned group, retain all currently available tail.
            while select.select([self.proc.stdout], [], [], 0)[0]:
                if not self.read():
                    break
            self.proc.stdin.close()
            self.proc.stdout.close()
        self.cleanup_end_ns = time.monotonic_ns()
        for stream in (self.stdout, self.stderr):
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
        self.event("replacement", session=self.folder.name, reason=reason,
                   returncode=self.proc.returncode if self.proc else None,
                   lifetime_ns=time.monotonic_ns() - self.begin,
                   unconsumed_stdout_bytes=len(self.pending),
                   files={name: file_info(self.folder / name)
                          for name in ("stdout.bin", "stderr.bin")})

    def call(self, folder, code, role, index=None, env=None, deadline=None):
        folder.mkdir()
        payload = wire(code, env)
        save(folder / "stdin.bin", payload)
        begin = time.monotonic_ns()
        deadline = deadline if deadline is not None else time.monotonic() + self.timeout
        response = None
        status = "transport_error"
        written = 0
        raw = b""
        start_offset = self.stdout.tell()
        stderr_start = (self.folder / "stderr.bin").stat().st_size
        self.event("submission", session=self.folder.name, role=role, source_index=index,
                   env=env, stdin_sha256=digest(payload), capture=str(folder))
        error = None
        invocation_end = None
        try:
            if self.interrupted():
                status = "interrupted"
                raise InterruptedError("supervisor signal before send")
            if time.monotonic() >= deadline:
                status = "timeout"
                raise TimeoutError("whole-job budget exhausted before send")
            if select.select([self.proc.stdout], [], [], 0)[0]:
                self.read()
            if self.pending:
                raise ValueError("unexpected stdout before submission; full bytes retained in session")
            while written < len(payload):
                if self.interrupted():
                    status = "interrupted"
                    raise InterruptedError("supervisor signal")
                if time.monotonic() >= deadline:
                    status = "timeout"
                    raise TimeoutError("stdin write timeout")
                if select.select([], [self.proc.stdin], [], .05)[1]:
                    try:
                        written += os.write(self.proc.stdin.fileno(), payload[written:])
                    except BlockingIOError:
                        continue
            self.event("sent", session=self.folder.name, role=role, source_index=index,
                       stdin_bytes_written=written)
            while True:
                # Native Main.repl prints JSON then a blank line. Do not skip banners.
                marker, width = self.pending.find(b"\n\n"), 2
                crlf = self.pending.find(b"\r\n\r\n")
                if crlf >= 0 and (marker < 0 or crlf < marker):
                    marker, width = crlf, 4
                if marker >= 0:
                    raw = self.pending[:marker + width]
                    self.pending = self.pending[marker + width:]
                    invocation_end = time.monotonic_ns()
                    response = json.loads(raw.decode("utf-8"))
                    if not isinstance(response, dict):
                        raise ValueError("native response is not a JSON object")
                    if self.pending:
                        raise ValueError("extra stdout after native response; full bytes retained")
                    status = "response"
                    break
                if self.interrupted():
                    status = "interrupted"
                    raise InterruptedError("supervisor signal")
                if time.monotonic() >= deadline:
                    status = "timeout"
                    raise TimeoutError("native response timeout")
                if select.select([self.proc.stdout], [], [], .05)[0] and not self.read():
                    raise EOFError("native stdout closed before complete response")
        except Exception:
            error = traceback.format_exc()
            self.close(status)
            invocation_end = self.cleanup_end_ns
        finally:
            if not self.closed:
                self.stdout.flush()
                os.fsync(self.stdout.fileno())
                os.fsync(self.stderr.fileno())
        # Persist a complete frame or the partial raw output; session stdout also
        # retains unexpected prefixes/tails. Invocation timing ends before this.
        save(folder / "response.bin", raw if raw else self.pending)
        stderr_end = (self.folder / "stderr.bin").stat().st_size
        with open(self.folder / "stderr.bin", "rb") as observed:
            observed.seek(stderr_start)
            save(folder / "stderr.observed.bin", observed.read(stderr_end - stderr_start))
        result = dict(session=self.folder.name, role=role, source_index=index,
                      status=status, error=error, env_requested=env,
                      stdin_bytes_written=written, elapsed_ns=time.monotonic_ns() - begin,
                      invocation_elapsed_ns=invocation_end - begin if invocation_end else None,
                      stdout_offset_start=start_offset,
                      stderr_offset_start=stderr_start,
                      stderr_offset_observed_end=stderr_end,
                      returncode=self.proc.poll(),
                      files={name: file_info(folder / name)
                             for name in ("stdin.bin", "response.bin", "stderr.observed.bin")})
        save(folder / "result.json", json.dumps(result, indent=2).encode())
        self.event("result", **result)
        return response if status == "response" else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codes", type=Path, required=True)
    parser.add_argument("--tasks", "--selected-tasks", dest="tasks", type=Path, required=True)
    parser.add_argument("--lake", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=300)
    parser.add_argument("--retire-after", type=int, default=256)
    args = parser.parse_args()
    if args.retire_after < 1 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("retire-after and timeout must be positive and finite")
    codes_bytes, tasks_bytes = args.codes.read_bytes(), args.tasks.read_bytes()
    codes, tasks = json.loads(codes_bytes), json.loads(tasks_bytes)
    if not isinstance(codes, list) or any(not isinstance(r, dict) or
            not isinstance(r.get("code"), str) for r in codes):
        parser.error("codes must be the original list of string-code objects")
    if not isinstance(tasks, list):
        parser.error("selected tasks must be a list")
    if not tasks or not codes or len(codes) % len(tasks):
        parser.error("codes must contain a positive fixed integer number of samples per ordered task")
    samples_per_task = len(codes) // len(tasks)
    task_names, headers = [], []
    for row in tasks:
        if not isinstance(row, dict):
            parser.error("selected task rows must be objects")
        name = row.get("problem_id", row.get("name"))
        header = row.get("header", DEFAULT_HEADER)
        if not isinstance(name, (str, int)) or not isinstance(header, str):
            parser.error("each task needs its original name and string header")
        task_names.append(name)
        headers.append(header)
    for index, row in enumerate(codes):
        if row.get("name") != task_names[index // samples_per_task]:
            parser.error(f"source index {index} name disagrees with ordered original task/sample group")
    found = shutil.which(args.lake)
    if not found:
        parser.error("lake is missing or not executable")
    stdbuf_found = shutil.which("stdbuf")
    if not stdbuf_found:
        parser.error("stock stdbuf is required for line-buffered persistent REPL stdout")
    lake = os.path.abspath(found)
    stdbuf = os.path.abspath(stdbuf_found)
    command = [stdbuf, "-oL", lake, "exe", "repl"]
    workspace = args.workspace.resolve(strict=True)
    args.out.mkdir(parents=True, exist_ok=False)
    save(args.out / "codes.original.json", codes_bytes)
    save(args.out / "tasks.original.json", tasks_bytes)
    signals = []
    old = {}

    def handle(number, _frame):
        signals.append(dict(signal=number, wall_ns=time.time_ns(), monotonic_ns=time.monotonic_ns()))

    for number in (signal.SIGTERM, signal.SIGINT):
        old[number] = signal.signal(number, handle)
    session = None
    generation = 0
    completed = []
    with open(args.out / "events.jsonl", "x", encoding="utf-8") as stream:
        sequence = 0

        def event(kind, **fields):
            nonlocal sequence
            stream.write(json.dumps(dict(event=kind, sequence=sequence, wall_ns=time.time_ns(),
                                         monotonic_ns=time.monotonic_ns(), **fields), ensure_ascii=False) + "\n")
            sequence += 1
            stream.flush()
            os.fsync(stream.fileno())

        def launch():
            nonlocal generation
            folder = args.out / f"session-{generation:08d}"
            generation += 1
            return Session(folder, command, workspace, args.timeout, event, lambda: bool(signals))

        paths = [Path(__file__), Path(stdbuf), Path(lake), workspace / "lean-toolchain",
                 workspace / "lake-manifest.json", workspace / ".lake/packages/REPL/REPL/Main.lean",
                 workspace / ".lake/packages/REPL/REPL/JSON.lean",
                 workspace / ".lake/packages/REPL/REPL/Frontend.lean",
                 workspace / ".lake/packages/REPL/.lake/build/bin/repl", workspace / ".lake/build/bin/repl"]
        event("run", command=command, cwd=str(workspace), timeout_seconds=args.timeout,
              retire_after=args.retire_after, count=len(codes), codes_sha256=digest(codes_bytes),
              task_count=len(tasks), samples_per_task=samples_per_task,
              duplicate_task_names=[dict(name=name, count=count) for name, count in Counter(task_names).items() if count > 1],
              tasks_sha256=digest(tasks_bytes), affinity=sorted(os.sched_getaffinity(0)),
              python=sys.version, provenance={str(p): file_info(p) for p in paths if p.is_file()},
              stdout_buffering=dict(utility=stdbuf, utility_sha256=file_info(Path(stdbuf))["sha256"],
                                    mode="line", argument="-oL", overhead="included in recorded complete clocks"),
              environment={k: os.environ.get(k) for k in
                           ("PATH", "LEAN_PATH", "LEAN_SYSROOT", "ELAN_HOME", "ELAN_TOOLCHAIN", "OMP_NUM_THREADS")},
              timing_scope="whole native calls plus captured setup/replacement; stages not separated",
              timeout_scope="one absolute per-candidate deadline before header lookup/launch/replacement; shared by setup/body/fallback; owned cleanup may extend it",
              lifecycle="one process; all observed original-header roots cached; retire count includes rootless fallbacks; entire cache reset",
              rootless_fallback="no env command in current bounded worker; fresh native environment, warm process",
              stderr_scope="full session raw bytes; per-response offsets are observation boundaries")
        for index in range(len(codes)):
            event("admitted", source_index=index, task_index=index // samples_per_task,
                  sample_index=index % samples_per_task)
        roots, used = {}, 0
        try:
            for index, row in enumerate(codes):
                if signals:
                    event("not_launched", source_index=index, reason="supervisor_signal")
                    continue
                job_begin_ns = time.monotonic_ns()
                deadline = job_begin_ns / 1e9 + args.timeout
                event("whole_job_begin", source_index=index, begin_ns=job_begin_ns,
                      deadline_ns=int(deadline * 1e9), timeout_seconds=args.timeout)
                try:
                    task_index, sample_index = divmod(index, samples_per_task)
                    header = headers[task_index]
                    ascii_header = header is not None and header.isascii()
                    match = ascii_header and row["code"].startswith(header)
                    folder = args.out / f"request-{index:08d}"
                    event("header_match", source_index=index, task_index=task_index, sample_index=sample_index,
                          header_sha256=digest(header.encode()) if header is not None else None,
                          header_ascii=ascii_header, exact_prefix=header is not None and row["code"].startswith(header))
                    if session and (session.closed or used >= args.retire_after):
                        session.close("retire_limit" if used >= args.retire_after else "failed_session")
                        session = None
                    if not session:
                        try:
                            session = launch()
                            roots, used = {}, 0
                        except Exception:
                            event("candidate_launch_error", source_index=index, error=traceback.format_exc())
                            continue
                    root_env = roots.get(header) if match else None
                    if match and root_env is None:
                        try:
                            setup = session.call(session.folder / f"setup-{len(roots):08d}", header, "header_setup", deadline=deadline)
                            if setup and type(setup.get("env")) is int and setup["env"] >= 0 and \
                                    not setup.get("sorries") and not setup.get("message") and not setup.get("error") and \
                                    not setup.get("messages"):
                                root_env = setup["env"]
                                roots[header] = root_env
                                event("root_cached", session=session.folder.name, header_sha256=digest(header.encode()),
                                      env=root_env, root_count=len(roots))
                            else:
                                session.close("unusable_header_setup")
                                session = None
                                event("fallback", source_index=index,
                                      reason="header_setup_diagnostics" if setup and setup.get("messages") else "unusable_header_setup")
                        except Exception:
                            event("setup_error", source_index=index, error=traceback.format_exc())
                            session.close("setup_exception")
                            session = None
                    if signals:
                        event("not_launched", source_index=index, reason="supervisor_signal_during_setup")
                        continue
                    if session is None:
                        try:
                            session = launch()
                            roots, used, root_env = {}, 0, None
                        except Exception:
                            event("candidate_launch_error", source_index=index, error=traceback.format_exc())
                            continue
                    if root_env is not None and match:
                        body = "".join(c if c in "\r\n" else " " for c in header) + row["code"][len(header):]
                        session.call(folder, body, "candidate_branch", index, root_env, deadline=deadline)
                    else:
                        event("fallback", source_index=index,
                              reason="non_ascii_header" if header is not None and not ascii_header else
                                     "header_mismatch_or_unknown" if not match else "header_setup_failed")
                        session.call(folder, row["code"], "candidate_fresh", index, deadline=deadline)
                    used += 1
                    completed.append(index)
                finally:
                    event("whole_job_end", source_index=index,
                          elapsed_ns=time.monotonic_ns() - job_begin_ns,
                          deadline_ns=int(deadline * 1e9),
                          nominal_budget_exceeded=time.monotonic() > deadline)
        except BaseException:
            event("supervisor_error", error=traceback.format_exc())
            raise
        finally:
            if session:
                session.close("shutdown")
            event("shutdown", signals=signals, result_indices=completed,
                  missing_result_indices=sorted(set(range(len(codes))) - set(completed)))
            for number, handler in old.items():
                signal.signal(number, handler)
    return 128 + signals[0]["signal"] if signals else 0


if __name__ == "__main__":
    sys.exit(main())
