from pathlib import Path
import json,subprocess,time
r=Path("/workspaces/repository")
receipt=r/Path("/tmp/gpu-smt-step0131-path.txt").read_text()/"experiment-001/program-argument-driver-compile/receipt.json"
while not receipt.exists():
    time.sleep(.2)
assert all(x["exit"]==0 for x in json.loads(receipt.read_text())["commands"])
cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",
str(r/"bench/lean-failure-profile/state-reuse/run.py"),
"--input","/tmp/gpu-smt-state-reuse-20261029/extended-preflight.json.gz",
"--out","/tmp/gpu-smt-state-reuse-ack2-preflight-20261029",
"--context","/tmp/gpu-smt-solo42-native-library-20261028/rebound-point-13d4606.json",
"--module-dir","/tmp/gpu-smt-state-reuse-20261029"]
raise SystemExit(subprocess.call(cmd,cwd=r))
