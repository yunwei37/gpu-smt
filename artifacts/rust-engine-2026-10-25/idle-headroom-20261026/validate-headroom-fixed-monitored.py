import pathlib,json,time,subprocess,os,signal,gzip,psutil,datetime
r=pathlib.Path('/workspaces/repository');tmp=pathlib.Path('/tmp/gpu-smt-rust-engine-build-20261025')
step=pathlib.Path(pathlib.Path('/tmp/gpu-smt-resource-pair-20261025/headroom-step.txt').read_text())
l=json.loads(pathlib.Path('/tmp/gpu-smt-resource-pair-20261025/active-full.json').read_text())
old=psutil.Process(l['pid']);assert int((pathlib.Path('/proc')/str(old.pid)/'stat').read_text().rsplit(')',1)[1].split()[19])==l['start_ticks']
root=psutil.Process();samples=[];errors=[];pressure=False
with(tmp/'validate-headroom-fixed-driver.log').open('wb')as f:p=subprocess.Popen(
 ['taskset','-c','10,11','python3',str(tmp/'validate-headroom-fixed.py')],
 cwd=r,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
while True:
 owned={}
 for owner in [root,old]:
  try:
   for q in [owner]+owner.children(recursive=True):
    try:owned[(q.pid,q.create_time())]=q.memory_info().rss
    except psutil.NoSuchProcess:pass
  except psutil.NoSuchProcess:pass
 total=sum(owned.values());samples.append(dict(time=time.monotonic(),rss_bytes=total))
 if total>48*1024**3 and p.poll()is None:
  pressure=True
  # Withdraw only this extra development check;the retained native run owns
  # its unchanged sampling/preemption policy and is never signalled here.
  try:
   child=psutil.Process(p.pid);children=child.children(recursive=True)
   for q in sorted(children,key=lambda x:x.memory_info().rss if x.is_running()else 0,reverse=True):
    try:q.kill()
    except psutil.NoSuchProcess:pass
   child.kill()
  except psutil.NoSuchProcess:pass
 if p.poll()is not None:break
 time.sleep(1)
code=p.wait()
(step/'experiment-001/fixed-development-rss.json').write_text(json.dumps(dict(
 exit=code,pressure_withdrew_only_new_validation=pressure,
 combined_peak_rss_bytes=max(x['rss_bytes']for x in samples),
 budget_bytes=48*1024**3,sampling_seconds=1,monitor_errors=errors,
 retained_full_owner=l['pid'],scope='Combined full collection plus new compiler/test/monitor trees;sampling not hard quota.'),indent=2)+'\n')
(step/'experiment-001/fixed-development-rss.jsonl.gz').write_bytes(gzip.compress(
 ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
print('VALIDATOR_EXIT',code,'PRESSURE',pressure,'PEAK',max(x['rss_bytes']for x in samples),flush=True)

raise SystemExit(code)
