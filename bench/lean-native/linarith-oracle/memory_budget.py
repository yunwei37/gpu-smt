"""One-second RSS watchdog for only the finite capture's owned process tree."""
import json
import os
from pathlib import Path
import signal
import threading
import time
import traceback
import psutil

class MemoryWatchdog:
    def __init__(self, root_pid, budget_bytes, threshold_bytes, max_repls, repl_path, out):
        current = psutil.Process()
        assert root_pid in [current.pid] + [p.pid for p in current.parents()]
        self.root = psutil.Process(root_pid)
        self.birth = self.root.create_time()
        self.known = {self.root.pid: self.birth}
        self.budget = budget_bytes
        self.threshold = threshold_bytes
        self.max_repls = max_repls
        self.repl_name = Path(repl_path).name
        self.out = Path(out)
        (self.out / "kills").mkdir()
        (self.out / "activity").mkdir()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, name="capture-rss-watchdog", daemon=True)
        self.samples = self.kills = self.peak_rss = self.peak_repls = 0
        self.error = None
        self.on_error = None
        self.extra_memory = None
        self.peak_extra_rss = 0

    def start(self):
        self.thread.start()

    def owned(self):
        try:
            if self.root.create_time() == self.birth:
                for proc in [self.root] + self.root.children(recursive=True):
                    self.known[proc.pid] = proc.create_time()
        except psutil.NoSuchProcess:
            pass
        result = []
        for pid, birth in list(self.known.items()):
            try:
                proc = psutil.Process(pid)
                if proc.create_time() != birth or proc.status() == psutil.STATUS_ZOMBIE:
                    continue
                result.append(proc)
            except psutil.NoSuchProcess:
                continue
        return result

    def sample(self, stream):
        processes = []
        for proc in self.owned():
            try:
                cmd = proc.cmdline()
                processes.append(dict(pid=proc.pid, birth=proc.create_time(), ppid=proc.ppid(),
                    rss=proc.memory_info().rss, command=cmd,
                    native_repl=bool(cmd and Path(cmd[0]).name == self.repl_name)))
            except psutil.NoSuchProcess:
                continue
        extra = self.extra_memory() if self.extra_memory is not None else None
        extra_rss = extra["rss_bytes"] if extra is not None else 0
        if not isinstance(extra_rss, int) or extra_rss < 0:
            raise RuntimeError("Invalid owned GPU provider RSS sample")
        self.peak_extra_rss = max(self.peak_extra_rss, extra_rss)
        total = sum(p["rss"] for p in processes) + extra_rss
        repls = [p for p in processes if p["native_repl"]]
        self.peak_rss = max(self.peak_rss, total)
        self.peak_repls = max(self.peak_repls, len(repls))
        row = dict(time_ns=time.monotonic_ns(), total_rss_bytes=total,
            budget_bytes=self.budget, effective_threshold_bytes=self.threshold,
            native_repl_count=len(repls), processes=processes,
            external_owned_provider=extra)
        # Actual limits are recorded from native processes, not inferred from configuration.
        for repl in repls:
            try:
                repl["address_limit"] = [line for line in Path("/proc", str(repl["pid"]), "limits").read_text().splitlines()
                                        if line.startswith("Max address space")]
            except FileNotFoundError:
                pass
        if total > self.threshold and not repls:
            raise RuntimeError("Owned aggregate exceeds budget with no live REPL victim")
        if total > self.threshold and repls:
            victim = max(repls, key=lambda p: p["rss"])
            try:
                proc = psutil.Process(victim["pid"])
                if proc.create_time() == victim["birth"]:
                    group = os.getpgid(proc.pid)
                    assert group in self.known and group != os.getpgrp()
                    owner = psutil.Process(group)
                    assert owner.create_time() == self.known[group]
                    activity_path = self.out / "activity" / (str(group) + ".json")
                    activity = json.loads(activity_path.read_text()) if activity_path.exists() else {}
                    notice = dict(owner_pid=group, owner_birth=owner.create_time(),
                        victim_pid=proc.pid, victim_birth=victim["birth"], victim_rss_bytes=victim["rss"],
                        total_rss_bytes=total, budget_bytes=self.budget,
                        effective_threshold_bytes=self.threshold,
                        source_id=activity.get("source_id"), snippet_id=activity.get("snippet_id"),
                        phase=activity.get("phase"), time_ns=time.monotonic_ns(),
                        reason="aggregate_rss_exceeded", largest_native_repl_selected=True)
                    path = self.out / "kills" / (str(group) + ".json")
                    temporary = path.with_suffix(".new")
                    temporary.write_text(json.dumps(notice))
                    temporary.replace(path)
                    os.killpg(group, signal.SIGKILL)
                    self.kills += 1
                    row["kill"] = notice
            except (psutil.NoSuchProcess, ProcessLookupError):
                row["selected_victim_exited_before_signal"] = victim["pid"]
        stream.write(json.dumps(row, separators=(",", ":")) + "\n")
        stream.flush()
        self.samples += 1

    def run(self):
        try:
            with (self.out / "memory-rss.jsonl").open("w") as stream:
                while not self.stop_event.is_set():
                    started = time.monotonic()
                    self.sample(stream)
                    self.stop_event.wait(max(0, 1 - (time.monotonic() - started)))
        except Exception:
            self.error = traceback.format_exc()
            try:
                (self.out / "memory-watchdog-error.txt").write_text(self.error)
            except OSError:
                # A full output volume can fail both the sample and its error record.
                # Keep the original failure in memory for the terminal record.
                pass
            finally:
                # Failure to record the error must not bypass stopping acquisition.
                if self.on_error is not None:
                    self.on_error()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def summary(self):
        return dict(root_pid=self.root.pid, root_birth=self.birth, budget_bytes=self.budget,
            effective_threshold_bytes=self.threshold, per_second=True,
            samples=self.samples, kills=self.kills, peak_sampled_owned_rss_bytes=self.peak_rss,
            peak_sampled_native_repl_count=self.peak_repls, error=self.error,
            peak_external_owned_provider_rss_bytes=self.peak_extra_rss,
            scope="Whole owned experiment tree RSS sum; sampled response, not a kernel RSS quota. Includes retained descendants after reparenting and optional source-owned GPU provider samples.")
