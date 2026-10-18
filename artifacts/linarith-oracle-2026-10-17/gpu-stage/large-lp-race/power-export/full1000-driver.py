from pathlib import Path
import os,resource,subprocess,json,datetime
R=Path("/workspaces/repository");A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-export";U=Path("/tmp/gpu-smt-linarith-oracle-20261017/power-export")
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
admission=json.loads((A/"qualification-result.json").read_text());assert admission["complete1000_admission"]
input_path=A.parents[2]/"input-top1000.jsonl";assert len(input_path.read_text().splitlines())==1000
conditions=[("power","power","oracle-highs"),("direct","direct","oracle-highs"),("native-dual","native","oracle-highs"),("stock-native","native","fast-hybrid")]
for label,frontend,method in conditions:
 out=U/("full1000-"+label)
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),GPU_SMT_COST_FRONTEND=frontend)
 env.pop("GPU_ARITHMETIC_NUMERIC_PHASE_LOG",None)
 cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",str(A/"run-power.py"),"--out",str(out),"--input",str(input_path),"--limit","1000","--width","8","--affinity","4","5","6","7","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods",method]
 print(json.dumps({"condition":label,"frontend":frontend,"method":method,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
 print(json.dumps({"closed":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
(A/"full1000-terminal.json").write_text(json.dumps({"state":"complete","utc":datetime.datetime.now(datetime.timezone.utc).isoformat()})+"\n")
