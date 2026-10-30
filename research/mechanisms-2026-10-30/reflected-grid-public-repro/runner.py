"""Finite phobos-vt measurement; one Lean at a time, native limits, no signals."""
from pathlib import Path
import subprocess,os,time,json,argparse,resource
HERE=Path(__file__).resolve().parent
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
CAPTURE_ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures')
BUILD_ROOT=CAPTURE_ROOT.parent/'generated'
ML=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
def persistent_capture_path(path):
    """Reuse the existing collector's PVC policy before any capture writes."""
    import importlib.util
    import sys
    owner=Path(__file__).resolve().parents[2]/"bench/lean-failure-profile/state-reuse/run.py"
    spec=importlib.util.spec_from_file_location("mechanisms_existing_capture_storage",owner)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module.persistent_output(path)

def rss(pid):
 try:return int(next(l.split()[1] for l in Path(f'/proc/{pid}/status').read_text().splitlines() if l.startswith('VmRSS:')))*1024
 except (OSError,StopIteration):return 0
def owned_tree():
 table={}
 for d in Path('/proc').iterdir():
  if not d.name.isdigit():continue
  try:
   text=(d/'stat').read_text();parts=text[text.rfind(')')+2:].split()
   table[int(d.name)]=(int(parts[1]),parts[19],rss(int(d.name)))
  except (OSError,ValueError,IndexError):continue
 roots={os.getpid()}
 owner=os.environ.get('M_OWNERSHIP_ROOT_PID')
 birth=os.environ.get('M_OWNERSHIP_ROOT_BIRTH')
 if owner and int(owner) in table and table[int(owner)][1]==birth:roots.add(int(owner))
 while True:
  more={pid for pid,(parent,_,_) in table.items() if parent in roots}
  if more<=roots:break
  roots|=more
 return [{'pid':pid,'start_ticks':table[pid][1],'rss_bytes':table[pid][2]} for pid in roots if pid in table]
def run(source,label,wall_seconds=1200,library=None,native_executable=None,embedded_probe=False,input_path=None,jobs=1,cpus="8,9,10,11"):
 out=persistent_capture_path(CAPTURE_ROOT/label);out.mkdir(parents=True,exist_ok=False)
 (out/'source.lean').write_bytes(source.read_bytes())
 (out/'runner.py').write_bytes(Path(__file__).read_bytes())
 env=os.environ.copy();paths=[SDK/'lib/lean',ML/'.lake/build/lib']+sorted((ML/'.lake/packages').glob('*/.lake/build/lib'))
 env.update(LEAN_SYSROOT=str(SDK),M_TACTIC_TRACE_FILE=str(out/'tactics.jsonl'),LD_PRELOAD=str(library or (BUILD_ROOT/'software-probe-cpu/software-probe.so')),M_WALL_MILLISECONDS=str(wall_seconds*1000),LEAN_PATH=':'.join(str(p) for p in paths),LEAN_NUM_THREADS=str(jobs))
 if input_path is not None:env['M_DAG_INPUT']=str(input_path)
 if embedded_probe:env.pop('LD_PRELOAD',None)
 args=['taskset','-c',cpus,str(native_executable or (SDK/'bin/lean')),f'-j{jobs}','-M8192','-T50000000',str(source)]
 usage_before=resource.getrusage(resource.RUSAGE_CHILDREN)
 began=time.monotonic();receipt={'argv':args,'source':str(source),'hardware_point':f'phobos-vt one-native-process M branch, CPU{cpus}, RSS budget16GiB',
   'native_jobs':jobs,'cpu_affinity':cpus,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'signals_sent':0,'native_allocation_limit':50000000,'native_T_flag':50000000,'native_T_semantics':'legacy field records CLI-T value, not a whole-source IO.getNumHeartbeats quota','native_memory_MiB':8192,'native_M_semantics':'Lean cooperative process RSS checks, not allocator-only, RLIMIT_AS or kernel hard quota','internal_wall_seconds':wall_seconds,'loaded_measurement_library':env.get('LD_PRELOAD','embedded probe'),'intended_wall_handler_exit_code':124,'observed_internal_alarm_signal_possible':14}
 (out/'launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
 peak=0;minavail=None;samples=0
 with (out/'stdout.txt').open('w') as stdout,(out/'stderr.txt').open('w') as stderr,(out/'memory.jsonl').open('w') as memory:
  child=subprocess.Popen(args,env=env,cwd=ML,stdout=stdout,stderr=stderr)
  receipt['pid']=child.pid;receipt['start_ticks']=Path(f'/proc/{child.pid}/stat').read_text().split()[21]
  (out/'launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
  while child.poll() is None:
   processes=owned_tree();owned=sum(x['rss_bytes'] for x in processes);peak=max(peak,owned)
   avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
   minavail=avail if minavail is None else min(minavail,avail)
   memory.write(json.dumps({'elapsed_s':time.monotonic()-began,'owned_rss_bytes':owned,'processes':processes,'node_MemAvailable_bytes':avail})+'\n');memory.flush();samples+=1
   try:child.wait(timeout=1)
   except subprocess.TimeoutExpired:pass
  code=child.wait()
 usage=resource.getrusage(resource.RUSAGE_CHILDREN)
 receipt.update(native_kernel_peak_rss_bytes=usage.ru_maxrss*1024,native_cpu_seconds=usage.ru_utime+usage.ru_stime-usage_before.ru_utime-usage_before.ru_stime,native_cpu_scope='RUSAGE_CHILDREN delta for this serial run',native_kernel_peak_rss_scope='RUSAGE_CHILDREN cumulative maximum in controller; not per-run highwater',exit=code,wall_s=time.monotonic()-began,sampled_peak_owned_rss_bytes=peak,
  minimum_node_MemAvailable_bytes=minavail,samples=samples,sample_interval_s=1,
  retired=not Path(f'/proc/{child.pid}').exists())
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt),flush=True);return code
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('label');p.add_argument('--wall-seconds',type=int,default=1200);p.add_argument('--library',type=Path);p.add_argument('--native-executable',type=Path);p.add_argument('--embedded-probe',action='store_true');p.add_argument('--input',type=Path);p.add_argument('--jobs',type=int,default=1);p.add_argument('--cpus',default='8,9,10,11');a=p.parse_args()
 raise SystemExit(run(a.source.resolve(),a.label,a.wall_seconds,a.library,a.native_executable,a.embedded_probe,a.input,a.jobs,a.cpus))
