from pathlib import Path
import subprocess,json,datetime
R=Path("/workspaces/repository")
HERE=Path(__file__).resolve().parent
COMMANDS=[['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '-u', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/workspace-interruption-20261019/resume-http-after-repair.py'], ['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '-u', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/shred-closing/run-kimina.py', '--out', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/shred-closing/full-populations-recovery2-20261019', '--datasets', 'minif2f', '--full'], ['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '-u', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/workspace-interruption-20261019/resume-current29750-after-repair.py'], ['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '-u', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/workspace-interruption-20261019/resume-formal49-after-repair.py'], ['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python', '-u', '/workspaces/repository/artifacts/linarith-oracle-2026-10-17/workspace-interruption-20261019/resume-older29750-after-repair.py']]
for index,command in enumerate(COMMANDS):
 row=dict(index=index,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=command)
 print(json.dumps(dict(event="start",**row)),flush=True)
 with (HERE/("sequential-cell"+str(index)+".log")).open("wb")as log:
  result=subprocess.run(command,cwd=R,stdout=log,stderr=subprocess.STDOUT)
 print(json.dumps(dict(event="exit",index=index,code=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())),flush=True)
 if result.returncode:raise SystemExit(result.returncode)
