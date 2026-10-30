"""Run one finite Lean source at a time; rely on Lean heartbeat/memory limits, never signals."""
from pathlib import Path
import subprocess,os,time,json,argparse
HERE=Path(__file__).resolve().parent
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
ML=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
def run(source,label):
 out=HERE/'native'/label;out.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy();paths=[ML/'.lake/build/lib']
 paths += sorted((ML/'.lake/packages').glob('*/.lake/build/lib'))
 env.update(LEAN_PATH=':'.join(str(p) for p in paths),LEAN_NUM_THREADS='1')
 args=['taskset','-c','4,5',str(SDK/'bin/lean'),'-j1','-M4096','-T20000000',str(source)]
 began=time.monotonic()
 with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr:
  child=subprocess.Popen(args,env=env,cwd=ML,stdout=stdout,stderr=stderr)
  samples=[];peak=0
  while child.poll() is None:
   try:
    status=Path(f'/proc/{child.pid}/status').read_text().splitlines()
    rss=int(next(l.split()[1] for l in status if l.startswith('VmRSS:')))*1024
    peak=max(peak,rss)
    available=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
    samples.append([time.monotonic()-began,rss,available])
   except (OSError,StopIteration):pass
   time.sleep(.1)
  code=child.wait()
 receipt={'argv':args,'source':str(source),'exit':code,'wall_s':time.monotonic()-began,
  'sampled_peak_rss_bytes':peak,'rss_sample_interval_s':.1,'samples':samples,
  'native_heartbeats':'maxHeartbeats in source and CLI allocation limit',
  'own_Lean_memory_limit_MiB':4096,'signals_sent':0,'hardware_point':'G10 Ryzen3500U, CPU4-5, serial, branch limit5GiB',
  'retired':not Path(f'/proc/{child.pid}').exists()}
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:v for k,v in receipt.items() if k!='samples'}),flush=True)
 return code
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('label')
 a=p.parse_args();raise SystemExit(run(a.source.resolve(),a.label))
