from pathlib import Path
import psutil,subprocess,time,os,signal,json,gzip,sys
from datetime import datetime,timezone
r=Path('/workspaces/repository')
step=r/Path('/tmp/gpu-smt-step0128-path.txt').read_text()
dest=step/'experiment-001'/sys.argv[1];dest.mkdir(exist_ok=False)
commands=json.loads(sys.argv[2]);budget=48*1024**3
os.sched_setaffinity(0,{11})
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',
 RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR='/tmp/gpu-smt-rust-engine-build-20261025/target',
 CARGO_BUILD_JOBS='1',RUST_TEST_THREADS='1')
def birth(pid):
 try:return int(Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()[19])
 except (OSError,IndexError,ValueError):return None
def sample(helper=None):
 roots=[psutil.Process()]
 if birth(551646)==168353179:roots.append(psutil.Process(551646))
 elif birth(551647)==168353182:roots.append(psutil.Process(551647))
 if helper is not None:
  try:roots.append(psutil.Process(helper.pid))
  except psutil.NoSuchProcess:pass
 processes={}
 for root in roots:
  try:children=[root]+root.children(recursive=True)
  except psutil.NoSuchProcess:continue
  for p in children:
   try:processes[(p.pid,p.create_time())]=p.memory_info().rss
   except psutil.NoSuchProcess:pass
 return sum(processes.values())
begin=time.monotonic();samples=[];rows=[];pressure=False
for index,command in enumerate(commands):
 if sample()>=budget:
  rows.append(dict(command=command,exit=None,error='No aggregate headroom'));break
 start=time.monotonic()
 with (dest/f'command-{index}.log').open('wb')as f:
  p=subprocess.Popen(command,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  while True:
   rss=sample(p);samples.append(dict(seconds=time.monotonic()-begin,combined_rss_bytes=rss))
   if rss>budget and p.poll()is None:
    pressure=True
    try:
     children=psutil.Process(p.pid).children(recursive=True)
     for q in reversed(children):
      try:q.kill()
      except psutil.NoSuchProcess:pass
    except psutil.NoSuchProcess:pass
    os.killpg(p.pid,signal.SIGKILL)
   if p.poll()is not None:break
   time.sleep(1)
  rc=p.wait()
 rows.append(dict(command=command,exit=rc,seconds=time.monotonic()-start))
 if rc!=0:break
result=dict(UTC=datetime.now(timezone.utc).isoformat(),commands=rows,seconds=time.monotonic()-begin,
 combined_peak_bytes=max((x['combined_rss_bytes']for x in samples),default=0),
 pressure_aborted_only_new_support=pressure,budget_bytes=budget,
 native_Lean_invocations=sum('lean' in Path(c['command'][0]).name for c in rows),scope='CPU11definition-only Lean compilation;native42unchanged;no candidate execution')
(dest/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
with gzip.open(dest/'memory-samples.jsonl.gz','wt')as f:
 for x in samples:f.write(json.dumps(x)+'\n')
(dest/'run-source.py').write_bytes(Path(__file__).read_bytes())
for p in dest.glob('*.log'):print(p.name,p.read_text()[-14000:]);p.with_suffix(p.suffix+'.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0));p.unlink()
print(json.dumps(result),flush=True)
