from pathlib import Path
import os,json,subprocess,resource,datetime
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
R=Path("/workspaces/repository");U=Path("/tmp/gpu-smt-linarith-oracle-20261017/native-bucket-control")
repl=Path("/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl")
env=dict(os.environ);env["GPU_ARITHMETIC_RACE_MIN_ROWS"]="11"
base=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python","-u",str(R/"bench/lean-native/linarith-oracle/run-race.py"),"--limit","24","--width","8","--affinity","8","9","10","11","--repl",str(repl),"--methods","fast-hybrid","oracle-hint"]
for name,extra in[("wave8-qualification24-cpu",[]),("bucket8-qualification24-cpu",["--native-buckets"])]:
 command=base+["--out",str(U/name)]+extra
 print("BEGIN",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 result=subprocess.run(command,env=env);print("END",name,result.returncode,flush=True)
 if result.returncode:raise SystemExit(result.returncode)
(U/"qualification24-return.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"returncode":0})+"\n")
