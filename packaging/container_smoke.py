"""Exercise the built image's real Lean/Mathlib /check endpoint."""
import json
import sys
import subprocess
import atexit
import time
from urllib.request import urlopen
from proofserve import Client

if "--self-test" in sys.argv:
    server = subprocess.Popen(["/bin/sh", "/usr/local/bin/start-proofserve",
                               "serve", "--listen", "127.0.0.1:3000"])
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
        with urlopen(url + "/health", timeout=2) as r:
            assert json.load(r)["status"] == "ok"
        break
    except OSError:
        time.sleep(1)
else:
    raise RuntimeError("container service did not become healthy")
result = Client(url, request_timeout=180).check([
    {"id": "accepted", "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num"},
    {"id": "rejected", "code": "example : False := by decide"},
    {"id": "incomplete", "code": "example : False := by sorry"},
], timeout=60, reuse=False)
assert [r["id"] for r in result["results"]] == ["accepted", "rejected", "incomplete"], result
assert all(r["error"] is None for r in result["results"]), result
good, bad, incomplete = [r["response"] for r in result["results"]]
assert not any(m.get("severity") == "error" for m in good.get("messages", [])), good
assert not good.get("sorries"), good
assert any(m.get("severity") == "error" for m in bad.get("messages", [])), bad
assert incomplete.get("sorries"), incomplete
print(json.dumps(result, indent=2))
