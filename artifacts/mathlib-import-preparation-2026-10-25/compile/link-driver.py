import pathlib,subprocess,os,time,json,gzip,datetime,signal,psutil
r=pathlib.Path('/workspaces/repository');d=pathlib.Path('/tmp/gpu-smt-mathlib-import-20261025/build')
a=r/'artifacts/mathlib-import-preparation-2026-10-25/compile'
project=pathlib.Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel')
sdk=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
os.sched_setaffinity(0,{10})
objects=sorted((project/'.lake/build/ir/REPL').rglob('*.c.o.export'))
assert objects and len({p.name for p in objects})==len(objects)
cmds=[
 ['ar','rcs',str(d/'libREPL-existing.a')]+[str(p)for p in objects],
 ['objcopy','--redefine-sym','main=gpu_smt_dependency_main',str(d/'libREPL-existing.a'),str(d/'libREPL-embedded.a')],
 [str(sdk/'bin/leanc'),'-O3','-c',str(d/'GpuSmtPrepared.c'),'-o',str(d/'GpuSmtPrepared.o')],
 [str(sdk/'bin/leanc'),'-std=gnu11','-O2','-Wall','-Wextra','-Werror','-c',str(r/'native/lean/prepared_host.c'),'-o',str(d/'prepared_host.o')],
 [str(sdk/'bin/leanc'),'-O3','-rdynamic','-L'+str(sdk/'lib'),'-o',str(d/'prepared-host'),str(d/'prepared_host.o'),str(d/'GpuSmtPrepared.o'),str(d/'libREPL-embedded.a')]
]
env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'],LEAN_SYSROOT=str(sdk),LEAN_CC='cc')
root=psutil.Process();old=psutil.Process(283334)
assert abs(old.create_time()-1792912973.05)<.01
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Compile/link only against unchanged retained Lean4.9/REPL objects. No native candidate execution, no dependency output mutations, no fixed AS cap. Existing object members archived privately because the original collector uses the same project.',object_inputs=[dict(path=str(p),bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns)for p in objects],commands=[])
ancillary=[]
launch=json.loads((r/'artifacts/lean-code-verification-2026-10-25/native-prerequisite-build-20261025/launch.json').read_text())
try:
 q=psutil.Process(launch['pid'])
 if abs(q.create_time()-launch['birth'])<.01:ancillary.append(q)
except psutil.NoSuchProcess:pass
samples=[];start=time.monotonic()
for i,cmd in enumerate(cmds):
 t=time.monotonic();pressure=False
 with (d/('link-'+str(i)+'.log')).open('wb')as f:
  p=subprocess.Popen(cmd,cwd=project,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  while True:
   owners={}
   for owner in [root,old]+ancillary:
    try:
     for q in [owner]+owner.children(recursive=True):
      try:owners[(q.pid,q.create_time())]=q.memory_info().rss
      except psutil.NoSuchProcess:pass
    except psutil.NoSuchProcess:pass
   total=sum(owners.values())
   samples.append(dict(seconds=time.monotonic()-start,command=i,rss_bytes=total,owned=[dict(pid=k[0],birth=k[1],rss=v)for k,v in owners.items()]))
   if total>48*1024**3 and p.poll()is None:
    pressure=True;os.killpg(p.pid,signal.SIGKILL)
   if p.poll()is not None:break
   time.sleep(1)
  code=p.wait()
 row=dict(command=cmd,exit=code,seconds=time.monotonic()-t,pressure_aborted_new_build=pressure)
 receipt['commands'].append(row)
 (a/('link-'+str(i)+'.log.gz')).write_bytes(gzip.compress((d/('link-'+str(i)+'.log')).read_bytes(),mtime=0))
 (a/'link-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(row),flush=True)
 if code:print((d/('link-'+str(i)+'.log')).read_text()[-8000:],flush=True);break
receipt.update(aggregate_peak_rss_bytes=max(s['rss_bytes']for s in samples),aggregate_budget_bytes=48*1024**3,output_built=all(c['exit']==0 for c in receipt['commands'])and len(receipt['commands'])==len(cmds),executed=False)
(a/'link-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(a/'link-memory-samples.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(s)+'\n'for s in samples)).encode(),mtime=0))
(a/'link-driver.py').write_bytes(pathlib.Path(__file__).read_bytes())
(a/'source-prepared_host.c').write_bytes((r/'native/lean/prepared_host.c').read_bytes())
print(json.dumps({k:v for k,v in receipt.items()if k not in ['object_inputs','commands']}),flush=True)
