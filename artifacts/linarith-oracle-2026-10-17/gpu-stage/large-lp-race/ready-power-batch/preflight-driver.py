from pathlib import Path
import os,subprocess,resource,json,datetime
R=Path("/workspaces/repository");A=R/"artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-power-batch";U=Path("/tmp/gpu-smt-linarith-oracle-20261017/ready-power-batch")
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
subprocess.run(["python3",str(A/"build.py")],cwd=R,check=True)
for label,enabled in [("sequential",False),("ready",True)]:
 out=U/("preflight15-"+label)
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS="11",GPU_ARITHMETIC_NEGATIVE_CERTIFICATES="1",GPU_SMT_COST_FRONTEND="power",GPU_SMT_NATIVE_OMEGA_CONTROL="1",GPU_SMT_OMEGA_CONTROL_LOG=str(out/"omega-calls.jsonl"),
 GPU_ARITHMETIC_GOAL_BATCH="1"if enabled else"0",GPU_SMT_GOAL_BATCH_LOG=str(out/"goal-batches.jsonl"),GPU_SMT_GOAL_BATCH_EXCHANGE_LOG=str(out/"batch-exchanges.jsonl"))
 env.pop("GPU_ARITHMETIC_NUMERIC_PHASE_LOG",None)
 cmd=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python",str(A/"run-ready-power.py"),"--out",str(out),"--input",str(A.parent/"ready-goal-batch/argument-goals/preflight-input.jsonl"),"--limit","0","--width","8","--affinity","8","9","10","11","--native-buckets","--repl","/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl","--methods","oracle-highs"]
 print(json.dumps({"mode":label,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":cmd}),flush=True);subprocess.run(cmd,cwd=R,env=env,check=True)
(A/"preflight-terminal.json").write_text(json.dumps({"state":"complete","utc":datetime.datetime.now(datetime.timezone.utc).isoformat()})+"\n")
