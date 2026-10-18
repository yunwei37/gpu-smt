from pathlib import Path
import os,subprocess,resource,json,datetime
R=Path("/workspaces/repository");A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/power-whole-repetitions";U=Path("/tmp/gpu-smt-linarith-oracle-20261017/power-whole-repetitions")
Q=A.parent/"power-export"
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
first=json.loads((Q/"full1000-result.json").read_text());assert first["state"]=="complete"
tail=json.loads((A.parent/"native-default-tail/result.json").read_text());assert tail["state"]=="complete"and tail["fidelity_qualified"]and not tail["consistent_default_improvement"]
for rep,order in [(2,["native-control","power"]),(3,["power","native-control"])]:
 for label in order:
  out=U/("rep"+str(rep)+"-"+label);native=label=="native-control"
  env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U.parent/"power-export"),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),GPU_SMT_COST_FRONTEND="native"if native else"power")
  env.pop("GPU_ARITHMETIC_NUMERIC_PHASE_LOG",None)
  cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",str(Q/"run-power.py"),"--out",str(out),"--input",str(A.parents[2]/"input-top1000.jsonl"),"--limit","1000","--width","8","--affinity","4","5","6","7","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods","fast-hybrid"if native else"oracle-highs"]
  print(json.dumps({"rep":rep,"condition":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":cmd}),flush=True);subprocess.run(cmd,cwd=R,env=env,check=True)
  print(json.dumps({"closed_rep":rep,"condition":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
(A/"terminal.json").write_text(json.dumps({"state":"complete","utc":datetime.datetime.now(datetime.timezone.utc).isoformat()})+"\n")
