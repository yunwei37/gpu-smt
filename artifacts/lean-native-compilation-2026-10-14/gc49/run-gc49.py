from pathlib import Path
import os,sys,json,time,subprocess,threading,gzip,requests,signal,resource,zipfile,shutil,datetime,collections,concurrent.futures
R=Path('/workspaces/repository');D=Path(__file__).parent
B=Path('/tmp/gpu-smt-kimina-header-repair-20261014')
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
sys.path.insert(0,str(R/'artifacts/lean-gpu-checking-2026-10-13/experiment022/source1'))
from lean_capture_warm import ResourceCapture
def environment(method):
 env=dict(os.environ);env['PATH']=str(SDK/'bin')+os.pathsep+env['PATH']
 env.update(LEAN_SERVER_LEAN_VERSION='v4.9.0-rc1',LEAN_SERVER_REPL_PATH='/tmp/gpu-smt-kimina-gc49-20261015/.lake/build/bin/repl',LEAN_SERVER_PROJECT_DIR=str(SDK.parent/'mathlib4'))
 env.update(LEAN_SERVER_PORT='8003',LEAN_SERVER_HOST='127.0.0.1')
 env.pop('LEAN_SERVER_NATIVE_DYNLIB',None)
 if method=='compiled':
  native=Path('/tmp/gpu-smt-native-mathlib-20261014')
  env['LEAN_SERVER_NATIVE_DYNLIB']=str(native/'.lake/build/lib/libMathlib-Tactic-Linarith-1.so')
  paths=[str(native/'.lake/build/lib')]+[str(p/'.lake/build/lib')for p in(native/'.lake/packages').iterdir()if p.is_dir()]
  env['LD_LIBRARY_PATH']=os.pathsep.join(paths+([env['LD_LIBRARY_PATH']]if env.get('LD_LIBRARY_PATH')else[]))
 return env
def drain(pipe,target):
 with gzip.open(target,'xb') as dst:
  while True:
   data=pipe.read(65536)
   if not data:break
   dst.write(data)
 pipe.close()
def basic(status,body):
 if status!=200:return 'operational'
 try:frame=body['results'][0]
 except (KeyError,IndexError,TypeError):return 'operational'
 if frame.get('error'):return 'operational'
 native=frame.get('response')
 if not isinstance(native,dict) or native.get('error'):return 'operational'
 ms=native.get('messages') or []
 if any(m.get('severity')=='error' for m in ms):return 'rejected'
 if native.get('sorries') or any(m.get('severity')=='warning' and ('declaration uses' in m.get('data','') and 'sorry' in m.get('data','') or 'failed' in m.get('data','')) for m in ms):return 'incomplete'
 return 'complete'
def archive(folder):
 target=folder.with_suffix('.zip')
 with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as z:
  for p in folder.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(folder.parent))
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for p in folder.rglob('*'):
   if p.is_file():assert z.read(str(p.relative_to(folder.parent)))==p.read_bytes()
 assert folder.resolve().is_relative_to(D.resolve())
 shutil.rmtree(folder)
