"""Execute a real24-source race qualification against one existing finite GPU Job."""
import os,sys,json,time,subprocess,resource,argparse
from pathlib import Path
import grpc
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('host')
parser.add_argument('--root',type=Path,default=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled'))
parser.add_argument('--affinity',type=int,nargs='+',default=[0,1,2,3])
parser.add_argument('--min-rows',type=int,default=37)
parser.add_argument('--label',default='labelled-large-lp-race-gpu24')
parser.add_argument('--out',type=Path)
parser.add_argument('--reference',type=Path,default=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle/qualification24-cpu/rep1-fast-hybrid'))
args=parser.parse_args();U=args.root
out=args.out or U/'labelled-qualification24-gpu'
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,set(args.affinity))
cpu=json.loads((U/'qualification24-cpu/rep1-oracle-hint/terminal.json').read_text())
assert cpu['state']=='complete' and cpu['counts']=={'complete':24},'CPU qualification must close before GPU launch'
channel=grpc.insecure_channel(args.host+':5001')
grpc.channel_ready_future(channel).result(timeout=60);channel.close()
env=dict(os.environ);env['GPU_SMT_CUOPT_HOST']=args.host
env['GPU_ARITHMETIC_RACE_MIN_ROWS']=str(args.min_rows);env['GPU_ARITHMETIC_RACE_ROOT']=str(U)
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(D/'run-race.py'),
 '--out',str(out),'--limit','24','--methods','oracle-gpu','--width','8',
 '--affinity',*[str(x)for x in args.affinity],'--reuse-reference',str(args.reference)]
build=json.loads((U/'build-receipt.json').read_text())
start=time.monotonic_ns()
with (U/(args.label+'-driver.log')).open('w')as log:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 receipt={'utc':time.strftime('%FT%TZ',time.gmtime()),'pid':p.pid,
  'start_ticks':Path('/proc',str(p.pid),'stat').read_text().split()[21],
  'argv':cmd,'host':args.host,'min_rows':args.min_rows,'minimum_live_GPU_batch':2,
  'RLIMIT_AS':48*1024**3,'affinity':args.affinity,'build':build,
  'scope':'real24 sources; corrected family; width8; sameLP CPU/GPU race; no numeric warmup; dispatch follows retained build receipt'}
 (A/('arithmetic-'+args.label+'-launch.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);code=p.wait()
result={'exit':code,'wrapper_whole_ns':time.monotonic_ns()-start,'utc':time.strftime('%FT%TZ',time.gmtime())}
(A/('arithmetic-'+args.label+'-return.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True);sys.exit(code)
