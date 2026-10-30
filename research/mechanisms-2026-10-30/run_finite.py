"""Finite phobos-vt measurement; one Lean at a time, native limits, no signals."""
from pathlib import Path
import subprocess,os,time,json,argparse,resource
HERE=Path(__file__).resolve().parent
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
CAPTURE_ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures')
BUILD_ROOT=CAPTURE_ROOT.parent/'generated'
ML=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
def rss(pid):
 try:return int(next(l.split()[1] for l in Path(f'/proc/{pid}/status').read_text().splitlines() if l.startswith('VmRSS:')))*1024
 except (OSError,StopIteration):return 0
def run(source,label,wall_seconds=1200,library=None):
 out=CAPTURE_ROOT/label;out.mkdir(parents=True,exist_ok=False)
 (out/'source.lean').write_bytes(source.read_bytes())
 (out/'runner.py').write_bytes(Path(__file__).read_bytes())
 env=os.environ.copy();paths=[ML/'.lake/build/lib']+sorted((ML/'.lake/packages').glob('*/.lake/build/lib'))
 env.update(M_TACTIC_TRACE_FILE=str(out/'tactics.jsonl'),LD_PRELOAD=str(library or (BUILD_ROOT/'software-probe-cpu/software-probe.so')),M_WALL_MILLISECONDS=str(wall_seconds*1000),LEAN_PATH=':'.join(str(p) for p in paths),LEAN_NUM_THREADS='1')
 args=['taskset','-c','8,9,10,11',str(SDK/'bin/lean'),'-j1','-M8192','-T50000000',str(source)]
 began=time.monotonic();receipt={'argv':args,'source':str(source),'hardware_point':'phobos-vt serial M branch, CPU8-11, RSS budget16GiB',
   'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'signals_sent':0,'native_allocation_limit':50000000,'native_memory_MiB':8192,'internal_wall_seconds':wall_seconds,'loaded_measurement_library':env['LD_PRELOAD'],'intended_wall_handler_exit_code':124,'observed_internal_alarm_signal_possible':14}
 (out/'launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
 peak=0;minavail=None;samples=0
 with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr,(out/'memory.jsonl').open('w') as memory:
  child=subprocess.Popen(args,env=env,cwd=ML,stdout=stdout,stderr=stderr)
  receipt['pid']=child.pid;receipt['start_ticks']=Path(f'/proc/{child.pid}/stat').read_text().split()[21]
  (out/'launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
  while child.poll() is None:
   owned=rss(child.pid)+rss(os.getpid());peak=max(peak,owned)
   avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
   minavail=avail if minavail is None else min(minavail,avail)
   memory.write(json.dumps({'elapsed_s':time.monotonic()-began,'owned_rss_bytes':owned,'node_MemAvailable_bytes':avail})+'\n');memory.flush();samples+=1
   try:child.wait(timeout=1)
   except subprocess.TimeoutExpired:pass
  code=child.wait()
 usage=resource.getrusage(resource.RUSAGE_CHILDREN)
 receipt.update(native_kernel_peak_rss_bytes=usage.ru_maxrss*1024,native_cpu_seconds=usage.ru_utime+usage.ru_stime,exit=code,wall_s=time.monotonic()-began,sampled_peak_owned_rss_bytes=peak,
  minimum_node_MemAvailable_bytes=minavail,samples=samples,sample_interval_s=1,
  retired=not Path(f'/proc/{child.pid}').exists())
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);return code
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('label');p.add_argument('--wall-seconds',type=int,default=1200);p.add_argument('--library',type=Path);a=p.parse_args()
 raise SystemExit(run(a.source.resolve(),a.label,a.wall_seconds,a.library))
