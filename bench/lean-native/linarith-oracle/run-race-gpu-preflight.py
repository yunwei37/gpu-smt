"""Execute the real24-source race qualification against the existing finite GPU Job."""
import os,sys,json,time,subprocess,resource
from pathlib import Path
import grpc
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle')
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,{0,1,2,3})
cpu=json.loads((U/'whole-lp-qualification24-cpu/rep1-oracle-hint/terminal.json').read_text())
assert cpu['state']=='complete' and cpu['counts']=={'complete':24}, 'CPU qualification must close before GPU launch'
host=sys.argv[1];channel=grpc.insecure_channel(host+':5001')
grpc.channel_ready_future(channel).result(timeout=60);channel.close()
env=dict(os.environ);env['GPU_SMT_CUOPT_HOST']=host;env['GPU_ARITHMETIC_RACE_MIN_ROWS']='37'
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(D/'run-race.py'),'--out',str(U/'whole-lp-qualification24-gpu'),'--limit','24','--methods','oracle-gpu','--width','8','--affinity','0','1','2','3','--reuse-reference',str(U/'qualification24-cpu/rep1-fast-hybrid')]
start=time.monotonic_ns()
with (U/'whole-lp-qualification24-gpu-driver.log').open('w')as log:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 receipt={'utc':time.strftime('%FT%TZ',time.gmtime()),'pid':p.pid,'start_ticks':Path('/proc',str(p.pid),'stat').read_text().split()[21],'argv':cmd,'host':host,'min_rows':37,'minimum_live_GPU_batch':2,'RLIMIT_AS':48*1024**3,'scope':'real24 sources; corrected family; width8; CPU/GPU sameLP race before search; all server/client CPUs0--3; no numeric warmup'}
 (A/'arithmetic-large-lp-race-gpu24-launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);code=p.wait()
result={'exit':code,'wrapper_whole_ns':time.monotonic_ns()-start,'utc':time.strftime('%FT%TZ',time.gmtime())}
(A/'arithmetic-large-lp-race-gpu24-return.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True);sys.exit(code)
