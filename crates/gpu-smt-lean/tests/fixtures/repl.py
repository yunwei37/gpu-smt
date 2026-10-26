"""Protocol/process fixture, never presented as native Lean proof checking."""
import json, sys, time
code = json.loads(sys.stdin.readline())["cmd"]
if code.startswith("memory_"):
    retained = bytearray(16 * 1024 * 1024)
    time.sleep(2.2)
if code == "eof_flush":
    # Model a real REPL that buffers its reply until its next read reaches EOF.
    sys.stdin.read()
if code == "slow":
    time.sleep(60)
if code == "stderr":
    sys.stderr.write("diagnostic " * 10000)
    sys.stderr.flush()
if code == "bad":
    payload = {"env": 0, "messages": [{"severity": "error", "data": "fixture rejection"}]}
elif code == "sorry":
    payload = {"env": 0, "messages": [], "sorries": [{}]}
else:
    payload = {"env": 0, "messages": []}
print(json.dumps(payload) + "\n", flush=True)
# A persistent REPL waits for another command; the backend must retire it.
time.sleep(60)
