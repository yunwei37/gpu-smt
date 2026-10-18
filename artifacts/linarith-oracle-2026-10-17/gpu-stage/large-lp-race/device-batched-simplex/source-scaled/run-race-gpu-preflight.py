"""Execute a matched finite source race qualification against an existing GPU Job."""
import os,sys,json,time,subprocess,resource,argparse
from pathlib import Path
import grpc
R=Path('/workspaces/repository');D=R/'bench/lean-native/linarith-oracle'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('host')
parser.add_argument('--input',type=Path)
parser.add_argument('--limit',type=int,default=24)
parser.add_argument('--minimum-ready',type=int,default=2)
parser.add_argument('--root',type=Path,default=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle-pooled'))
parser.add_argument('--affinity',type=int,nargs='+',default=[0,1,2,3])
parser.add_argument('--min-rows',type=int,default=37)
parser.add_argument('--label',default='labelled-large-lp-race-gpu24')
parser.add_argument('--out',type=Path)
parser.add_argument('--reference',type=Path,default=Path('/tmp/gpu-smt-linarith-oracle-20261017/race-oracle/qualification24-cpu/rep1-fast-hybrid'))
parser.add_argument('--cpu-qualification',type=Path)
parser.add_argument('--native-buckets',action='store_true')
parser.add_argument('--independent-jobs',action='store_true')
parser.add_argument('--device-simplex',action='store_true')
parser.add_argument('--original-feasibility',action='store_true')
parser.add_argument('--lp-method',choices=['PDLP','Barrier'],default='PDLP')
parser.add_argument('--repl',type=Path)
args=parser.parse_args();U=args.root
out=args.out or U/'labelled-qualification24-gpu'
A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.sched_setaffinity(0,set(args.affinity))
cpu_root=args.cpu_qualification or U/'qualification24-cpu'
cpu=json.loads((cpu_root/'rep1-oracle-hint/terminal.json').read_text())
assert cpu['state']=='complete' and cpu['attempts']==args.limit and not cpu['counts'].get('operational',0),'Matching CPU qualification must close before GPU launch'
if args.device_simplex:
 import socket
 with socket.create_connection((args.host,5001))as connection:
  connection.sendall(b'{"ping":true}\n')
  with connection.makefile('rb')as stream:assert json.loads(stream.readline())['ready']
else:
 channel=grpc.insecure_channel(args.host+':5001')
 grpc.channel_ready_future(channel).result(timeout=60);channel.close()
env=dict(os.environ);env['GPU_SMT_CUOPT_HOST']=args.host
if args.device_simplex:env['GPU_SMT_CUDA_BATCH_HOST']=args.host
env['GPU_ARITHMETIC_RACE_MIN_ROWS']=str(args.min_rows);env['GPU_ARITHMETIC_RACE_ROOT']=str(U)
if args.independent_jobs:env['GPU_ARITHMETIC_GPU_INDEPENDENT_JOBS']='1'
env['GPU_ARITHMETIC_GPU_LP_METHOD']=args.lp_method
if args.original_feasibility:env['GPU_ARITHMETIC_GPU_ORIGINAL_FEASIBILITY']='1'
env['GPU_ARITHMETIC_GPU_MIN_READY']=str(args.minimum_ready)
cmd=['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python',str(D/'run-race.py'),
 '--out',str(out),'--limit',str(args.limit),'--methods','oracle-gpu','--width','8',
 '--affinity',*[str(x)for x in args.affinity],'--reuse-reference',str(args.reference)]
if args.input:cmd+=['--input',str(args.input)]
if args.native_buckets:cmd+=['--native-buckets']
if args.repl:cmd+=['--repl',str(args.repl)]
build=json.loads((U/'build-receipt.json').read_text())
start=time.monotonic_ns()
with (U/(args.label+'-driver.log')).open('w')as log:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 receipt={'utc':time.strftime('%FT%TZ',time.gmtime()),'pid':p.pid,
  'start_ticks':Path('/proc',str(p.pid),'stat').read_text().split()[21],
  'argv':cmd,'host':args.host,'min_rows':args.min_rows,'minimum_live_GPU_batch':args.minimum_ready,'independent_jobs':args.independent_jobs,'lp_method':('device_phase_I_simplex'if args.device_simplex else args.lp_method),'original_feasibility':args.original_feasibility,'device_simplex':args.device_simplex,
  'RLIMIT_AS':48*1024**3,'affinity':args.affinity,'build':build,
  'scope':'Declared finite source cohort; corrected family; width8; sameLP CPU/GPU race; no numeric warmup; dispatch follows retained build receipt'}
 (A/('arithmetic-'+args.label+'-launch.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);code=p.wait()
result={'exit':code,'wrapper_whole_ns':time.monotonic_ns()-start,'utc':time.strftime('%FT%TZ',time.gmtime())}
(A/('arithmetic-'+args.label+'-return.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True);sys.exit(code)
