from pathlib import Path
import subprocess,json,datetime,os,re
E=Path(__file__).resolve().parent;P=Path('/tmp/gpu-smt-native-cpu-perf-20261015')
record=json.loads((E/'perf-setup.json').read_text())
def run(args,env=None):
    c=subprocess.run(args,cwd=P,env=env,text=True,capture_output=True)
    record['steps'].append(dict(command=args,returncode=c.returncode,stdout=c.stdout,stderr=c.stderr))
    (E/'perf-setup.json').write_text(json.dumps(record,indent=2)+chr(10))
    return c
packages=['libopencsd1','libdebuginfod1t64','libdw1t64','libslang2','libbabeltrace1','libtraceevent1']
versions=[]
for package in packages:
    c=run(['apt-cache','policy',package])
    m=re.search(r'Candidate: (\\S+)',c.stdout)
    if not m:raise RuntimeError(package+' unavailable')
    versions.append(package+'='+m.group(1))
c=run(['apt-get','download']+versions)
if c.returncode:raise SystemExit(c.returncode)
for package in packages:
    deb=next(P.glob(package+'_*.deb'))
    c=run(['dpkg-deb','-x',str(deb),str(P/'runtime')])
    if c.returncode:raise SystemExit(c.returncode)
env=dict(os.environ);env['LD_LIBRARY_PATH']=str(P/'runtime/usr/lib/x86_64-linux-gnu')+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
perf=P/'runtime/usr/bin/perf'
c=run(['ldd',str(perf)],env)
print('LINKAGE',c.stdout,flush=True)
if 'not found' in c.stdout:raise SystemExit('actual remaining dependencies recorded')
c=run([str(perf),'version','--build-options'],env)
print('PERF_VERSION',c.returncode,c.stdout[:1800],c.stderr,flush=True)
lean='/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux/bin/lean'
c=run([str(perf),'stat','-e','cpu-clock:u','--',lean,'--version'],env)
record['dependency_only_availability_probe']=dict(returncode=c.returncode,stdout=c.stdout,stderr=c.stderr)
(E/'perf-setup.json').write_text(json.dumps(record,indent=2)+chr(10))
print('CAPABILITY_PROBE',c.returncode,c.stdout,c.stderr,flush=True)
