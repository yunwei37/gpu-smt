from pathlib import Path
import subprocess,os,time,json,gzip,datetime,signal,psutil
r=Path('/workspaces/repository')
base=r/'artifacts/rust-engine-2026-10-25/consumer-journal-20261026/validation'
old_info=json.loads(Path('/tmp/gpu-smt-resource-pair-20261025/active-full.json').read_text())
old=psutil.Process(old_info['pid'])
assert int((Path('/proc')/str(old.pid)/'stat').read_text().rsplit(')',1)[1].split()[19])==old_info['start_ticks']
os.sched_setaffinity(0,{11});root=psutil.Process();samples=[];pressure=False;errors=[]
os.environ.update(PATH='/usr/local/cargo/bin:'+os.environ.get('PATH',''),CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR='/tmp/gpu-smt-rust-engine-build-20261025/target')
os.sched_setaffinity(0,{10,11})
os.environ['RUSTDOCFLAGS']='-D warnings'
commands=[
 ['cargo','test','-p','gpu-smt-server','--example','resource_pair'],
 ['cargo','fmt','--all','--','--check'],
 ['cargo','clippy','--workspace','--all-targets','--','-D','warnings'],
 ['cargo','test','--workspace','--all-targets'],
 ['cargo','run','-p','gpu-smt-server','--example','resource_pair','--','--help']]
start=time.monotonic();receipts=[]
def sample():
 owned={}
 for owner in [root,old]:
  try:
   for q in [owner]+owner.children(recursive=True):
    try:owned[(q.pid,q.create_time())]=q.memory_info().rss
    except psutil.NoSuchProcess:pass
  except psutil.NoSuchProcess:pass
 total=sum(owned.values())
 samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total))
 return total
for i,cmd in enumerate(commands):
 p=None;begin=time.monotonic()
 with(base/('command-%d.log'%i)).open('wb')as log:
  try:
   if sample()>=48*1024**3:raise RuntimeError('No aggregate headroom for new offline analysis')
   p=subprocess.Popen(cmd,cwd=r,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
   while True:
    if sample()>48*1024**3 and p.poll()is None:
     pressure=True;os.killpg(p.pid,signal.SIGKILL)
    if p.poll()is not None:break
    time.sleep(1)
  except BaseException as e:errors.append(repr(e))
  finally:
   if p is not None:
    if p.poll()is None:os.killpg(p.pid,signal.SIGKILL)
    code=p.wait()
   else:code=None
 receipts.append(dict(command=cmd,exit=code,seconds=time.monotonic()-begin))
 if code!=0:break
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 commands=receipts,samples=len(samples),combined_peak_rss_bytes=max(x['rss_bytes']for x in samples),
 budget_bytes=48*1024**3,pressure_aborted_only_new_analysis=pressure,
 monitor_errors=errors,old_owner=old.pid,old_start_ticks=old_info['start_ticks'],
 native_candidate_executions=0,process_fixture_only=True)
(base/'receipt.json').write_text(json.dumps(receipt,indent=2)+chr(10))
(base/'memory-samples.jsonl.gz').write_bytes(gzip.compress(
 ''.join(json.dumps(x)+chr(10)for x in samples).encode(),mtime=0))
(base/'run-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(receipt),flush=True)
for p in sorted(base.glob('*.log')):print(p.name,p.read_text()[-4000:],flush=True)
raise SystemExit(0 if len(receipts)==len(commands)and receipts[-1]['exit']==0 else 1)
