from pathlib import Path
import os,sys,json,time,subprocess,threading,gzip,requests,signal,resource,zipfile,shutil,datetime,collections,concurrent.futures
R=Path('/workspaces/repository');D=Path(__file__).parent
B=Path('/tmp/gpu-smt-kimina-header-repair-20261014')
T=Path('/tmp/gpu-smt-goedel427-20261014');SDK=T/'lean-4.27.0-linux'
sys.path.insert(0,str(R/'artifacts/lean-gpu-checking-2026-10-13/experiment022/source1'))
from lean_capture_warm import ResourceCapture
def environment(method):
 env=dict(os.environ);env['PATH']=str(SDK/'bin')+os.pathsep+env['PATH']
 env.update(LEAN_SERVER_LEAN_VERSION='v4.27.0',LEAN_SERVER_REPL_PATH=str(T/'repl-kimina-gc-header-repair/.lake/build/bin/repl'),LEAN_SERVER_PROJECT_DIR=str(T/'mathlib4'))
 env.update(LEAN_SERVER_PORT='8002',LEAN_SERVER_HOST='127.0.0.1')
 env.pop('LEAN_SERVER_NATIVE_DYNLIB',None)
 if method=='compiled':
  config=json.loads((D/'native-library.json').read_text())
  env['LEAN_SERVER_REPL_PATH']=str(T/'repl-kimina-native-gc-header-repair/.lake/build/bin/repl')
  env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest']
  env['LD_LIBRARY_PATH']=os.pathsep.join(config['library_paths']+([env['LD_LIBRARY_PATH']] if env.get('LD_LIBRARY_PATH') else []))
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
 source=D/('preflight-gc-input.jsonl' if ds=='preflight' else 'input.jsonl')
 started=time.monotonic_ns();(folder/'input.jsonl').write_bytes(source.read_bytes())
 inputs=[json.loads(x) for x in source.read_text().splitlines()]
 observer=ResourceCapture(folder) if profile else None;stop=threading.Event()
 def observe():
  while not stop.wait(1):observer.sample()
 monitor=threading.Thread(target=observe) if observer else None
 if monitor:monitor.start()
 command=[str(B/'.venv/bin/python'),'-m','server']
 proc=subprocess.Popen(command,cwd=B,env=environment(method),stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 (folder/'command.json').write_text(json.dumps({'command':command,'pid':proc.pid,'cwd':str(B),'backend':'Docker-declared Kimina GC fork ported to producer4.27; native-load only compiled; Python stock defaults','method':method,'affinity':sorted(os.sched_getaffinity(0)),'stock_defaults':'12GiBaddressspace/maxpool23/maxuses-1/legacy300s; originalCORE0 inherited','api':'/verify, four requests in flight, privatePort8002'},indent=2)+'\n')
 drains=[threading.Thread(target=drain,args=(pipe,folder/name)) for pipe,name in [(proc.stdout,'server.stdout.gz'),(proc.stderr,'server.stderr.gz')]]
 for t in drains:t.start()
 session=requests.Session();rows=[];ready=False;failure=None
 try:
  while not ready:
   if proc.poll() is not None:raise RuntimeError('stock server terminated before readiness')
   try:ready=session.get('http://127.0.0.1:8002/api/openapi.json').status_code==200
   except requests.ConnectionError:time.sleep(.1)
  local=threading.local();sessions=[];session_lock=threading.Lock()
  def request(ordinal,item):
   if not hasattr(local,'session'):
    local.session=requests.Session()
    with session_lock:sessions.append(local.session)
   before=time.monotonic_ns()
   try:
    response=local.session.post('http://127.0.0.1:8002/verify',json={'codes':[{'custom_id':item['proof_id'],'proof':item['code']}],'disable_cache':False})
    after=time.monotonic_ns()
    (folder/'responses'/f'{ordinal:08d}.json').write_bytes(response.content)
    try:body=response.json()
    except ValueError:body=None
    row={'source_index':item['index'],'proof_id':item['proof_id'],'ordinal':ordinal,'published_status':item['author']['status'],'status_code':response.status_code,'basic':basic(response.status_code,body),'admitted_ns':before,'response_ns':after,'elapsed_seconds':(after-before)/1e9,'raw_response':f'responses/{ordinal:08d}.json'}
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
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{8,9,10,11})
 action=sys.argv[1]
 if action=='preflight':
  selected=[]
  for line in (D/'input.jsonl').read_text().splitlines():
   row=json.loads(line)
   if row['proof_id'] in ['Proof_00000', 'Proof_00004']:selected.append(row)
  assert len(selected)==2
  (D/'preflight-gc-input.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected))
  out=D/'preflight-gc3';out.mkdir()
  for method in ['original','compiled']:capture(out,method,'preflight',method)
 elif action=='full':
  out=D/'full-gc2';out.mkdir()
  ds='goedel427'
  for rep,order in enumerate([('original','compiled'),('compiled','original'),('original','compiled')]):
   pair={}
   for method in order:pair[method]=capture(out,f'{ds}-rep{rep}-{method}',ds,method)
   differences=[i for i in pair['original'] if pair['original'][i]!=pair['compiled'].get(i)]
   (out/(ds+f'-rep{rep}-basic-differences.json')).write_text(json.dumps(differences)+'\n')
  for method in ['original','compiled']:capture(out,ds+'-profile-'+method,ds,method,True)
  (out/'acquisition-completed.md').write_text('All8modern conditions returned. Complete result review required; no automatic contribution/RQ promotion.\n')
 else:raise ValueError('preflight or full only')
if __name__=='__main__':main()
