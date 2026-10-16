from pathlib import Path
import types,os,json
D=Path(__file__).parent;U=Path('/tmp/gpu-smt-farkas-fast427-20261014')
source=(D/'run-highs-native-cpu.py').read_text().replace('8004','8007')
m=types.ModuleType('fast427ProbeCapture');m.__file__=str(D/'farkas-fast427-probe.py')
exec(compile(source,str(D/'run-highs-native-cpu.py'),'exec'),m.__dict__)
base=m.environment
def environment(method):
 solver='highs' if method.endswith('highs') else 'hybrid' if method.endswith('hybrid') else 'tiered'
 env=base(solver)
 env['LEAN_SERVER_PROJECT_DIR']=str(m.m.T/'mathlib4')
 build=U/'farkas427'
 env['LEAN_PATH']=str(build/'.lake/build/lib/lean')+os.pathsep+env.get('LEAN_PATH','')
 env.pop('FARKAS_USE_FAST',None)
 if method.startswith('fast'):env['FARKAS_USE_FAST']='1'
 return env
m.m.environment=environment
if __name__=='__main__':
 m.m.resource.setrlimit(m.m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{16,17,18,19})
 out=D/'farkas-fast427-full1';out.mkdir()
 orders=[('full-hybrid','fast-hybrid','full-highs','fast-highs'),
         ('fast-highs','full-highs','fast-hybrid','full-hybrid'),
         ('full-highs','fast-highs','full-hybrid','fast-hybrid')]
 for rep,order in enumerate(orders):
  answers={}
  for method in order:
   answers[method]=m.capture(out,f'goedel427-rep{rep}-{method}',method,'goedel427')
  for solver in ['hybrid','highs']:
   a=answers['full-'+solver];b=answers['fast-'+solver]
   differences=[i for i in a if a[i]!=b.get(i)]
   (out/f'goedel427-rep{rep}-{solver}-basic-differences.json').write_text(json.dumps(differences)+'\n')
 for method in ['full-hybrid','fast-hybrid','full-highs','fast-highs']:
  m.capture(out,'goedel427-profile-'+method,method,'goedel427',True)
 (out/'acquisition-completed.md').write_text('All16proof-producing-preprocessing conditions returned; fullresultreview required, noautomaticRQ/device/noveltyclaim.\n')
