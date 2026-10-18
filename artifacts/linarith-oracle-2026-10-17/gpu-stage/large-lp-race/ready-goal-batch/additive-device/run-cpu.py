from pathlib import Path
import subprocess,os,json,datetime,resource
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch/additive-device'
Q=A.parent/'argument-goals';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/ready-goal-additive-device')
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
q=json.loads((Q/'preflight-analysis.json').read_text())
assert q['parsed_external_LP_requests_in_ready_groups']>0
assert not q['ready-batch']['verdict_differences'] and not q['ready-batch']['non_message_differences']
assert json.loads((A/'build-receipt.json').read_text())['exit']==0
out=U/'qualification15-cpu'
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'),
GPU_ARITHMETIC_GOAL_BATCH='1',GPU_SMT_GOAL_BATCH_LOG=str(out/'goal-batches.jsonl'),GPU_SMT_GOAL_BATCH_EXCHANGE_LOG=str(out/'batch-exchanges.jsonl'))
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-device.py'),'--out',str(out),'--input',str(Q/'preflight-input.jsonl'),'--limit','0','--width','8','--affinity','8','9','10','11','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','fast-hybrid','oracle-highs']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
subprocess.run(cmd,cwd=R,env=env,check=True)
