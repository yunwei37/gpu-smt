from pathlib import Path
import importlib.util,sys,os,json,datetime
r=Path('/workspaces/repository');source=r/'artifacts/lean-gpu-checking-2026-10-13/experiment022'
sys.path.insert(0,str(source))
spec=importlib.util.spec_from_file_location('original_acquisition',source/'run-native6.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=Path(__file__).parent;m.BASE=d
m.inputs=lambda dataset,preflight:r/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs'/dataset
binaries={'original-warm':r/'artifacts/lean-service-lifecycle-2026-10-13/build1/Lean49PreparedBranches','closed-cache':d/'build/Lean49ClosedModeCache'}
os.sched_setaffinity(0,{0,1,2,3})
out=d/'full1-proofnet';out.mkdir(exist_ok=False)
for rep,order in enumerate([('original-warm','closed-cache'),('closed-cache','original-warm'),('original-warm','closed-cache')]):
 for name in order:
  m.STOCK=binaries[name]
  code=m.capture(out,f'proofnet-rep{rep}-{name}','proofnet','warm',4)
  if code:raise RuntimeError('original acquisition failed; partial retained')
for name in ['closed-cache','original-warm']:
 m.STOCK=binaries[name]
 code=m.capture(out,f'proofnet-profile-{name}','proofnet','warm',4,profile=True)
 if code:raise RuntimeError('original profile acquisition failed; partial retained')
(out/'complete-matrix.md').write_text('All8 planned complete cells acquired; actual metric/basic/engagement review remains required. No automatic promotion.\n')
