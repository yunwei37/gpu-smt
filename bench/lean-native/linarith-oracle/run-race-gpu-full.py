"""Full original1000 GPU cell after matched pooled native/CPU cells retire."""
import os,sys,json,time,subprocess,resource
from pathlib import Path
import grpc
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,{0,1,2,3})
cpu=json.loads((U/'width8-full1000-pooled-cpu/rep1-oracle-hint/terminal.json').read_text())
assert cpu['state']=='complete' and cpu['counts']=={'complete':992,'rejected':8}, 'CPU qualification must close before GPU launch'
import gzip
C=U/'width8-full1000-pooled-cpu'
def records(path):
 with gzip.open(path,'rt')as f:return [json.loads(line)for line in f]
baseline=records(C/'rep1-fast-hybrid/responses.jsonl.gz')
oracle=records(C/'rep1-oracle-hint/responses.jsonl.gz')
assert len(baseline)==len(oracle)==1000
for method in ['fast-hybrid','oracle-hint']:
 t=json.loads((C/('rep1-'+method)/'terminal.json').read_text())
 assert t['state']=='complete' and t['counts']=={'complete':992,'rejected':8}
assert all(x['index']==y['index']and x['proof_id']==y['proof_id']and x['outcome']==y['outcome']and{k:v for k,v in x['response'].items()if k!='messages'}=={k:v for k,v in y['response'].items()if k!='messages'}for x,y in zip(baseline,oracle))
host=sys.argv[1];channel=grpc.insecure_channel(host+':5001')
grpc.channel_ready_future(channel).result(timeout=60);channel.close()
env=dict(os.environ);env['GPU_SMT_CUOPT_HOST']=host;env['GPU_ARITHMETIC_RACE_MIN_ROWS']=str(json.loads((R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/full1000-row-selection.json').read_text())['threshold_rows'])
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(D/'run-race.py'),'--out',str(U/'width8-full1000-gpu'),'--methods','oracle-gpu','--width','8','--affinity','0','1','2','3','--reuse-reference',str(U/'width8-full1000-pooled-cpu/rep1-fast-hybrid')]
start=time.monotonic_ns()
with (U/'width8-full1000-gpu-driver.log').open('w')as log:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 receipt={'utc':time.strftime('%FT%TZ',time.gmtime()),'pid':p.pid,'start_ticks':Path('/proc',str(p.pid),'stat').read_text().split()[21],'argv':cmd,'host':host,'min_rows':int(env['GPU_ARITHMETIC_RACE_MIN_ROWS']),'minimum_live_GPU_batch':2,'RLIMIT_AS':48*1024**3,'scope':'full original1000 sources; strong pooled native/CPU reference; corrected family; width8; CPU/GPU sameLP race before search; all server/client CPUs0--3; no numeric warmup'}
 (A/'arithmetic-large-lp-race-full1000-launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);code=p.wait()
result={'exit':code,'wrapper_whole_ns':time.monotonic_ns()-start,'utc':time.strftime('%FT%TZ',time.gmtime())}
(A/'arithmetic-large-lp-race-full1000-return.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True);sys.exit(code)
