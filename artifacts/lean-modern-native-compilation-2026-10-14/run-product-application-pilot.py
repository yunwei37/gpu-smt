from pathlib import Path
import types,os,json
D=Path(__file__).parent;U=Path('/tmp/gpu-smt-product-batch427-20261014')
source=(D/'run-highs-native-cpu.py').read_text().replace('8004','8008')
m=types.ModuleType('product427ProbeCapture');m.__file__=str(D/'product-application-probe.py')
exec(compile(source,str(D/'run-highs-native-cpu.py'),'exec'),m.__dict__)
base=m.environment
def environment(method):
 env=base('hybrid')
 env['LEAN_SERVER_PROJECT_DIR']=str(m.m.T/'mathlib4')
 env['LEAN_PATH']=str(U/'farkas427/.lake/build/lib/lean')+os.pathsep+env.get('LEAN_PATH','')
 for key in ['FARKAS_USE_FAST','FARKAS_USE_PRODUCTS']:env.pop(key,None)
 if method.startswith('fast'):env['FARKAS_USE_FAST']='1'
 if method.endswith('products'):env['FARKAS_USE_PRODUCTS']='1'
 return env
m.m.environment=environment
if __name__=='__main__':
 m.m.resource.setrlimit(m.m.resource.RLIMIT_CORE,(0,0))
 out=D/'product-application-pilot1';out.mkdir()
 for rep,order in enumerate([('fast','fast-products'),('fast-products','fast'),('fast','fast-products')]):
  for method in order:m.capture(out,f'rep{rep}-{method}',method,'preflight',False)
