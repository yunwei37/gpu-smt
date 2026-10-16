from pathlib import Path
import subprocess,json,datetime,os
E=Path(__file__).resolve().parent
P=Path('/tmp/gpu-smt-native-cpu-perf-20261015');P.mkdir(exist_ok=True)
record=dict(observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=[])
def run(args,env=None):
    c=subprocess.run(args,cwd=P,env=env,text=True,capture_output=True)
    record['steps'].append(dict(command=args,returncode=c.returncode,stdout=c.stdout,stderr=c.stderr))
    (E/'perf-setup.json').write_text(json.dumps(record,indent=2)+chr(10))
    return c
c=run(['apt-get','download','linux-perf=6.12.111-1'])
if c.returncode:raise SystemExit(c.returncode)
pkg=next(P.glob('linux-perf_6.12.111-1_amd64.deb'))
c=run(['dpkg-deb','-x',str(pkg),str(P/'runtime')])
if c.returncode:raise SystemExit(c.returncode)
perf=P/'runtime/usr/bin/perf'
c=run(['ldd',str(perf)])
print('EXTRACTED_PERF',perf,'LDD',c.stdout)
