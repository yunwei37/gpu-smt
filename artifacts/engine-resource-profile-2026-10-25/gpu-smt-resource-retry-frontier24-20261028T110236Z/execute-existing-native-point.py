
import pathlib,json,datetime,os,subprocess,time,resource,importlib.util
out=pathlib.Path(__file__).parent
q=pathlib.Path(json.loads((out/'manifest.json').read_text())['reference_qualification'])
manifest=json.loads((out/'manifest.json').read_text())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def live(pid,birth):
 try:
  t=pathlib.Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()
  return int(t[19])==birth and t[0]!='Z'
 except FileNotFoundError:return False
prior=json.loads((q/'engine-launch.json').read_text())
assert not live(prior['pid'],prior['start_ticks'])
assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
os.sched_setaffinity(0,{8,9,10,11})
ctx=json.loads((q/'warm/terminal.json').read_text())['source_context']
spec=importlib.util.spec_from_file_location('existing_warm_context',q/'warm-run.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
library_environment=mod.native_library_environment(ctx)
assert library_environment['LEAN_SERVER_NATIVE_DYNLIB']==manifest['native_library']
env=dict(os.environ,LEAN_SYSROOT=ctx['sysroot'],LEAN_PATH=ctx['LEAN_PATH'],
 PATH=ctx['sysroot']+'/bin:'+os.environ['PATH'],**library_environment)
started=time.monotonic()
with(out/'engine.stdout').open('wb')as dest,(out/'engine.stderr').open('wb')as err,(out/'input24.json').open('rb')as src:
 child=subprocess.Popen(manifest['command'],cwd=ctx['project'],env=env,stdin=src,stdout=dest,stderr=err,start_new_session=True)
 launch={'utc':now(),'pid':child.pid,'start_ticks':int(pathlib.Path('/proc',str(child.pid),'stat').read_text().rsplit(')',1)[1].split()[19]),'command':manifest['command']}
 (out/'engine-launch.json').write_text(json.dumps(launch,indent=2)+'\n')
 rc=child.wait()
elapsed=time.monotonic()-started
(out/'engine-exit.json').write_text(json.dumps({'utc':now(),'exit':rc,'external_seconds':elapsed,'scope':'launch through capture serialization,retirement and program exit'},indent=2)+'\n')
if rc:raise RuntimeError('Native benchmark exits nonzero;preserve raw capture')
cap=json.loads((out/'engine.stdout').read_text())
assert cap['batch']==json.loads((out/'input24.json').read_text())and len(cap['results'])==24
survivors=[]
for row in cap['results']:
 for attempt in row['attempts']:
  for p in attempt['processes']:
   if live(p['pid'],p['start_ticks']):survivors.append(p)
assert not survivors,survivors
(out/'terminal.json').write_text(json.dumps({'utc':now(),'state':'retry-frontier24-complete','returned':24,'native_survivors':survivors,'external_seconds':elapsed,'gain_claim':False,'next':'root compare all outcomes and completecosts'},indent=2)+'\n')
print(json.dumps({'state':'retry-frontier24-complete','external_seconds':elapsed}),flush=True)
