from pathlib import Path
import os,subprocess,resource,json,time
R=Path("/workspaces/repository")
A=R/"artifacts/linarith-oracle-2026-10-17/formal-oracle-4.9"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/formal-oracle-4.9")
D=Path("/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture")
S=D/"lean-4.9.0-rc1-linux"
M=D/"mathlib4"
N=Path("/tmp/gpu-smt-native-mathlib-20261014/.lake/build/lib")
paths=[M/".lake/build/lib"]+[p/".lake/build/lib" for p in (M/".lake/packages").iterdir() if p.is_dir()]
env=os.environ.copy();env["PATH"]=str(S/"bin")+":"+env["PATH"]
env["LEAN_PATH"]=":".join(str(p) for p in [U]+paths)
env["LD_LIBRARY_PATH"]=":".join(str(p) for p in [N]+[p/".lake/build/lib" for p in (N.parents[2]/".lake/packages").glob("*")])
os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
U.mkdir(exist_ok=True)
(U/"FormalOracle49.lean").write_bytes((A/"FormalOracle49.lean").read_bytes())
commands=[[str(S/"bin/lean"),"-o","FormalOracle49.olean","-c","FormalOracle49.c","FormalOracle49.lean"],
[str(S/"bin/leanc"),"-O3","-shared","-fPIC","-o","libFormalOracle49.so","FormalOracle49.c","-L"+str(N),"-Wl,--no-as-needed","-l:libMathlib-Tactic-Linarith-1.so"]]
for i,cmd in enumerate(commands):
 t=time.monotonic();p=subprocess.run(cmd,cwd=U,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (A/f"build-{i}.log").write_text(p.stdout)
 print(json.dumps({"command":cmd,"returncode":p.returncode,"wall_seconds":time.monotonic()-t,"output":p.stdout[-10000:]}),flush=True)
 if p.returncode:raise SystemExit(p.returncode)
(A/"build-receipt.json").write_text(json.dumps({"commands":commands,"sdk":str(S),"library":str(N),"lean_path":env["LEAN_PATH"]},indent=2))
