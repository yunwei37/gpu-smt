from pathlib import Path
import subprocess,os,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-omega-control';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-omega-control')
out=U/'preflight-direct-dual-omega'
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1',
GPU_SMT_CONTROL_FRONTEND='direct',GPU_SMT_NATIVE_OMEGA_CONTROL='1',GPU_SMT_OMEGA_CONTROL_LOG=str(out/'omega-calls.jsonl'))
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-control.py'),'--out',str(out),'--input',str(A/'preflight-input.jsonl'),'--limit','0','--width','8','--affinity','4','5','6','7','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','oracle-highs']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
subprocess.run(cmd,cwd=R,env=env,check=True)
(A/'direct-omega-preflight-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
