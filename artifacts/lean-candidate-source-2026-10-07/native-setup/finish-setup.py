import os,time,subprocess,json,hashlib,datetime
from pathlib import Path
b=Path(__file__).parent
while Path('/proc/33568').exists():time.sleep(10)
env=dict(os.environ);env['PATH']=str(b/'lean-4.9.0-rc1-linux/bin')+':'+env['PATH'];env['LEAN_NUM_THREADS']='4';env['XDG_CACHE_HOME']=str(b/'cache')
cmd=['taskset','-c','0-3',str(b/'lean-4.9.0-rc1-linux/bin/lake'),'build','Mathlib','repl']
with (b/'logs/build-native-resume.log').open('wb') as f:r=subprocess.run(cmd,cwd=b/'mathlib4',env=env,stdout=f,stderr=subprocess.STDOUT)
(b/'build-status.json').write_text(json.dumps({'command':cmd,'exitcode':r.returncode,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
if r.returncode:raise SystemExit(r.returncode)
cmd=[str(b/'lean-4.9.0-rc1-linux/bin/lake'),'exe','repl'];request=(b/'transport-stdin.bin').read_bytes();meta={'command':cmd,'cwd':str(b/'mathlib4'),'stdin_sha256':hashlib.sha256(request).hexdigest(),'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':300}
(b/'transport-meta.json').write_text(json.dumps(meta,indent=2))
try:
 r=subprocess.run(cmd,cwd=b/'mathlib4',env=env,input=request,capture_output=True,timeout=300);out,err=r.stdout,r.stderr;meta['returncode']=r.returncode
except subprocess.TimeoutExpired as e:out,err=e.stdout or b'',e.stderr or b'';meta['exception']='TimeoutExpired'
(b/'transport-stdout.bin').write_bytes(out);(b/'transport-stderr.bin').write_bytes(err);meta['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();meta['stdout_sha256']=hashlib.sha256(out).hexdigest();meta['stderr_sha256']=hashlib.sha256(err).hexdigest();(b/'transport-meta.json').write_text(json.dumps(meta,indent=2))
identities={}
for p in [b/'lean-4.9.0-rc1-linux/bin/lean',b/'lean-4.9.0-rc1-linux/bin/lake',b/'mathlib4/.lake/packages/REPL/.lake/build/bin/repl',b/'mathlib4/.lake/build/lib/Mathlib.olean',b/'lake-manifest.upstream.json',b/'lake-manifest.vendor.json']:
 identities[str(p)]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(b/'binary-identities.json').write_text(json.dumps(identities,indent=2));print('SETUP AND TRANSPORT FINISHED',meta,flush=True)
