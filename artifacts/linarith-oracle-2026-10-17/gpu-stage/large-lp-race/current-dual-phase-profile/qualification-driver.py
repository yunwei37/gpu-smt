from pathlib import Path
import os,subprocess,json,datetime
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/current-dual-phase-profile')
python='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
common=['--input',str(R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/candidate-capacity32/input-first64.jsonl'),
 '--limit','64','--width','8','--affinity','4','5','6','7','--native-buckets',
 '--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl']
for name,script,root,methods in [
 ('normal',R/'bench/lean-native/linarith-oracle/run-race.py','/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle',['oracle-highs']),
 ('profile',A/'run-profile.py',str(U),['fast-hybrid','oracle-highs'])]:
 env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=root,GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
 cmd=[python,str(script),'--out',str(U/('qualification64-'+name)),*common,'--methods',*methods]
 if name=='profile':cmd+=['--diagnostic']
 print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
 subprocess.run(cmd,cwd=R,env=env,check=True)
 print(json.dumps({'closed':name}),flush=True)
(A/'qualification-terminal.json').write_text(json.dumps({'state':'complete','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
