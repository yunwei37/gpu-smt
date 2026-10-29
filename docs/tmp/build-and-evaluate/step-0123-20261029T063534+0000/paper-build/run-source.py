from pathlib import Path
import psutil,subprocess,time,os,signal,json,gzip,shutil
from datetime import datetime,timezone
r=Path('/workspaces/repository')
step=Path('/workspaces/repository/docs/tmp/build-and-evaluate/step-0123-20261029T063534+0000')
out=Path('/tmp/gpu-smt-paper-frontier-and-lrat-prior-20261029')
out.mkdir(exist_ok=False)
dest=step/'paper-build';dest.mkdir()
command=['taskset','-c','11','/workspaces/.agent-state/gpu-smt-deps/tectonic-0.17.0/tectonic',
 str(r/'docs/paper/main.tex'),'--outdir',str(out),'--keep-logs']
budget=48*1024**3
def birth(pid):
 try:return int(Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()[19])
 except (OSError,IndexError,ValueError):return None
def owned_snapshot(helper=None):
 roots=[psutil.Process(os.getpid()),psutil.Process(os.getppid())]
 if birth(551646)==168353179:
  roots.append(psutil.Process(551646))
 elif birth(551647)==168353182:
  roots.append(psutil.Process(551647))
 if helper is not None:
  try:roots.append(psutil.Process(helper.pid))
  except psutil.NoSuchProcess:pass
 processes={}
 for root in roots:
  try: candidates=[root]+root.children(recursive=True)
  except psutil.NoSuchProcess:continue
  for p in candidates:
   try:processes[(p.pid,p.create_time())]=p.memory_info().rss
   except psutil.NoSuchProcess:pass
 return sum(processes.values())
before=owned_snapshot()
if before>budget:
 raise RuntimeError('Existing own RSS is over budget; new compiler not started')
started=datetime.now(timezone.utc).isoformat();begin=time.monotonic()
samples=[];pressure=False
with (out/'command.log').open('wb')as log:
 p=subprocess.Popen(command,cwd=r/'docs/paper',stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 while True:
  rss=owned_snapshot(p)
  samples.append({'seconds':time.monotonic()-begin,'combined_rss_bytes':rss})
  if rss>budget and p.poll() is None:
   pressure=True;os.killpg(p.pid,signal.SIGTERM)
  if p.poll() is not None:break
  time.sleep(1)
 rc=p.wait()
receipt={'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),
 'command':command,'exit':rc,'seconds':time.monotonic()-begin,
 'combined_sampled_peak_bytes':max(x['combined_rss_bytes']for x in samples),
 'pressure_aborted_only_new_compiler':pressure,'original42CLI_pid':551647,
 'original42CLI_start_ticks':168353182,'native_Lean_executions':0,
 'scope':'SingleCPU11document compile;combined sampled own trees;support interference remains disclosed'}
(dest/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
with gzip.open(dest/'memory-samples.jsonl.gz','wt')as f:
 for x in samples:f.write(json.dumps(x)+'\n')
for name in ['main.pdf','main.log','command.log']:
 f=out/name
 if f.exists():
  raw=f.read_bytes();encoded=gzip.compress(raw,mtime=0);assert gzip.decompress(encoded)==raw
  (dest/(name+'.gz')).write_bytes(encoded)
print(json.dumps(receipt))
if rc!=0 or pressure:raise RuntimeError('Paper compile incomplete; evidence retained')
shutil.copyfile(out/'main.pdf',r/'docs/paper/main.pdf')
assert (r/'docs/paper/main.pdf').read_bytes()==gzip.decompress((dest/'main.pdf.gz').read_bytes())