def capture(out,label,ds,method,profile=False):
 folder=out/label;folder.mkdir();(folder/'responses').mkdir()
 source=D/'input.jsonl'
 started=time.monotonic_ns();(folder/'input.jsonl').write_bytes(source.read_bytes())
 inputs=[json.loads(x) for x in source.read_text().splitlines()]
 observer=ResourceCapture(folder) if profile else None;stop=threading.Event()
 def observe():
  while not stop.wait(1):observer.sample()
 monitor=threading.Thread(target=observe) if observer else None
 if monitor:monitor.start()
 command=[str(B/'.venv/bin/python'),'-m','server']
 proc=subprocess.Popen(command,cwd=B,env=environment(method),stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 (folder/'command.json').write_text(json.dumps({'command':command,'pid':proc.pid,'cwd':str(B),'backend':'Published Kimina GC path ported to producer4.9; selective native arithmetic only compiled; current Python stock defaults','method':method,'affinity':sorted(os.sched_getaffinity(0)),'stock_defaults':'12GiBaddressspace/maxpool23/maxuses-1/legacy300s; originalCORE0 inherited','api':'/verify, four requests in flight, privatePort8003'},indent=2)+'\n')
 drains=[threading.Thread(target=drain,args=(pipe,folder/name)) for pipe,name in [(proc.stdout,'server.stdout.gz'),(proc.stderr,'server.stderr.gz')]]
 for t in drains:t.start()
 session=requests.Session();rows=[];ready=False;failure=None
 try:
  while not ready:
   if proc.poll() is not None:raise RuntimeError('stock server terminated before readiness')
   try:ready=session.get('http://127.0.0.1:8003/api/openapi.json').status_code==200
   except requests.ConnectionError:time.sleep(.1)
  local=threading.local();sessions=[];session_lock=threading.Lock()
  def request(ordinal,item):
   if not hasattr(local,'session'):
    local.session=requests.Session()
    with session_lock:sessions.append(local.session)
   before=time.monotonic_ns()
   try:
    response=local.session.post('http://127.0.0.1:8003/verify',json={'codes':[{'custom_id':('minif2f-'+str(item['index'])),'proof':item['code']}],'disable_cache':False})
    after=time.monotonic_ns()
    (folder/'responses'/f'{ordinal:08d}.json').write_bytes(response.content)
    try:body=response.json()
    except ValueError:body=None
    row={'source_index':item['index'],'proof_id':('minif2f-'+str(item['index'])),'ordinal':ordinal,'published_status':None,'status_code':response.status_code,'basic':basic(response.status_code,body),'admitted_ns':before,'response_ns':after,'elapsed_seconds':(after-before)/1e9,'raw_response':f'responses/{ordinal:08d}.json'}
    return row
   except BaseException:
    if proc.poll() is not None:raise RuntimeError('stock server terminated during request')
    raise
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   pending={};next_ordinal=0
   def fill():
    nonlocal next_ordinal
    while len(pending)<4 and next_ordinal<len(inputs):
     i=next_ordinal;next_ordinal+=1
     pending[pool.submit(request,i,inputs[i])]=i
   fill()
   with (folder/'results.jsonl').open('a',buffering=1) as results:
    while pending:
     done,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
     for future in sorted(done,key=lambda f:pending[f]):
      pending.pop(future)
      row=future.result();results.write(json.dumps(row)+'\n');rows.append(row)
      if len(rows)%256==0:print(json.dumps({'cell':label,'returned':len(rows),'expected':len(inputs)}),flush=True)
     fill()
  for client in sessions:client.close()
 except BaseException as e:
  failure={'type':type(e).__name__,'error':str(e)}
 finally:
  session.close()
  if proc.poll() is None:proc.terminate()
  server_code=proc.wait()
  for t in drains:t.join()
  if monitor:stop.set();monitor.join();observer.close()
 ended=time.monotonic_ns()
 terminal={'label':label,'dataset':ds,'method':method,'profile':profile,'begin_ns':started,'end_ns':ended,'whole_seconds':(ended-started)/1e9,'returned':len(rows),'expected':len(inputs),'failure':failure,'server_returncode':server_code,'counts':dict(collections.Counter(r['basic'] for r in rows)),'whole_boundary':'input persistence/serverstartup/import/preparation/nativeverification/HTTP/logging/rawcapture/replacement/shutdown/EOF, live gzip captureCPU included; ZIP after clock'}
 (out/(label+'.terminal.json')).write_text(json.dumps(terminal,indent=2)+'\n')
 print(json.dumps(terminal),flush=True)
 if failure or len(rows)!=len(inputs):raise RuntimeError('partial acquisition preserved '+label)
 archive(folder)
 return {r['source_index']:r['basic'] for r in rows}
def main():
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 out=D/'full1';out.mkdir()
 ds='minif2f'
 for rep,order in enumerate([('original','compiled'),('compiled','original'),('original','compiled')]):
  pair={}
  for method in order:pair[method]=capture(out,f'{ds}-rep{rep}-{method}',ds,method)
  differences=[i for i in pair['original']if pair['original'][i]!=pair['compiled'].get(i)]
  (out/(ds+f'-rep{rep}-basic-differences.json')).write_text(json.dumps(differences)+'\n')
 for method in ['original','compiled']:capture(out,ds+'-profile-'+method,ds,method,True)
 (out/'acquisition-completed.md').write_text('All8original mini candidate conditions returned; full source/native/resource result review remainsrequired.\n')
if __name__=='__main__':main()
