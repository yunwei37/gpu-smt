from pathlib import Path
import os,select,json,time,subprocess,resource,datetime
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
R=Path("/workspaces/repository");U=Path("/tmp/gpu-smt-linarith-oracle-20261017/pooled-wall-cost")
pid=138135;p=Path("/proc")/str(pid)
if p.exists() and (p/"stat").read_text().split()[2]!="Z":
 cmd=(p/"cmdline").read_bytes().replace(b"\0",b" ").decode()
 if "width8-full1000-gpu"not in cmd:raise RuntimeError("GPU collector owner changed; preserve state")
 try:fd=os.pidfd_open(pid)
 except ProcessLookupError:fd=None
 if fd is not None:
  try:select.select([fd],[],[])
  finally:os.close(fd)
# This finite benchmark continuation waits for the existing lifecycle's final
# persisted receipt, not just a Lean reply or collector process exit.
receipt=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target/arithmetic-large-lp-race-full1000-cleanup.json"
while not receipt.exists():time.sleep(1)
r=json.loads(receipt.read_text())
if r["deleteExit"]!=0 or r["labReady"]!="True" or r["otherWorkspacePhase"]!="Running":
 raise RuntimeError("GPU lifecycle did not restore its declared boundary")
q=json.loads((U/"qualification24-parity.json").read_text())
if any(x["count"]!=24 for x in q.values()):raise RuntimeError("qualification incomplete")
cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python","-u",str(R/"bench/lean-native/linarith-oracle/run-corrected-cost.py"),
 "--cost-profile","--cost-root",str(U),"--out",str(U/"full1000"),"--methods","fast-hybrid","oracle","--width","8","--affinity","0","1","2","3"]
env=dict(os.environ);env["GPU_ARITHMETIC_RACE_MIN_ROWS"]="11"
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
(U/"full1000-start.json").write_text(json.dumps({"utc":start,"argv":cmd,"after_GPU_cleanup":r,"scope":"own pooled-family diagnostic; same original1000,width8,CPU0–3,48GiB; no primary overlap"},indent=2)+"\n")
print("GPU lifecycle retired; begin pooled own-clock full profile",start,flush=True)
result=subprocess.run(cmd,env=env)
(U/"full1000-return.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"returncode":result.returncode})+"\n")
raise SystemExit(result.returncode)
