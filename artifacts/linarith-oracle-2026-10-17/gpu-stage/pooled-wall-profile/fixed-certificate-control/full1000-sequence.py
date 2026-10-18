from pathlib import Path
import os,json,subprocess,resource,datetime
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
R=Path("/workspaces/repository");U=Path("/tmp/gpu-smt-linarith-oracle-20261017/numeric-replay")
env=dict(os.environ);env["GPU_ARITHMETIC_RACE_MIN_ROWS"]="11"
base=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python","-u",str(R/"bench/lean-native/linarith-oracle/run-race.py"),"--width","8","--affinity","0","1","2","3"]
for name,methods,extra in[
 ("full1000-baseline",["fast-hybrid"],[]),
 ("full1000-replay",["fast-hybrid","oracle-hint"],["--numeric-replay-bin",str(U/"numeric-replay")])]:
 if extra:env["GPU_ARITHMETIC_REPLAY_DATA"]=str(U/"full1000-cache.jsonl")
 command=base+["--out",str(U/name),"--methods",*methods]+extra
 print("BEGIN",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 result=subprocess.run(command,env=env);print("END",name,result.returncode,flush=True)
 if result.returncode:raise SystemExit(result.returncode)
(U/"full1000-sequence-return.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"returncode":0})+"\n")
