from pathlib import Path
import subprocess,os,time,datetime,json
r=Path('/workspaces/repository');e=Path(__file__).parent
native=Path('/tmp/gpu-smt-arena-native-stages-20261016/source/target/release/sokonanoda')
source=Path('/tmp/gpu-smt-arena-native-stages-20261016/arena-source/_build/tests/init.ndjson')
lib=Path('/tmp/gpu-smt-reclaiming-native-20261016')
assert source.stat().st_size==347555345
for mode in ['on','off']:
 name='reclaim-'+mode+'-official-init'
 env=dict(os.environ)
 for key in ['GPU_SMT_CANONICAL_OFF','GPU_SMT_RECLAIM_OFF','GPU_SMT_ARENA_TRACE']:env.pop(key,None)
 env['LD_LIBRARY_PATH']=str(lib)+os.pathsep+env.get('LD_LIBRARY_PATH','')
 env['GPU_SMT_ARENA_TRACE']=str(e/(name+'.csv'))
 if mode=='off':env['GPU_SMT_RECLAIM_OFF']='1'
 cmd=['/usr/bin/time','-v','-o',str(e/(name+'.resources.txt')),str(native),
      '--stdin','--nat-extension','--string-extension','--axiom-allow-all',
      '--threads','4','--print-success-message']
 launch={'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'command':cmd,'cwd':str(r),'input':str(source),'input_bytes':source.stat().st_size,
  'environment_overrides':{'LD_LIBRARY_PATH':env['LD_LIBRARY_PATH'],
    'GPU_SMT_ARENA_TRACE':env['GPU_SMT_ARENA_TRACE'],
    'GPU_SMT_RECLAIM_OFF':env.get('GPU_SMT_RECLAIM_OFF')},
  'scope':'E040 complete official Init host setup, all native checks retained; no GPU or replacement verdict'}
 (e/(name+'.launch.json')).write_text(json.dumps(launch,indent=2)+'\n')
 t=time.monotonic()
 with source.open('rb') as inp,(e/(name+'.stdout')).open('wb') as out,(e/(name+'.stderr')).open('wb') as err:
  proc=subprocess.Popen(cmd,cwd=r,env=env,stdin=inp,stdout=out,stderr=err)
  (e/(name+'.pid.json')).write_text(json.dumps({'pid':proc.pid})+'\n')
  code=proc.wait()
 v={**launch,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'exit':code,'whole_seconds':time.monotonic()-t}
 (e/(name+'.terminal.json')).write_text(json.dumps(v,indent=2)+'\n')
 print(json.dumps(v),flush=True)
 if code:raise RuntimeError('complete native execution failed; raw retained '+name)
(e/'host-acquisition-completed.md').write_text('Both complete official Init host observations terminal; setup only, root result/self-review pending, no GPU/main-matrix/independent-review completion.\n')
