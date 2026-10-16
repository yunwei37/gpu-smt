from pathlib import Path
import importlib.util, os, resource
p=Path(__file__).parent
spec=importlib.util.spec_from_file_location('repaired',p/'run-gc-repaired-header.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original_environment=m.environment
def environment(method):
 env=original_environment(method);env['LEAN_SERVER_PROJECT_DIR']='/tmp/gpu-smt-header-missing-mathlib-20261014'
 return env
m.environment=environment
resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{8,9,10,11})
out=p/'missing-header-control2';out.mkdir()
m.capture(out,'original','preflight','original')
