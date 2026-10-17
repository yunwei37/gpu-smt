from pathlib import Path
import subprocess
r=Path("/workspaces/repository")
u=Path("/tmp/gpu-smt-linarith-oracle-20261017")
for label,interval in [("on",1),("off",0)]:
 cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '/workspaces/repository/bench/lean-native/linarith-oracle/run-comparison.py', '--out', 'OUT', '--input', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/strong-fallback-preflight-input.jsonl', '--methods', 'fast-hybrid', '--affinity', '0', '1', '2', '3', '--sample-seconds', 'INTERVAL']
 cmd[cmd.index("OUT")]=str(u/("observer-overhead-"+label))
 cmd[cmd.index("INTERVAL")]=str(interval)
 subprocess.run(cmd,cwd=r,check=True)
