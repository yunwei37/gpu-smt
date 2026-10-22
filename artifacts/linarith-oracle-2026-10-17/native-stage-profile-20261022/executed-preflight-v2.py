from pathlib import Path
import asyncio,json,os,resource,runpy,sys,datetime
from types import SimpleNamespace
R=Path('/workspaces/repository');O=R/'artifacts/linarith-oracle-2026-10-17/native-stage-profile-20261022'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ['GPU_SMT_MEMORY_ROOT_PID']=str(os.getpid())
sys.path[:0]=[str(K),str(K/'client')]
capture=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/kimina-http.py'))
original=Path('/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build')
version=int(sys.argv[1]) if len(sys.argv)>1 else 1
diagnostic=Path('/tmp/gpu-smt-native-stage-profile-20261022'+('' if version==1 else '-v'+str(version)))
items=[json.loads(l) for l in (R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl').open()][:24]
assert len(items)==24
args=SimpleNamespace(kimina=K,build=original,build_source=R/'bench/lean-native/linarith-oracle/reproduction',
 repl=Path('/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl'),
 reference=R/'artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support',
 support_python=Path('/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python'),
 native_engine='hybrid',concurrency=2,total_memory_gib=48,per_repl_gib=24,
 watchdog_test_threshold_bytes=0,skip_warm=False,cost_timing=False)
async def main():
 results=[]
 cases=[('frozen',original,False),('diagnostic-off',diagnostic,False),('diagnostic-on',diagnostic,True)] if version==1 else [('diagnostic-on-v'+str(version),diagnostic,True)]
 for label,build,enabled in cases:
  args.build=build;args.cost_timing=enabled
  print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':'cell_start','label':label}),flush=True)
  terminal=await capture['cell'](args,'native',O/label,items,json.loads((build/'build.json').read_text()))
  results.append(dict(label=label,terminal=terminal))
  print(json.dumps({'event':'cell_complete','label':label,'terminal':terminal}),flush=True)
  assert terminal['state']=='complete' and terminal['returned']==24
  assert not terminal['owned_live_descendants_after_shutdown'] and not terminal['memory_watchdog']['error']
 (O/('preflight-terminals'+('' if version==1 else '-v'+str(version))+'.json')).write_text(json.dumps(results,indent=2)+'\n')
asyncio.run(main())
