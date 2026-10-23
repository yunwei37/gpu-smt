from pathlib import Path
import asyncio,json,os,resource,runpy,sys,datetime
from types import SimpleNamespace
R=Path('/workspaces/repository');O=R/'artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
os.environ['GPU_SMT_MEMORY_ROOT_PID']=str(os.getpid())
sys.path[:0]=[str(K),str(K/'client')]
capture=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/kimina-http.py'))
original=Path('/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build')
version=2
diagnostic=Path('/tmp/gpu-smt-native-stage-profile-20261022'+('' if version==1 else '-v'+str(version)))
reject_only=len(sys.argv)>2 and sys.argv[2]=='rejected'
full=len(sys.argv)>2 and sys.argv[2]=='full'
items=[json.loads(l) for l in (R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl').open()]
if reject_only:
 rejected={'Proof_00710','Proof_12175','Proof_15022','Proof_15224','Proof_16530','Proof_17093','Proof_20359','Proof_25649'}
 items=[x for x in items if x['proof_id'] in rejected]
 assert len(items)==8
elif full:
 assert len(items)==1000
else:
 items=items[:24]
 assert len(items)==24
args=SimpleNamespace(kimina=K,build=original,build_source=R/'bench/lean-native/linarith-oracle/reproduction',
 repl=Path('/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl'),
 reference=R/'artifacts/lean-modern-native-compilation-2026-10-14/farkas-external-support',
 support_python=Path('/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python'),
 native_engine='hybrid',concurrency=2,total_memory_gib=48,per_repl_gib=24,
 watchdog_test_threshold_bytes=0,skip_warm=False,cost_timing=False)
args.reference_diagnostic=False;args.reference_phases=False;args.cost_timing=False
args.build_source=R/'bench/lean-native/linarith-oracle'
args.build=Path('/tmp/gpu-smt-current-budget-gpu-20261023')
args.device_min_rows=38
args.gpu_host=sys.argv[1]if len(sys.argv)>1 else None
selected=[json.loads(l)for l in (R/'artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl').open()]
async def main():
 methods=['gpu']if args.gpu_host else ['power','native']
 results=[]
 for method in methods:
  print(json.dumps(dict(event="cell_start",method=method,sources=len(selected),pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())),flush=True)
  terminal=await capture['cell'](args,method,O/('full1000-'+method),selected,json.loads((args.build/'build.json').read_text()))
  results.append(dict(method=method,terminal=terminal))
  assert terminal['state']=='complete'and terminal['returned']==len(selected)
  assert not terminal['memory_watchdog']['error']and not terminal['owned_live_descendants_after_shutdown']
 (O/('full1000-gpu-terminal-summary.json'if args.gpu_host else'full1000-cpu-terminal-summary.json')).write_text(json.dumps(results,indent=2)+'\n')
asyncio.run(main())
