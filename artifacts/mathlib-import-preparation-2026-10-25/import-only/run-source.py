from pathlib import Path
import datetime,gzip,json,os,psutil,resource,signal,subprocess,tempfile,threading,time
r=Path('/workspaces/repository');tmp=Path('/tmp/gpu-smt-mathlib-import-20261025')
a=r/'artifacts/mathlib-import-preparation-2026-10-25/import-only';a.mkdir(exist_ok=False)
sdk=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
host=tmp/'build/prepared-host'
os.sched_setaffinity(0,{10})
assert resource.getrlimit(resource.RLIMIT_AS)[0]==resource.RLIM_INFINITY
old=psutil.Process(283334);assert abs(old.create_time()-1792912973.05)<.01
repls=[q for q in old.children(recursive=True)if q.name()=='repl']
assert repls
reference=repls[0];context=reference.environ();project=Path(reference.cwd())
env=dict(os.environ)
for name in ['LEAN_PATH','LEAN_SRC_PATH']:
 if name in context:env[name]=context[name]
env['PATH']=str(sdk/'bin')+os.pathsep+env['PATH']
env['LEAN_SYSROOT']=str(sdk)
sources=json.loads(gzip.decompress((r/'artifacts/engine-resource-profile-2026-10-25/population-inputs/all.json.gz').read_bytes()))
source=sources['candidates'][0]
(a/'source.json').write_text(json.dumps(source,ensure_ascii=False)+'\n')
owners=[psutil.Process(),old]
launch=json.loads((r/'artifacts/lean-code-verification-2026-10-25/native-prerequisite-build-20261025/launch.json').read_text())
try:
 q=psutil.Process(launch['pid'])
 if abs(q.create_time()-launch['birth'])<.01:owners.append(q)
except psutil.NoSuchProcess:pass
work=Path(tempfile.mkdtemp(prefix='smt-import-',dir='/tmp'));socket=work/'s'
cmd=[str(host),str(socket),str(sdk)]
start=time.monotonic();stop=threading.Event();errors=[];samples=[];child=None
def watch():
 while not stop.is_set():
  try:
   members={}
   for root in owners:
    try:
     for q in [root]+root.children(recursive=True):
      try:members[(q.pid,q.create_time())]=q.memory_info().rss
      except psutil.NoSuchProcess:pass
    except psutil.NoSuchProcess:pass
   total=sum(members.values())
   samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total,
    processes=[dict(pid=k[0],birth=k[1],rss_bytes=v)for k,v in members.items()]))
   if total>48*1024**3:
    errors.append('combined48GiBpressure; terminate only new import preparation')
    if child and child.poll()is None:os.killpg(child.pid,signal.SIGKILL)
    return
  except Exception as e:
   errors.append(repr(e))
   if child and child.poll()is None:
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   return
  stop.wait(1)
thread=threading.Thread(target=watch,daemon=True)
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,cwd=str(project),
 inherited_context_reference=dict(pid=reference.pid,birth=reference.create_time()),
 context={k:env.get(k)for k in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT']},
 source_id=source['id'],scope='Prepare only parsed imports from original full source; never connect branch socket or execute candidate commands.',
 native_candidate_executions=0,RLIMIT_AS=None,aggregate_budget_bytes=48*1024**3)
try:
 with(a/'stderr.log').open('wb')as stderr:
  child=subprocess.Popen(cmd,cwd=project,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
   stderr=stderr,text=True,start_new_session=True)
  receipt['parent_pid']=child.pid;receipt['parent_birth']=psutil.Process(child.pid).create_time()
  thread.start()
  child.stdin.write(json.dumps(source['code'])+'\n');child.stdin.flush()
  line=child.stdout.readline();receipt['ready_seconds']=time.monotonic()-start
  (a/'stdout.jsonl').write_text(line)
  handshake=json.loads(line)if line else None;receipt['handshake']=handshake
  if handshake:
   parent=psutil.Process(child.pid)
   receipt['observed_parent_threads']=parent.num_threads()
   receipt['observed_parent_children']=[q.pid for q in parent.children(recursive=True)]
   receipt['observed_parent_rss_bytes']=parent.memory_info().rss
   assert handshake['prepared_context']['header_errors']is False
   assert handshake['prepared_context']['imported_modules']>0
   assert parent.num_threads()==1 and not parent.children()
  child.stdin.close()
  tail=child.stdout.read()
  if tail:
   with(a/'stdout.jsonl').open('a')as stream:stream.write(tail)
  code=child.wait();receipt['exit']=code;receipt['retired']=not psutil.pid_exists(child.pid)
  if not handshake or code:raise RuntimeError('actual Mathlib parent preparation failed')
finally:
 if child and child.poll()is None:
  os.killpg(child.pid,signal.SIGKILL);child.wait()
 stop.set()
 if thread.ident:thread.join()
 receipt.update(whole_seconds=time.monotonic()-start,monitor_errors=errors,
  sampled_aggregate_peak_rss_bytes=max((x['rss_bytes']for x in samples),default=None))
 (a/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 (a/'memory-samples.jsonl.gz').write_bytes(gzip.compress(
  ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
 (a/'run-source.py').write_bytes(Path(__file__).read_bytes())
 if socket.exists():socket.unlink()
 work.rmdir()
 print(json.dumps({k:v for k,v in receipt.items()if k!='context'}),flush=True)
