from pathlib import Path
import os,json,subprocess,resource,datetime,gzip
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
p=Path('/workspaces/repository')
a=p/'artifacts/linarith-oracle-2026-10-17/gpu-stage/full29750-generalization'
u=Path('/tmp/gpu-smt-linarith-oracle-20261017/full29750-generalization-recovery2-20261019')
inp=p/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl'
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT='/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle',GPU_ARITHMETIC_RACE_MIN_ROWS='11',GPU_ARITHMETIC_NEGATIVE_CERTIFICATES='1')
python='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python'
def cell(epoch,name,wrapper,methods,ref=None,limit=0):
 out=u/(epoch+'-'+name)
 cmd=[python,str(a/wrapper),'--out',str(out),'--input',str(inp),'--limit',str(limit),'--width','8','--affinity','0','1','2','3','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl','--methods',*methods]
 if ref:cmd+=['--reuse-reference',str(ref)]
 print(json.dumps({'event':'launch','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd}),flush=True)
 subprocess.run(cmd,cwd=p,env=env,check=True)
 return out
def read(path):
 with gzip.open(path,'rt')as f:return[json.loads(l)for l in f]

ref=cell('full29750','native','run-ast.py',['fast-hybrid'])
cell('full29750','native-dual','run-native.py',['oracle-highs'],ref/'rep1-fast-hybrid')
cell('full29750','direct-dual','run-ast.py',['oracle-highs'],ref/'rep1-fast-hybrid')
print('FULL_BLOCK_COMPLETE',flush=True)
