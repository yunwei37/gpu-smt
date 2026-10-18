from pathlib import Path
import os,subprocess,json,time,resource
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
R=Path("/workspaces/repository");U=Path("/tmp/gpu-smt-linarith-oracle-20261017/numeric-replay")
env=dict(os.environ);env["GPU_ARITHMETIC_RACE_MIN_ROWS"]="11"
base=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python","-u",str(R/"bench/lean-native/linarith-oracle/run-race.py"),"--limit","24","--width","8","--affinity","8","9","10","11"]
for name,methods,extra in [
 ("qualification24-baseline",["fast-hybrid"],[]),
 ("qualification24-replay",["fast-hybrid","oracle-hint"],["--numeric-replay-bin",str(U/"numeric-replay")])]:
 if extra:env["GPU_ARITHMETIC_REPLAY_DATA"]=str(U/"qualification24-cache.jsonl")
 command=base+["--out",str(U/name),"--methods",*methods]+extra
 print("BEGIN",name,flush=True)
 result=subprocess.run(command,env=env)
 print("END",name,result.returncode,flush=True)
 if result.returncode:raise SystemExit(result.returncode)
