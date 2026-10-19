"""Finite benchmark-only live-worker accounting and resource attribution."""
import asyncio
import json
import os
from pathlib import Path
import time
import psutil

DIRECTORY = os.environ.get("GPU_SMT_MEMORY_DIRECTORY")
_slots = None

async def acquire(repl):
    global _slots
    if not DIRECTORY:
        return
    if _slots is None:
        _slots = asyncio.Semaphore(int(os.environ["LEAN_SERVER_MAX_REPLS"]))
    await _slots.acquire()
    repl._budget_slot = True

def release(repl):
    if getattr(repl, "_budget_slot", False):
        repl._budget_slot = False
        _slots.release()

def activity(repl, snippet_id, phase):
    if not DIRECTORY or repl.proc is None:
        return
    path = Path(DIRECTORY) / "activity" / (str(repl.proc.pid) + ".json")
    path.parent.mkdir(exist_ok=True)
    try:
        birth = psutil.Process(repl.proc.pid).create_time()
    except psutil.NoSuchProcess:
        birth = getattr(repl, "_budget_birth", None)
    if birth is None:
        return
    repl._budget_birth = birth
    source_id = snippet_id.removesuffix("-header") if snippet_id else None
    data = dict(pid=repl.proc.pid, birth=birth, snippet_id=snippet_id,
                source_id=source_id, phase=phase, time_ns=time.monotonic_ns())
    temporary = path.with_suffix(".new")
    temporary.write_text(json.dumps(data))
    temporary.replace(path)

async def capture_exit(repl):
    if not DIRECTORY or repl.proc is None:
        return
    await repl.proc.wait()
    stderr = await repl.proc.stderr.read() if repl.proc.stderr else b""
    repl._budget_exit_stderr = stderr.decode(errors="replace")
    path = Path(DIRECTORY) / "process-exits.jsonl"
    with path.open("a") as stream:
        stream.write(json.dumps(dict(pid=repl.proc.pid,
            birth=getattr(repl, "_budget_birth", None),
            returncode=repl.proc.returncode, stderr=repl._budget_exit_stderr)) + "\n")

def resource_error(repl):
    if not DIRECTORY or repl.proc is None:
        return None
    path = Path(DIRECTORY) / "kills" / (str(repl.proc.pid) + ".json")
    if path.exists():
        row = json.loads(path.read_text())
        if row["owner_birth"] == getattr(repl, "_budget_birth", None):
            return "aggregate RSS watchdog: " + json.dumps(row, separators=(",", ":"))
    text = getattr(repl, "_budget_exit_stderr", "")
    markers = ["out of memory", "std::bad_alloc", "cannot allocate memory",
               "memory allocation failed", "failed to allocate", "virtual memory exhausted"]
    if any(marker in text.lower() for marker in markers):
        return "native allocation failure under configured address-space limit: " + text
    return None
