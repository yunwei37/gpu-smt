"""Own method off/observation qualification, identical real candidates."""
from pathlib import Path
from types import SimpleNamespace
import asyncio,gzip,json,os,resource,runpy,sys,time
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path[:0]=[str(K),str(K/'client')]
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ['GPU_SMT_MEMORY_ROOT_PID']=str(os.getpid())
receipt=json.loads((A/'build.json').read_text());B=Path(receipt['build']);SDK=Path(receipt['sdk']);M=SDK.parent/'mathlib4'
paths=[str(M/'.lake/build/lib')]+[str(p/'.lake/build/lib')for p in (M/'.lake/packages').iterdir()if p.is_dir()]
build=dict(sdk=str(SDK),mathlib=str(M),lean_path=receipt['lean_path'],
 lean_src_path=':'.join([str(B),str(M)]+[str(p)for p in (M/'.lake/packages').iterdir()if p.is_dir()]),
 library_paths=[str(B)]+paths,native_library=str(B/'libCounterexample.so'))
args=SimpleNamespace(kimina=K,build=B,repl=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel/.lake/build/bin/repl'),
 reference=R/'artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support',
 concurrency=2,total_memory_gib=48,per_repl_gib=24,watchdog_test_threshold_bytes=0,skip_warm=False,cost_timing=False)
capture=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/kimina-http.py'))
items=[json.loads(l)for l in (A/'preparation32/prepared.jsonl').open()]
async def main():
 summary=[]
 for mode in ['off','observe']:
  out=A/('qualification32v3-'+mode)
  os.environ.update(GPU_SMT_CEX_MODE=mode,GPU_SMT_CEX_WORKER=str(R/'bench/lean-counterexample/worker.py'),GPU_SMT_CEX_LOG=str(out/'goals.jsonl'))
  print(json.dumps(dict(event='own_mode_start',mode=mode,sources=len(items),pid=os.getpid())),flush=True)
  terminal=await capture['cell'](args,'stock',out,items,build)
  terminal.update(own_method_mode=mode,scope='Own counterexample hook off/observation only; no new competitor integration; real originalfirst32; root self-review.')
  (out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
  assert terminal['state']=='complete'and terminal['returned']==len(items)
  assert not terminal['memory_watchdog']['error']and not terminal['owned_live_descendants_after_shutdown']
  summary.append(terminal)
 (A/'qualification32v3-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
