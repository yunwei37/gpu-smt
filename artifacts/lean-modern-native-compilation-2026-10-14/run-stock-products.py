from pathlib import Path
import types,os,sys,json
D=Path(__file__).parent
N=Path('/tmp/gpu-smt-stock-products427-20261015')
U=Path('/tmp/gpu-smt-lazy-products427-20261015/farkas427')
source=(D/'run-gc-repaired-header.py').read_text().replace('8002','8011')
m=types.ModuleType('stock_products_capture');m.__file__=str(D/'run-stock-products.py')
exec(compile(source,str(D/'run-gc-repaired-header.py'),'exec'),m.__dict__)
base=m.environment
current_profile=False;current_folder=None
def environment(method):
 env=base('compiled')
 config=json.loads((D/f'stock-products-{method}-native-library.json').read_text())
 env['LEAN_SERVER_NATIVE_DYNLIB']=config['load_manifest']
 env['LD_LIBRARY_PATH']=os.pathsep.join(config['library_paths']+([env['LD_LIBRARY_PATH']] if env.get('LD_LIBRARY_PATH') else []))
 for key in ['FARKAS_NATIVE_BIN','FARKAS_USE_FAST','FARKAS_USE_PRODUCTS','FARKAS_USE_LAZY_PRODUCTS','FARKAS_EXTERNAL_CPU_HYBRID','HIGHS_CERT_TELEMETRY','FARKAS_CORPUS_FILE']:
  env.pop(key,None)
 if method=='products':
  env['LEAN_SERVER_REPL_PATH']=str(N/'repl/.lake/build/bin/repl')
  env['LEAN_PATH']=str(U/'.lake/build/lib/lean')+os.pathsep+env.get('LEAN_PATH','')
  if current_profile:env['FARKAS_CORPUS_FILE']=str(current_folder/'product-applications.jsonl')
 return env
m.environment=environment
def capture(out,label,method,ds,profile=False):
 global current_profile,current_folder
 current_profile=profile;current_folder=out/label
 return m.capture(out,label,ds,method,profile)
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0))
 action=sys.argv[1]
 if action=='preflight':
  root=D/'stock-products-preflight1';root.mkdir()
  ids={'Proof_00000','Proof_00004','Proof_00009','Proof_00075','Proof_05612'}
  rows=[json.loads(l) for l in (D/'input.jsonl').read_text().splitlines() if json.loads(l)['proof_id'] in ids]
  assert len(rows)==5
  (root/'input.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
  (root/'native-library.json').write_bytes((D/'stock-products-stock-native-library.json').read_bytes())
  m.D=root
  out=root/'cells';out.mkdir()
  for method in ['stock','products']:capture(out,method,method,'original-sources',True)
 elif action=='full':
  out=D/'stock-products-full1';out.mkdir()
  for rep,order in enumerate([('stock','products'),('products','stock'),('stock','products')]):
   for method in order:capture(out,f'goedel427-rep{rep}-{method}',method,'goedel427')
  for method in ['stock','products']:capture(out,f'goedel427-profile-{method}',method,'goedel427',True)
  (out/'acquisition-completed.md').write_text('All8original wholepopulation cells returned; complete result review required.\n')
 else:raise ValueError('preflight or full only')
