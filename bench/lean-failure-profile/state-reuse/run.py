"""Finite serial native measurement,selected owned RSS/no AS/CPU eligibility.

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
import shutil
import signal
import subprocess
import time
import traceback

RUN_OUTPUT = None


DEFAULT_BUDGET_GIB = 48


def resource_point(budget_gib, cpu_spec, allowed_cpus, host_memory_bytes):
    """Bind the declared diagnostic point to actual host/affinity observations."""
    budget = budget_gib * 1024**3
    if budget_gib <= 0 or budget > host_memory_bytes:
        raise ValueError("RSS budget must be positive and fit physical host RAM; "
                         "select a smaller budget with headroom for other work")
    try:
        cpus = set(allowed_cpus) if cpu_spec is None else {
            int(value) for value in cpu_spec.split(",")}
    except ValueError as error:
        raise ValueError("--cpus must contain comma-separated eligible CPU IDs") from error
    if not cpus or not cpus.issubset(allowed_cpus):
        raise ValueError("--cpus must be a nonempty subset of current CPU eligibility")
    return dict(budget_bytes=budget, cpu_eligibility=sorted(cpus),
                hardware_memory_bytes=host_memory_bytes)


def check_continuation_resources(history, point):
    """A previous point is not a same-hardware prefix without recorded evidence."""
    prior = [row for row in history if row.get("event") == "resource_point"]
    if not prior or any(any(row.get(key) != value for key, value in point.items())
                        for row in prior):
        raise ValueError("previous resource/hardware point differs or is unknown; "
                         "keep the old capture and start a separate fresh point")




def persistent_output(path, workspace=Path("/workspaces")):
    """Resolve capture output onto the existing Workspace volume before writes."""
    workspace, output = workspace.resolve(), path.resolve()
    if not workspace.is_mount() or not output.is_relative_to(workspace):
        raise ValueError("--out must be on the existing /workspaces PVC; "
                         "container /tmp is disposable")
    existing = output
    while not existing.exists():
        existing = existing.parent
    if existing.stat().st_dev != workspace.stat().st_dev:
        raise ValueError("--out is on a different filesystem from the /workspaces PVC")
    return output


def native_exit_kind(current, source_started, operational):
    """Only an actually begun source can own an otherwise unexplained exit."""
    if operational is None and current is not None and source_started:
        return "native_process_failure"
    return operational


def continuation_plan(rows, history, retired):
    """Restore finite pending cells/retries;never reinterpret native failures."""
    by_id = {(r["id"], r["mode"]): r for r in rows}
    if len(by_id) != len(rows):
        raise ValueError("duplicate original candidate identities")
    completed, recorded, derived = {}, set(), []
    for row in history:
        if row["event"] not in ("candidate_end", "operational_end"):
            continue
        key = (row["id"], row["mode"])
        if key not in by_id:
            raise ValueError("prior result outside original input")
        recorded.add((row["segment"], key))
        completed[key] = row
    for old in retired:
        current = old.get("current")
        if not current or old.get("operational") or (old["segment"], tuple(current)) in recorded:
            continue
        key = tuple(current)
        if key not in by_id or not old.get("source_started"):
            raise ValueError("unreported exit has no matching admitted-source evidence")
        row = dict(event="operational_end", id=key[0], mode=key[1],
                   segment=old["segment"], exclusive_retry=old.get("exclusive_retry", False),
                   status="native_process_failure", native_exit_code=old["exit"],
                   transport_wall_seconds=None, derived_from_prior_retirement=True,
                   replay_qualified=False)
        derived.append(row)
        completed[key] = row
    pending = [r for r in rows if (r["id"], r["mode"]) not in completed]
    retry = [by_id[key] for key, row in completed.items()
             if row["event"] == "operational_end" and row["status"] == "resource_preempted"
             and not row.get("exclusive_retry", False)]
    return pending, retry, derived


def main():
    global RUN_OUTPUT

    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument("--input", type=Path, required=True)
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--context", type=Path, required=True)
    a.add_argument("--module-dir", type=Path, required=True)
    a.add_argument("--resume-from", type=Path,
                   help="Actually retired prior run of this exact input/context;keep its raw prefix")
    a.add_argument("--rss-budget-gib", type=int, default=DEFAULT_BUDGET_GIB,
                   help="Aggregate owned-tree sampled RSS budget; choose host headroom explicitly")
    a.add_argument("--cpus", help="Eligible CPU IDs,comma-separated;default is current affinity")
    args = a.parse_args()
    try:
        args.out = persistent_output(args.out)
    except (OSError, ValueError) as error:
        a.error(str(error))
    import psutil

    started = time.monotonic()
    assert resource.getrlimit(resource.RLIMIT_AS) == (-1, -1)
    # The owning thread verifies the previous collection's actual retirement
    # before launch and records it in the experiment;no stale PID catalog here.
    try:
        point = resource_point(args.rss_budget_gib, args.cpus,
                               set(os.sched_getaffinity(0)), psutil.virtual_memory().total)
    except ValueError as error:
        a.error(str(error))
    point["host_boot_id"] = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    budget = point["budget_bytes"]
    os.sched_setaffinity(0, set(point["cpu_eligibility"]))
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
    pending, retry, results, derived = list(rows), [], [], []
    root = psutil.Process()
    peak, number, phase = 0, 0, 0
    if args.resume_from:
        previous = args.resume_from
        previous_exit = json.loads((previous/"client-exit.json").read_text())
        if previous_exit.get("error") is None or (previous/"terminal.json").exists():
            raise ValueError("continuation requires an incomplete failed prior run")
        if json.loads(gzip.decompress((previous.parent/"input.json.gz").read_bytes()))["candidates"] != rows:
            raise ValueError("continuation input differs")
        if json.loads((previous.parent/"native-context.json").read_text()) != definition:
            raise ValueError("continuation native context differs")
        history = [json.loads(line) for line in (previous/"results.jsonl").read_text().splitlines()]
        lifecycle = [json.loads(line) for line in (previous/"lifecycle.jsonl").read_text().splitlines()]
        check_continuation_resources(lifecycle, point)
        prior_launch_path = previous.parent/"launch.json"
        if prior_launch_path.exists():
            prior_launch = json.loads(prior_launch_path.read_text())
            stat = Path("/proc")/str(prior_launch["pid"])/"stat"
            if stat.exists() and int(stat.read_text().rsplit(")", 1)[1].split()[19]) == prior_launch["start_ticks"]:
                raise ValueError("prior controller still lives")
        for launch in (r for r in lifecycle if r["event"] == "launch"):
            try:
                if psutil.Process(launch["pid"]).create_time() == launch["birth"]:
                    raise ValueError("prior owned native process still lives")
            except psutil.NoSuchProcess:
                pass
        retired = []
        for old in (r for r in lifecycle if r["event"] == "retired"):
            if old.get("current") and old.get("operational") is None:
                key = tuple(old["current"])
                raw = previous/("segment-%04d" % old["segment"])/"raw.log"
                began = False
                for line in raw.read_text().splitlines():
                    try:
                        value = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(value, dict) and value.get("event") == "candidate_begin":
                        if (value["id"], value["mode"]) == key:
                            began = True
                old = dict(old, source_started=began)
            retired.append(old)
        pending, retry, derived = continuation_plan(rows, history, retired)
        for directory in sorted(previous.glob("segment-*")):
            shutil.copytree(directory, args.out/directory.name)
        for name in ["results.jsonl", "lifecycle.jsonl", "memory.jsonl.gz"]:
            shutil.copyfile(previous/name, args.out/name)
        number = max((r["segment"] for r in lifecycle if r["event"] == "launch"), default=-1) + 1
        with gzip.open(previous/"memory.jsonl.gz", "rt") as samples:
            for line in samples:
                value = json.loads(line)
                peak = max(peak, value["rss"])
                phase = max(phase, value.get("phase", 0)+1)
        results = history + derived
        (args.out/"continuation.json").write_text(json.dumps(dict(
            previous_run=str(previous), previous_client_exit=previous_exit,
            prior_result_rows=len(history), derived_prior_attempts=derived,
            pending_first_attempts=len(pending), deferred_exclusive_retries=len(retry),
            phase=phase, input_and_context_equal=True,
            clock_scope="New phase starts a new seconds axis;prior gaps are not a fresh uninterrupted clock."
        ), indent=2)+"\n")
    memory = gzip.open(args.out/"memory.jsonl.gz", "at" if args.resume_from else "wt")
    ledger = (args.out/"results.jsonl").open("a" if args.resume_from else "w")
    events = (args.out/"lifecycle.jsonl").open("a" if args.resume_from else "w")

    def record(f, value):
        f.write(json.dumps(value, ensure_ascii=False)+"\n")
        f.flush()

    record(events, dict(event="resource_point", **point))

    for value in derived:
        record(ledger, value)

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
        record(memory, dict(seconds=time.monotonic()-started, phase=phase, rss=total,
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
        source_started = False
        operational_start = None
        finished = set()
        operational = None
        operational_current = None
        next_request = 0
        buffer = b""

        def admit(proc):
            nonlocal current, current_start, next_request, operational, operational_current, source_started
            if next_request >= len(batch):
                return
            if sample() > budget:
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
            source_started = False
            # Starts before admission ACK;includes native dispatch/import work.
            current_start = time.monotonic()
            proc.stdin.write(b"next\n")
            proc.stdin.flush()

        def parse(line):
            nonlocal current, current_start, operational, operational_current, source_started, operational_start
            try:
                value = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                return  # observer records/unstructured diagnostics remain raw
            if value.get("event") == "candidate_begin":
                assert current == (value["id"], value["mode"])
                source_started = True
            elif value.get("event") == "candidate_end":
                assert current == (value["id"], value["mode"])
                elapsed = time.monotonic()-current_start
                if elapsed >= 300 or operational is not None:
                    operational = operational or "timeout"
                    operational_current = operational_current or current
                    operational_start = current_start
                    value["event"] = "late_candidate_end"
                else:
                    finished.add(current)
                value.update(segment=index, exclusive_retry=exclusive,
                             transport_wall_seconds=elapsed)
                results.append(value)
                record(ledger, value)
                current = current_start = None
                source_started = False
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
                        if total > budget and not exited:
                            operational = "resource_preempted"
                            operational_current = current
                            # The sole native frontend is the largest owned Lean
                            # process. Never signal another Workspace or root.
                            owned = psutil.Process(proc.pid)
                            victims = [owned] + owned.children(recursive=True)
                            victim = max(victims, key=lambda q: q.memory_info().rss)
                            record(events, dict(event="watchdog_kill", segment=index,
                                pid=victim.pid, birth=victim.create_time(),
                                current=current, rss=total, budget=budget))
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
            operational = native_exit_kind(current, source_started, operational)
            if operational == "native_process_failure":
                operational_current = current
            record(events, dict(event="retired", segment=index, pid=proc.pid,
                                birth=identity, exit=rc, current=current,
                                source_started=source_started, exclusive_retry=exclusive,
                                operational=operational))
        if operational and operational_current:
            row = next(x for x in batch if (x["id"], x["mode"]) == operational_current)
            value = dict(event="operational_end", id=operational_current[0], mode=operational_current[1],
                         segment=index, exclusive_retry=exclusive,
                         status=operational, native_exit_code=rc,
                         transport_wall_seconds=(time.monotonic()-(operational_start or current_start)
                            if operational_start is not None or current_start is not None else None),
                         replay_qualified=False)
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
            exclusive_retries=sum(x.get("exclusive_retry", False) for x in results
                                  if x["event"] in ("candidate_end", "operational_end")),
            exclusive_retries_this_phase=len(retry), segments=number,
            seconds=time.monotonic()-started, sampled_peak_RSS_bytes=peak,
            **point, watchdog_sampling_seconds=1, fixed_AS=False,
            proof_result_reuse=False,
            complete_replay_qualification=False, continuation_phase=phase,
            seconds_scope="Current controller phase only;prior gaps are not included" if phase else "Single controller phase")
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
