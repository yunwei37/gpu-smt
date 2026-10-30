"""Qualify the pinned image and expose cold-load cost separately from batching."""
import atexit
import json
import os
import subprocess
import sys
import time
from urllib.request import urlopen

from proofserve import Client

if "--self-test" in sys.argv:
    env = os.environ.copy()
    env["RUST_LOG"] = "proofserve_engine::resources=info,proofserve_lean::prepared=info"
    server = subprocess.Popen(
        ["/bin/sh", "/usr/local/bin/start-proofserve", "serve",
         "--listen", "127.0.0.1:3000", "--memory-gib", "3"],
        env=env,
    )

    def retire():
        if server.poll() is None:
            server.terminate()
        try:
            server.wait(timeout=30)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()

    atexit.register(retire)
    url = "http://localhost:3000"
else:
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"

for attempt in range(60):
    try:
        with urlopen(url + "/health", timeout=2) as response:
            assert json.load(response)["status"] == "ok"
        break
    except OSError:
        time.sleep(1)
else:
    raise RuntimeError("container service did not become healthy")

client = Client(url, request_timeout=240)
observations = []


def check(phase, snippets, timeout):
    started = time.monotonic()
    result = client.check(snippets, timeout=timeout, reuse=False)
    observations.append({
        "phase": phase,
        "request_budget_seconds": timeout,
        "wall_seconds": time.monotonic() - started,
        "result": result,
    })
    print(json.dumps(observations[-1]), flush=True)
    assert [r["id"] for r in result["results"]] == [s["id"] for s in snippets], result
    return result["results"]


cold = check("first_mathlib", [{
    "id": "cold",
    "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num",
}], 180)
repeat = check("repeat_mathlib_different_source", [{
    "id": "repeat",
    "code": "import Mathlib\nexample : (2 : Nat) + 3 = 5 := by norm_num",
}], 180)
batch = check("small_native_batch", [
    {"id": "accepted", "code": "example : (2 : Nat) + 2 = 4 := by rfl"},
    {"id": "rejected", "code": "example : False := by decide"},
    {"id": "incomplete", "code": "example : False := by sorry"},
], 30)

rows = cold + repeat + batch
assert all(r["error"] is None and isinstance(r["response"], dict) for r in rows), observations
for row in cold + repeat + batch[:1]:
    native = row["response"]
    assert not any(m.get("severity") == "error" for m in native.get("messages", [])), row
    assert not native.get("sorries"), row
assert any(m.get("severity") == "error" for m in batch[1]["response"].get("messages", [])), batch[1]
assert batch[2]["response"].get("sorries"), batch[2]
print(json.dumps({"qualification": "passed", "observations": observations}), flush=True)
