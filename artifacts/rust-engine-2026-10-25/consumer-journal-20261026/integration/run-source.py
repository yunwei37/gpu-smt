from pathlib import Path
import os,json,gzip,subprocess,signal,time,datetime,threading,psutil
r=Path('/workspaces/repository');a=r/'artifacts/rust-engine-2026-10-25/consumer-journal-20261026/integration'
a.mkdir();tmp=Path('/tmp/gpu-smt-consumer-journal-20261026');os.sched_setaffinity(0,{10,11})
fixture=tmp/'hold-fixture.py'
fixture.write_text("#!/usr/bin/python3"+chr(10)+"import os,sys,json,time"+chr(10)+"from pathlib import Path"+chr(10)+"code=json.loads(sys.stdin.readline())['cmd']"+chr(10)+"if code=='held':"+chr(10)+" p=Path(os.environ['GPU_SMT_FIXTURE_MARKER']);q=p.with_suffix('.ready');q.write_text(str(os.getpid()));q.rename(p);time.sleep(60)"+chr(10)+"else:"+chr(10)+" print(json.dumps({'env':0,'fixture_pid':os.getpid()})+'"+chr(92)+"n',flush=True)"+chr(10))
fixture.chmod(0o700)
old_info=json.loads(Path('/tmp/gpu-smt-resource-pair-20261025/active-full.json').read_text())
old=psutil.Process(old_info['pid']);assert int(Path('/proc/%d/stat'%old.pid).read_text().rsplit(')',1)[1].split()[19])==old_info['start_ticks']
root=psutil.Process();samples=[];errors=[];pressure=[];current=[None];stop=threading.Event()
budget=48*1024**3
def sample():
 owned={}
 for owner in [root,old]:
  try:
   for p in [owner]+owner.children(recursive=True):
    try:owned[(p.pid,p.create_time())]=p.memory_info().rss
    except psutil.NoSuchProcess:pass
  except psutil.NoSuchProcess:pass
 total=sum(owned.values());samples.append(dict(mono=time.monotonic(),rss_bytes=total))
 if total>budget:
  pressure.append(total);p=current[0]
  if p is not None and p.poll()is None:p.send_signal(signal.SIGTERM)
 return total
def watch():
 while not stop.wait(1):
  try:sample()
  except BaseException as e:errors.append(repr(e))
watcher=threading.Thread(target=watch);watcher.start();receipts=[]
try:
 for signum in [signal.SIGTERM,signal.SIGINT]:
  assert sample()<budget,'No combined headroom; no fixture launched'
  cell=a/signum.name;cell.mkdir();out=cell/'pair'
  marker=tmp/(signum.name+'.pid');marker.unlink(missing_ok=True)
  batch=dict(mode='all',candidates=[dict(id=i,code=i,timeout_ms=300000,reuse=False)for i in ['fast','held']])
  (cell/'input.json').write_text(json.dumps(batch))
  (cell/'resources.json').write_text(json.dumps(dict(memory_bytes=budget,cpus=[10,11],cores_per_worker=1)))
  cmd=['/tmp/gpu-smt-rust-engine-build-20261025/target/debug/examples/resource_pair',str(cell/'input.json'),str(fixture),'/tmp','/usr/bin/true','/tmp','controlled-not-Lean',str(cell/'resources.json'),str(out)]
  env=os.environ.copy();env['GPU_SMT_FIXTURE_MARKER']=str(marker)
  begin=time.monotonic();known={};p=None
  with(cell/'driver.log').open('wb')as log:
   try:
    p=subprocess.Popen(cmd,cwd=r,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT);current[0]=p
    def remember():
     try:
      driver=psutil.Process(p.pid)
      for q in [driver]+driver.children(recursive=True):
       try:known[(q.pid,q.create_time())]=q
       except psutil.NoSuchProcess:pass
     except psutil.NoSuchProcess:pass
    until=time.monotonic()+10
    while True:
     remember();journal=out/'native/results.jsonl'
     text=journal.read_text()if journal.exists()else''
     if marker.exists()and text.endswith(chr(10))and text.strip():break
     assert p.poll()is None,'Driver exited before controlled body was held'
     assert time.monotonic()<until,'Fixture readiness deadline'
     time.sleep(.01)
    prefix=[json.loads(x)for x in text.splitlines()];assert len(prefix)==1 and prefix[0]['verification']['id']=='fast'
    assert prefix[0]['verification']['outcome']['status']=='accepted'
    sample();p.send_signal(signum)
    until=time.monotonic()+10
    while p.poll()is None:
     remember();assert time.monotonic()<until,'Driver termination deadline';time.sleep(.02)
    code=p.wait();assert code==1
    terminal=json.loads((out/'native/terminal.json').read_text())
    assert terminal['state']=='interrupted'and terminal['interrupted']
    assert not(out/'prepared').exists(),'Pair must stop after interrupted cell'
    events=[json.loads(x)for x in (out/'native/results.jsonl').read_text().splitlines()]
    assert events[-1]==dict(event='complete',count=2)
    with gzip.open(out/'native/capture.json.gz','rt')as f:capture=json.load(f)
    results={x['id']:x for x in capture['results']}
    assert results['fast']['outcome']['status']=='accepted'and results['held']['outcome']['status']=='backend_error'
    assert {e['verification']['id']:e['verification']for e in events if e['event']=='result'}==results
    live=[]
    for v in capture['results']:
     for attempt in v['attempts']:
      for identity in attempt['processes']:
       q=Path('/proc')/str(identity['pid'])/'stat'
       if q.exists()and int(q.read_text().rsplit(')',1)[1].split()[19])==identity['start_ticks']:live.append(identity)
    assert not live,live
    receipts.append(dict(signal=signum.name,command=cmd,exit=code,seconds=time.monotonic()-begin,
     prefix_results_before_signal=1,complete_consumer_rows=2,terminal_state=terminal['state'],
     statuses={k:v['outcome']['status']for k,v in results.items()},remaining_owned_processes=live,
     prepared_cell_started=False,native_candidate_executions=0,protocol_fixture_only=True))
   finally:
    if p is not None and p.poll()is None:
     p.send_signal(signal.SIGTERM)
     try:p.wait(timeout=2)
     except subprocess.TimeoutExpired:
      for (pid,birth),q in reversed(list(known.items())):
       try:
        if psutil.Process(pid).create_time()==birth:q.kill()
       except psutil.NoSuchProcess:pass
      p.kill();p.wait()
    current[0]=None;marker.unlink(missing_ok=True)
finally:
 stop.set();watcher.join();fixture.unlink(missing_ok=True)
 sample()
 receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),cases=receipts,
  sampled_combined_peak_rss_bytes=max(s['rss_bytes']for s in samples),budget_bytes=budget,
  pressure_samples=pressure,monitor_errors=errors,old_owner=old.pid,old_start_ticks=old_info['start_ticks'],
  scope='Actual debug example process with controlled Python protocol fixture, not Lean proof/performance or a second native acquisition.')
 (a/'receipt.json').write_text(json.dumps(receipt,indent=2)+chr(10))
 (a/'memory-samples.jsonl.gz').write_bytes(gzip.compress(''.join(json.dumps(x)+chr(10)for x in samples).encode(),mtime=0))
 (a/'run-source.py').write_bytes(Path(__file__).read_bytes())
 print(json.dumps(receipt),flush=True)
assert len(receipts)==2 and not pressure and not errors
