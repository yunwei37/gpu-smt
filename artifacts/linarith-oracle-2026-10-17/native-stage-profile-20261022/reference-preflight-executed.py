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
args.reference_diagnostic=False;args.reference_phases=False
helper=Path('/tmp/gpu-smt-native-reference-profile-20261022-v3/farkas-batchd')
positive=items[:24]
rejected={'Proof_00710','Proof_12175','Proof_15022','Proof_15224','Proof_16530','Proof_17093','Proof_20359','Proof_25649'}
allitems=[json.loads(l)for l in (O.parent/'input-top1000.jsonl').open()]
negative=[x for x in allitems if x['proof_id']in rejected]
async def main():
 results=[]
 cases=[('reference-frozen24',original,args.reference,False,False,False,positive),
        ('reference-off24',diagnostic,helper,True,False,False,positive),
        ('reference-on24',diagnostic,helper,True,True,True,positive),
        ('reference-rejected8',diagnostic,helper,True,True,True,negative)]
 for label,build,ref,mode,phases,timing,selected in cases:
  args.build=build;args.reference=ref;args.reference_diagnostic=mode;args.reference_phases=phases;args.cost_timing=timing
  print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':'cell_start','label':label}),flush=True)
  terminal=await capture['cell'](args,'native',O/label,selected,json.loads((build/'build.json').read_text()))
  results.append(dict(label=label,terminal=terminal))
  print(json.dumps({'event':'cell_complete','label':label,'terminal':terminal}),flush=True)
  assert terminal['state']=='complete'and terminal['returned']==len(selected)
  assert not terminal['owned_live_descendants_after_shutdown']and not terminal['memory_watchdog']['error']
 (O/'reference-preflight-terminals.json').write_text(json.dumps(results,indent=2)+'\\n')
asyncio.run(main())
