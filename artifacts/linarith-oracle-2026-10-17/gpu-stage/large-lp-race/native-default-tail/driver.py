from pathlib import Path
import os,subprocess,resource,json,datetime
R=Path("/workspaces/repository");A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-default-tail";U=Path("/tmp/gpu-smt-linarith-oracle-20261017/native-default-tail")
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
assert len((A/"input-native-tail10.jsonl").read_text().splitlines())==10
for pair,orders in [(1,["default-tiered","hybrid"]),(2,["hybrid","default-tiered"])]:
 for route in orders:
  label="pair"+str(pair)+"-"+route;out=U/label
  env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U.parent/"power-export"),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_SMT_CONTROL_FRONTEND="native",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),GPU_SMT_STOCK_DEFAULT_TIERED="1"if route=="default-tiered"else"0",GPU_SMT_STOCK_ENGINE_RECEIPT=str(A/(label+"-engine-route.json")))
  cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",str(A/"run-native.py"),"--out",str(out),"--input",str(A/"input-native-tail10.jsonl"),"--limit","0","--width","8","--affinity","4","5","6","7","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods","fast-hybrid"]
  print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"label":label,"argv":cmd}),flush=True)
  subprocess.run(cmd,cwd=R,env=env,check=True)
  print(json.dumps({"closed":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
(A/"terminal.json").write_text(json.dumps({"state":"complete","utc":datetime.datetime.now(datetime.timezone.utc).isoformat()})+"\n")
