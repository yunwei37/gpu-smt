from pathlib import Path
import os,select,json,subprocess,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile';U=Path('/tmp/gpu-smt-linarith-oracle-20261017/current-dual-phase-profile')
receipt=json.loads((A/'request-build-receipt.json').read_text())
assert len(receipt['commands'])==6 and all(x['exit']==0 for x in receipt['commands'])
assert (U/'arithmetic-batchd').is_file()and not(U/'arithmetic-batchd').is_symlink()
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(U),GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(A/'run-profile.py'),'--out',str(U/'full1000-with-requests'),'--input',str(R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'),'--limit','1000','--width','8','--affinity','4','5','6','7','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','fast-hybrid','oracle-highs','--diagnostic']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
subprocess.run(cmd,cwd=R,env=env,check=True)
(A/'full1000-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
