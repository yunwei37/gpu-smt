from pathlib import Path
import os,subprocess,json,datetime
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-queue-control'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-queue-control')
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT='/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle',GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
python='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
input=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/candidate-capacity32/input-first64.jsonl'
for mode,script in [('static',R/'bench/lean-native/linarith-oracle/run-race.py'),('dynamic',A/'run-dynamic.py')]:
 argv=[python,str(script),'--out',str(U/('qualification64-'+mode)),'--input',str(input),'--limit','64','--width','8','--affinity','4','5','6','7','--native-buckets','--repl',str(U/'repl'),'--methods','fast-hybrid']
 print(json.dumps({'event':'launch','mode':mode,'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv}),flush=True)
 subprocess.run(argv,cwd=R,env=env,check=True)
 print(json.dumps({'event':'closed','mode':mode}),flush=True)
(A/'qualification-driver-terminal.json').write_text(json.dumps({'state':'closed','time':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
