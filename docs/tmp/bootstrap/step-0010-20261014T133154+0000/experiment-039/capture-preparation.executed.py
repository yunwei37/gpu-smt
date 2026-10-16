"""Actual finite E039 HTTP acquisition; reuse existing GC49 native environment."""
from pathlib import Path
import collections,concurrent.futures,datetime,gzip,importlib.util,json,os,resource,subprocess,sys,threading,time
import requests
R=Path('/workspaces/repository');E=Path(__file__).parent
MODE=sys.argv[1];OUT=Path(sys.argv[2]);OUT.mkdir(exist_ok=False)
SOURCE=R/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/proofnet/input.jsonl'
GC=R/'artifacts/lean-native-compilation-2026-10-14/gc49/run-gc49.py'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
spec=importlib.util.spec_from_file_location('e039_existing_gc49',GC);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ITEMS=[json.loads(x) for x in SOURCE.read_text().splitlines()]
assert len(ITEMS)==5952 and len({x['index'] for x in ITEMS})==5952
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def drain(pipe,p):
 with gzip.open(p,'wb',compresslevel=1) as f:
  while b:=pipe.read(65536):f.write(b)
 pipe.close()
def capture(label,items,width):
 O=OUT/label;O.mkdir();start=time.monotonic_ns();rows=[];failure=None
 with gzip.open(O/'input.jsonl.gz','wt',compresslevel=1) as f:
  for x in items:f.write(json.dumps(x,ensure_ascii=False)+'\n')
 env=g.environment('compiled');env.pop('LEAN_SERVER_PORT',None)
 SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
 env['LEAN_SYSROOT']=str(SDK)
 old=R/'artifacts/lean-native-boundary-2026-10-11/experiment012/preflight2/branch-minif2f-first32/receipt.json'
 env['LEAN_PATH']=json.loads(old.read_text())['environment']['LEAN_PATH']
 cmd=[str(K/'.venv/bin/python'),'-u',str(E/'observe-native-service.executed.py'),str(O)]
 proc=subprocess.Popen(cmd,cwd=K,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 dump(O/'command.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'pid':proc.pid,'cwd':str(K),'environment_source':str(GC),'method':'same producer4.9 GC+selective native arithmetic baseline','native_composition':{k:env.get(k) for k in ['LEAN_SERVER_REPL_PATH','LEAN_SERVER_PROJECT_DIR','LEAN_SERVER_NATIVE_DYNLIB','LEAN_SYSROOT','LEAN_PATH','LD_LIBRARY_PATH','LEAN_NUM_THREADS','OMP_NUM_THREADS','FARKAS_USE_FAST','FARKAS_EXTERNAL_CPU_HYBRID']},'affinity':sorted(os.sched_getaffinity(0)),'inflight':width,'timeout':'stock request default, recorded by caller and observer','policy':'existing default maxpool/maxuses/12GiB; no custom memory/thread setting'})
 ts=[threading.Thread(target=drain,args=(pipe,O/name)) for pipe,name in [(proc.stdout,'server.stdout.gz'),(proc.stderr,'server.stderr.gz')]]
 for t in ts:t.start()
 local=threading.local();sessions=[];lock=threading.Lock()
 try:
  ready=O/'server-ready.json'
  while True:
   if proc.poll() is not None:raise RuntimeError('official app exited before ready: '+str(proc.returncode))
   if ready.exists():
    try:
     port=json.loads(ready.read_text())['port'];url='http://127.0.0.1:'+str(port)
     response=requests.get(url+'/api/openapi.json')
     if response.status_code==200:break
    except (ValueError,requests.ConnectionError):pass
   time.sleep(.1)
  def request(ordinal,item):
   if not hasattr(local,'client'):
    local.client=requests.Session()
    with lock:sessions.append(local.client)
   t=time.monotonic_ns()
   answer=local.client.post(url+'/verify',json={'codes':[{'custom_id':'proofnet-'+str(item['index']),'proof':item['code']}],'disable_cache':False})
   ended=time.monotonic_ns()
   try:body=answer.json()
   except ValueError:body=None
   return {'ordinal':ordinal,'source_index':item['index'],'admitted_ns':t,'response_ns':ended,'elapsed_seconds':(ended-t)/1e9,'status_code':answer.status_code,'basic':g.basic(answer.status_code,body),'body_utf8':answer.content.decode('utf-8'),'actual_request':'original code string, stock timeout/reuse'}
  with (gzip.open(O/'http-results.jsonl.gz','wt',compresslevel=1)) as raw,concurrent.futures.ThreadPoolExecutor(max_workers=width) as pool:
   pending={};n=0
   def fill():
    nonlocal n
    while len(pending)<width and n<len(items):
     i=n;n+=1;pending[pool.submit(request,i,items[i])]=i
   fill()
   while pending:
    done,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
    for f in sorted(done,key=lambda x:pending[x]):
     pending.pop(f);row=f.result();raw.write(json.dumps(row,ensure_ascii=False)+'\n');raw.flush();rows.append(row)
    fill()
 except BaseException as e:failure={'type':type(e).__name__,'error':repr(e)}
 finally:
  for s in sessions:s.close()
  if proc.poll() is None:proc.terminate()
  code=proc.wait()
  for t in ts:t.join()
 end=time.monotonic_ns()
 terminal={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'begin_ns':start,'end_ns':end,'whole_seconds':(end-start)/1e9,'server_exit':code,'expected':len(items),'returned':len(rows),'counts':dict(collections.Counter(x['basic'] for x in rows)),'failure':failure,'inflight':width,'whole_boundary':'input persistence/official app start/actual native prep/body/HTTP/phase/raw logging/replacements/stock close kill-wait and drains; no build or synthetic warmup','scope':'complete request-driven preparation characterization, not new-system or GPU speedup'}
 dump(O/'terminal.json',terminal);print('CELL_TERMINAL',json.dumps(terminal),flush=True)
 if failure or len(rows)!=len(items) or code not in (0,-15):raise RuntimeError('invalid/partial acquisition retained: '+label)
 return terminal
if MODE=='preflight':
 selected=[ITEMS[i] for i in [0,1,25]]
 assert selected[-1]['code']=='None'
 results=[capture('preflight',selected,1)]
elif MODE=='full':
 results=[capture('rep'+str(rep),ITEMS,4) for rep in range(3)]
else:raise ValueError('preflight or full')
dump(OUT/'terminal.json',{'state':'complete','cells':len(results),'returned':sum(x['returned'] for x in results),'results':results})
