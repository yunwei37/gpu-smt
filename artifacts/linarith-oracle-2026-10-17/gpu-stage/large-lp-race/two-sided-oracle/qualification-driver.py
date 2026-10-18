from pathlib import Path
import os,json,subprocess,resource,time
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
p=Path('/workspaces/repository');u=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle')
a=p/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/two-sided-oracle'
base=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(p/'bench/lean-native/linarith-oracle/run-race.py'),'--input',str(a/'input-negative10.jsonl'),'--limit','10','--width','8','--affinity','8','9','10','11','--native-buckets','--repl','/tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl']
env=dict(os.environ,GPU_ARITHMETIC_RACE_ROOT=str(u),GPU_ARITHMETIC_RACE_MIN_ROWS='11')
env.pop('GPU_ARITHMETIC_NEGATIVE_CERTIFICATES',None)
for name,methods,negative in [('qualification10-success-only',['fast-hybrid','oracle-highs'],False),('qualification10-two-sided',['oracle-highs'],True)]:
 runenv=dict(env)
 if negative:runenv['GPU_ARITHMETIC_NEGATIVE_CERTIFICATES']='1'
 cmd=base+['--out',str(u/name),'--methods',*methods]
 if negative:cmd+=['--reuse-reference',str(u/'qualification10-success-only/rep1-fast-hybrid')]
 with(u/(name+'-driver.log')).open('w')as log:
  child=subprocess.Popen(cmd,cwd=p,env=runenv,stdout=log,stderr=subprocess.STDOUT)
  print(json.dumps({'pid':child.pid,'argv':cmd,'negative_certificates':negative}),flush=True)
  status=child.wait()
 if status:raise SystemExit(status)
print('COMPLETE',flush=True)
