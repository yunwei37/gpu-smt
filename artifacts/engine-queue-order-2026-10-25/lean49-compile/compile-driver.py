import pathlib,subprocess,os,time,json,gzip,datetime,signal,psutil
r=pathlib.Path('/workspaces/repository')
project=pathlib.Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel')
sdk=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
d=pathlib.Path('/tmp/gpu-smt-lean49-compile-20261025')
a=r/'artifacts/engine-queue-order-2026-10-25/lean49-compile'
a.mkdir(exist_ok=True)
os.sched_setaffinity(0,{8,9,10,11})
cmd=[str(sdk/'bin/lake'),'env',str(sdk/'bin/lean'),'-R',str(r/'native/lean'),'-c',str(d/'GpuSmtPrepared.c'),str(r/'native/lean/GpuSmtPrepared.lean')]
env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'],LEAN_SYSROOT=str(sdk))
root=psutil.Process()
old=psutil.Process(283334)
assert abs(old.create_time()-1792912973.05)<.01
samples=[];pressure=False;start=time.monotonic()
with (d/'compile.log').open('wb')as f:
 p=subprocess.Popen(cmd,cwd=project,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 while True:
  processes={}
  for owner in [root,old]:
   try:
    if owner==old and abs(owner.create_time()-1792912973.05)>.01:continue
    for q in [owner]+owner.children(recursive=True):
     try:processes[(q.pid,q.create_time())]=q.memory_info().rss
     except psutil.NoSuchProcess:pass
   except psutil.NoSuchProcess:pass
  total=sum(processes.values())
  samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total,owned=[dict(pid=k[0],birth=k[1],rss=v)for k,v in processes.items()]))
  if total>48*1024**3 and p.poll()is None:
   pressure=True
   # Abort only this bounded compilation; never invalidate the live old group.
   os.killpg(p.pid,signal.SIGKILL)
  if p.poll()is not None:break
  time.sleep(1)
 code=p.wait()
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,cwd=str(project),exit=code,seconds=time.monotonic()-start,aggregate_peak_rss_bytes=max(x['rss_bytes']for x in samples),aggregate_budget_bytes=48*1024**3,pressure_aborted_new_build=pressure,scope='Compile engine module against actual retained Lean4.9/REPL API only; no proof candidate collection, no dependency build/source changes, no fixed AS cap; sample both known research group and bounded compiler each second.',dependency_archive_link='not executed; existing native capture stays frozen')
(a/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(a/'compile.log.gz').write_bytes(gzip.compress((d/'compile.log').read_bytes(),mtime=0))
(a/'memory-samples.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(s)+'\n'for s in samples)).encode(),mtime=0))
(a/'source-GpuSmtPrepared.lean').write_bytes((r/'native/lean/GpuSmtPrepared.lean').read_bytes())
print(json.dumps(receipt),flush=True)
print((d/'compile.log').read_text()[-5000:],flush=True)
