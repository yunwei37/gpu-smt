from pathlib import Path
import os,select,json,subprocess,gzip,shutil,resource,datetime
r=Path('/workspaces/repository');u=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle/full1000-phase1')
a=r/'artifacts/linarith-oracle-2026-10-17/gpu-stage/full1000-phase1'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{4,5,6,7})
pid=18460;identity='71246143'
try:
 fd=os.pidfd_open(pid);actual=Path('/proc/'+str(pid)+'/stat').read_text().rsplit(')',1)[1].split()[19]
 if actual!=identity:raise RuntimeError('original driver identity changed; no collection')
 poll=select.poll();poll.register(fd,select.POLLIN);poll.poll();os.close(fd)
except ProcessLookupError:pass
closed={}
for name in ['oracle-gpu','oracle-highs','fast-hybrid']:
 p=u/('rep1-'+name)/'terminal.json'
 if not p.exists():raise RuntimeError('driver exited before all cells terminal: '+name)
 t=json.loads(p.read_text());closed[name]={'state':t['state'],'attempts':t['attempts'],'counts':t['counts'],'whole_ns':t['whole_ns']}
proc=subprocess.run(['python3',str(r/'bench/lean-native/linarith-oracle/analyze-batch.py'),str(u)],text=True,capture_output=True)
(a/'paired-analysis-command.log').write_text(proc.stdout+proc.stderr)
if proc.returncode:raise RuntimeError('analysis failed '+str(proc.returncode))
for name in ['oracle-highs','fast-hybrid','oracle-highs-backend']:
 src=u/('rep1-'+name)
 if not src.exists():continue
 dst=a/('rep1-'+name);dst.mkdir(exist_ok=True)
 for p in src.iterdir():
  if not p.is_file():continue
  if p.suffix in ['.gz','.json']:shutil.copy2(p,dst/p.name)
  else:
   with p.open('rb')as source,(dst/(p.name+'.gz')).open('wb')as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0)as compressed:shutil.copyfileobj(source,compressed)
shutil.copy2(u/'paired-analysis.json',a/'paired-analysis.json')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':'original_driver_exit','driver_pid':pid,'start_ticks':identity,'closed':closed,'analysis_exit':proc.returncode,'scope':'single pidfd-triggered offline collection; no Agent, polling timer or automatic git'}
(a/'closed-pair-collection.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt),flush=True)
