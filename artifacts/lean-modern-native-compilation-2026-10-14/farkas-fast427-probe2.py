from pathlib import Path
import types,os,json
D=Path(__file__).parent;U=Path('/tmp/gpu-smt-farkas-fast427-20261014')
source=(D/'run-highs-native-cpu.py').read_text().replace('8004','8007')
m=types.ModuleType('fast427ProbeCapture');m.__file__=str(D/'farkas-fast427-probe.py')
exec(compile(source,str(D/'run-highs-native-cpu.py'),'exec'),m.__dict__)
base=m.environment
def environment(method):
 solver='highs' if method.endswith('highs') else 'tiered'
 env=base(solver)
 env['LEAN_SERVER_PROJECT_DIR']=str(U/'mathlib4')
 build=U/'farkas427'
 paths=[str(build/'.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (build/'.lake/packages').iterdir() if p.is_dir()]
 env['LEAN_PATH']=os.pathsep.join(paths+([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
 env.pop('FARKAS_USE_FAST',None)
 if method.startswith('fast'):env['FARKAS_USE_FAST']='1'
 return env
m.m.environment=environment
if __name__=='__main__':
 m.m.resource.setrlimit(m.m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{16,17,18,19})
 out=D/'farkas-fast427-probe2';out.mkdir()
 for method in ['full-tiered','fast-tiered','full-highs','fast-highs']:
  m.capture(out,method,method,'preflight',True)
