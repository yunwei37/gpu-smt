from pathlib import Path
import json,os,select,subprocess
p=Path('/workspaces/repository')
a=p/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-solver-frontier/native-preprocess-dual'
u=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-solver-frontier')
prior=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle/full1000-third')
try:fd=os.pidfd_open(243173)
except ProcessLookupError:fd=None
if fd is not None:select.select([fd],[],[]);os.close(fd)
terminal=json.loads((prior/'terminal.json').read_text())
assert terminal['state']=='complete' and terminal['attempts']==2000
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT='/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle',GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(a/'run-qualification.py'),'--out',str(u/'native-preprocess-dual1000'),'--input',str(p/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'),'--limit','1000','--width','8','--affinity','0','1','2','3','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods','oracle-highs','--reuse-reference',str(prior/'rep1-fast-hybrid')]
print(json.dumps({'event':'prior_terminal','terminal':terminal,'argv':cmd}),flush=True)
subprocess.run(cmd,cwd=p,env=env,check=True)
