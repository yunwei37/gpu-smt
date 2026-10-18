from pathlib import Path
import os,resource,subprocess,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-omega-cost';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/strong-omega-cost')
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
out=U/'qualification15-native-dual'
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'),GPU_SMT_COST_FRONTEND='native',
GPU_ARITHMETIC_NUMERIC_PHASE_LOG=str(out/'numeric-phases.jsonl'))
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-profile.py'),'--out',str(out),'--input',str(A.parent/'ready-goal-batch/argument-goals/preflight-input.jsonl'),'--limit','0','--width','8','--affinity','4','5','6','7','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','oracle-highs','--diagnostic']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
subprocess.run(cmd,cwd=R,env=env,check=True)
(A/'native-dual-qualification-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
