"""Finite serial native measurement,48GiB owned RSS/no AS/CPU8–11.

Keeps a warm native frontend inside each segment. On300s timeout or RSS
preemption,reap it before proceeding. Resource-preempted candidates retry alone
after the frontier,once;unresolved operational outcomes are never tactic failures.
No cache/policy/production engine behavior is enabled.
"""
import argparse
import collections
import gzip
import json
import os
from pathlib import Path
import resource
import selectors
import signal
import subprocess
import time
import traceback

RUN_OUTPUT = None

import psutil

BUDGET = 48 * 1024**3


def main():
    global RUN_OUTPUT
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--input", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--context", type=Path, required=True)
    a.add_argument("--module-dir", type=Path, required=True)
    args = a.parse_args()
    assert resource.getrlimit(resource.RLIMIT_AS) == (-1, -1)
    # The owning thread verifies the previous collection's actual retirement
    # before launch and records it in the experiment;no stale PID catalog here.
    os.sched_setaffinity(0, {8, 9, 10, 11})
    args.out.mkdir(exist_ok=False)
    RUN_OUTPUT = args.out
    definition = json.loads(args.context.read_text())
    project = Path(definition["cwd"])
    env = dict(os.environ, **definition["native_environment_overrides"])
    paths = [str(Path(x) if Path(x).is_absolute() else (project/x).resolve())
             for x in env["LEAN_PATH"].split(":")]
    env["LEAN_PATH"] = str(args.module_dir) + ":" + ":".join(paths)
    sdk = env["LEAN_SYSROOT"]
    env["PATH"] = sdk + "/bin:" + env["PATH"]
    for k in list(env):
        if k.startswith("GPU_ARITHMETIC_") or k in [
                "GPU_SMT_CEX_MODE", "GPU_SMT_ORACLE_SOCKET",
                "GPU_SMT_LINARITH_SOCKET", "GPU_SMT_CANDIDATE_TIMING"]:
            env.pop(k, None)
    rows = json.loads(gzip.decompress(args.input.read_bytes()))["candidates"]
    identities = [(x["id"], x["mode"]) for x in rows]
    assert len(identities) == len(set(identities))
    pending = list(rows)
    retry = []
    results = []
    root = psutil.Process()
    started = time.monotonic()
    memory = gzip.open(args.out/"memory.jsonl.gz", "wt")
    ledger = (args.out/"results.jsonl").open("w")
    events = (args.out/"lifecycle.jsonl").open("w")
    peak = 0
    number = 0

    def record(f, value):
        f.write(json.dumps(value, ensure_ascii=False)+"\n")
        f.flush()

    def sample():
        nonlocal peak
        processes = []
        for q in [root] + root.children(recursive=True):
            try:
                processes.append(dict(pid=q.pid, birth=q.create_time(),
                                      rss=q.memory_info().rss))
            except psutil.NoSuchProcess:
                pass
        total = sum(q["rss"] for q in processes)
        peak = max(peak, total)
        record(memory, dict(seconds=time.monotonic()-started, rss=total,
                            processes=processes))
        return total

    def segment(batch, exclusive):
        nonlocal number
        index = number
        number += 1
        segment = args.out/f"segment-{index:04d}"
        segment.mkdir()
        (segment/"input.json").write_text(json.dumps(batch, ensure_ascii=False))
        command = [sdk+"/bin/lean", "--load-dynlib="+str(args.module_dir/"libStateReuseProfile.so"), "--run",
                   str(Path(__file__).with_name("StateReuseMeasure.lean")),
                   str(segment/"input.json"), "ack"]
        current = None
        current_start = None
        finished = set()
        operational = None
        operational_current = None
        next_request = 0
        buffer = b""

        def admit(proc):
            nonlocal current, current_start, next_request, operational, operational_current
            if next_request >= len(batch):
                return
            if sample() > BUDGET:
                if finished:
                    operational = "idle_cache_resource_recycle"
                else:
                    row = batch[next_request]
                    next_request += 1
                    current = (row["id"], row["mode"])
                    operational_current = current
                    current_start = time.monotonic()
                    operational = "resource_preempted"
                os.killpg(proc.pid, signal.SIGKILL)
                return
            row = batch[next_request]
            next_request += 1
            current = (row["id"], row["mode"])
            # Starts before admission ACK;includes native dispatch/import work.
            current_start = time.monotonic()
            proc.stdin.write(b"next\n")
            proc.stdin.flush()

        def parse(line):
            nonlocal current, current_start, operational, operational_current
            try:
                value = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                return  # observer records/unstructured diagnostics remain raw
            if value.get("event") == "candidate_begin":
                assert current == (value["id"], value["mode"])
            elif value.get("event") == "candidate_end":
                assert current == (value["id"], value["mode"])
                elapsed = time.monotonic()-current_start
                if elapsed >= 300 or operational is not None:
                    operational = operational or "timeout"
                    operational_current = operational_current or current
                    value["event"] = "late_candidate_end"
                else:
                    finished.add(current)
                value.update(segment=index, exclusive_retry=exclusive,
                             transport_wall_seconds=elapsed)
                results.append(value)
                record(ledger, value)
                current = current_start = None
                if operational is None:
                    admit(proc)
                else:
                    os.killpg(proc.pid, signal.SIGKILL)

        with (segment/"raw.log").open("wb") as raw:
            proc = subprocess.Popen(command, env=env, cwd=project,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                start_new_session=True)
            identity = psutil.Process(proc.pid).create_time()
            record(events, dict(event="launch", segment=index, pid=proc.pid,
                                birth=identity, exclusive_retry=exclusive,
                                command=command, sources=len(batch)))
            sel = selectors.DefaultSelector()
            sel.register(proc.stdout, selectors.EVENT_READ)
            next_sample = 0
            try:
                admit(proc)
                eof = False
                while not eof:
                    now = time.monotonic()
                    # Retain the unreaped leader until owned group retirement.
                    # This also closes descendant-held output pipes on exit.
                    exited = os.waitid(os.P_PID, proc.pid,
                        os.WEXITED | os.WNOWAIT | os.WNOHANG) is not None
                    if exited:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    if now >= next_sample:
                        total = sample()
                        next_sample = now + 1
                        if total > BUDGET and not exited:
                            operational = "resource_preempted"
                            operational_current = current
                            # The sole native frontend is the largest owned Lean
                            # process. Never signal another Workspace or root.
                            owned = psutil.Process(proc.pid)
                            victims = [owned] + owned.children(recursive=True)
                            victim = max(victims, key=lambda q: q.memory_info().rss)
                            record(events, dict(event="watchdog_kill", segment=index,
                                pid=victim.pid, birth=victim.create_time(),
                                current=current, rss=total, budget=BUDGET))
                            victim.kill()
                    if current_start and now-current_start >= 300 and not exited:
                        operational = operational or "timeout"
                        operational_current = operational_current or current
                        os.killpg(proc.pid, signal.SIGKILL)
                    now = time.monotonic()
                    wait = min(1, next_sample-now)
                    if current_start is not None:
                        wait = min(wait, current_start+300-now)
                    for _, _ in sel.select(max(0, wait)):
                        data = os.read(proc.stdout.fileno(), 65536)
                        if not data:
                            eof = True
                            break
                        raw.write(data)
                        raw.flush()
                        buffer += data
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            parse(line)
                if buffer:
                    parse(buffer)
            finally:
                sel.close()
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                rc = proc.wait()
                proc.stdout.close()
                proc.stdin.close()
            record(events, dict(event="retired", segment=index, pid=proc.pid,
                                birth=identity, exit=rc, current=current,
                                operational=operational))
        if operational and operational_current:
            row = next(x for x in batch if (x["id"], x["mode"]) == operational_current)
            value = dict(event="operational_end", id=operational_current[0], mode=operational_current[1],
                         segment=index, exclusive_retry=exclusive,
                         status=operational, replay_qualified=False)
            record(ledger, value)
            results.append(value)
            finished.add(operational_current)
            if operational == "resource_preempted" and not exclusive:
                retry.append(row)
        elif operational == "idle_cache_resource_recycle":
            record(events, dict(event=operational, segment=index,
                                scope="No active candidate;retire cache then continue remaining sources"))
        elif rc != 0 or current:
            raise RuntimeError(f"Preserve failed native segment{index}:exit{rc},current{current}")
        return [x for x in batch if (x["id"], x["mode"]) not in finished]

    try:
        while pending:
            pending = segment(pending, False)
        for row in retry:
            rest = segment([row], True)
            assert not rest
        terminal = dict(state="complete", planned=len(rows),
            native_end_rows=sum(x["event"] == "candidate_end" for x in results),
            operational_attempts=sum(x["event"] == "operational_end" for x in results),
            exclusive_retries=len(retry), segments=number,
            seconds=time.monotonic()-started, sampled_peak_RSS_bytes=peak,
            budget_bytes=BUDGET, watchdog_sampling_seconds=1, fixed_AS=False,
            cpu_eligibility=[8, 9, 10, 11], proof_result_reuse=False,
            complete_replay_qualification=False)
        (args.out/"terminal.json").write_text(json.dumps(terminal, indent=2)+"\n")
    finally:
        memory.close()
        ledger.close()
        events.close()


if __name__ == "__main__":
    error = None
    try:
        main()
    except BaseException:
        error = traceback.format_exc()
        raise
    finally:
        if RUN_OUTPUT is not None:
            (RUN_OUTPUT/"client-exit.json").write_text(json.dumps(
                dict(error=error, state="failed" if error else "returned"))+"\n")
