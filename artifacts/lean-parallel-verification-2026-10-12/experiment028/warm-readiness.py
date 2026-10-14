from pathlib import Path
import importlib.util,sys,os,json
r=Path('/workspaces/repository')
source=r/'artifacts/lean-gpu-checking-2026-10-13/experiment022'
sys.path.insert(0,str(source))
spec=importlib.util.spec_from_file_location('original_acquisition',source/'run-native6.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=Path(__file__).parent
original_inputs=m.inputs
m.BASE=d
m.inputs=original_inputs
# Restore its source-relative preflight selection while changing only output ownership.
m.inputs=lambda dataset,preflight: source.parent/'experiment021/inputs/preflight3'/dataset if preflight else r/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs'/dataset
m.STOCK=d/'build/Lean49ClosedModeCache'
os.sched_setaffinity(0,{0,1,2,3})
out=d/'warm-readiness';out.mkdir(exist_ok=False)
raise SystemExit(m.capture(out,'proofnet-cache-warm-ready','proofnet','warm',4,preflight=True))
