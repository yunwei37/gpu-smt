"""Read-only hardware/native-module inventory. No verifier is launched."""
from pathlib import Path
import ctypes,os,platform,json,shutil
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'hardware'
def main():
 OUT.mkdir(exist_ok=True)
 cpu=Path('/proc/cpuinfo').read_text()
 (OUT/'cpuinfo.txt').write_text(cpu)
 (OUT/'meminfo.txt').write_text(Path('/proc/meminfo').read_text())
 class Attr(ctypes.Structure):
  _fields_=[('type',ctypes.c_uint32),('size',ctypes.c_uint32),('config',ctypes.c_uint64),('sample',ctypes.c_uint64),('sample_type',ctypes.c_uint64),('read_format',ctypes.c_uint64),('flags',ctypes.c_uint64)]
 libc=ctypes.CDLL(None,use_errno=True);events=[]
 for typ,config,name in [(0,0,'hardware-cycles'),(1,0,'software-cpu-clock')]:
  a=Attr();a.type=typ;a.size=ctypes.sizeof(a);a.config=config;a.flags=(1<<5)|(1<<6)
  ctypes.set_errno(0);fd=libc.syscall(298,ctypes.byref(a),0,-1,-1,0)
  events.append({'event':name,'fd':fd,'errno':ctypes.get_errno()})
  if fd>=0:os.close(fd)
 ml=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
 lib=ml/'.lake/build/lib';so=list(lib.glob('*.so'));olean=list((lib/'Mathlib').rglob('*.olean'))
 native={p.name.removeprefix('lib').removesuffix('-1.so') for p in so}
 rows=[]
 for p in sorted((lib/'Mathlib/Tactic').rglob('*.olean')):
  module='-'.join(p.relative_to(lib).with_suffix('').parts)
  rows.append({'module':module.replace('-','.'),'olean_bytes':p.stat().st_size,
    'matching_flat_shared_library_present':module in native})
 data={'kernel':platform.platform(),'cpu_model':next(x.split(':',1)[1].strip() for x in cpu.splitlines() if x.startswith('model name')),
  'eligible_cpus':sorted(os.sched_getaffinity(0)),'perf_executable':shutil.which('perf'),
  'perf_event_paranoid':Path('/proc/sys/kernel/perf_event_paranoid').read_text().strip(),
  'perf_event_open':events,'mathlib_olean_modules':len(olean),'shared_library_files':len(so),
  'shared_library_bytes':sum(p.stat().st_size for p in so),'tactic_modules':len(rows),
  'tactic_modules_with_matching_so':sum(x['matching_flat_shared_library_present'] for x in rows),
  'module_rows':rows,'important_scope':'Presence is not proof of loading, native execution or cycle cost. No permissions changed.'}
 (OUT/'inventory.json').write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:v for k,v in data.items() if k!='module_rows'},indent=2))
if __name__=='__main__':main()
