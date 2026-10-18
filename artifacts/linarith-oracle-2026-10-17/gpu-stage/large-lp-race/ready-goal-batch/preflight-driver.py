from pathlib import Path
import subprocess,os,json,datetime,resource
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/ready-goal-batch')
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
for label,enabled in [('sequential',False),('ready-batch',True)]:
 out=U/('preflight-'+label)
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
 GPU_SMT_CONTROL_FRONTEND='direct',GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'),
 GPU_ARITHMETIC_GOAL_BATCH='1'if enabled else'0',GPU_SMT_GOAL_BATCH_LOG=str(out/'goal-batches.jsonl'))
 cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-goals.py'),'--out',str(out),'--input',str(A/'preflight-input.jsonl'),'--limit','0','--width','8','--affinity','8','9','10','11','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','oracle-highs']
 print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'argv':cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
(A/'preflight-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
