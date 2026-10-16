from pathlib import Path
import types,os,json
D=Path(__file__).parent;U=Path('/tmp/gpu-smt-lazy-products427-20261015')
source=(D/'product-application-probe.py').read_text().replace("'8008'","'8010'")
p=types.ModuleType('lazy_products_capture');p.__file__=str(D/'lazy-products-preflight.py')
exec(compile(source,str(D/'product-application-probe.py'),'exec'),p.__dict__)
base=p.environment
def environment(method):
 env=base('fast-products' if method=='fast' else 'full-products')
 env['LEAN_PATH']=str(U/'farkas427/.lake/build/lib/lean')+os.pathsep+env.get('LEAN_PATH','')
 env['FARKAS_NATIVE_BIN']=str(D/'highs-certificate-oracle.py')
 env.pop('FARKAS_EXTERNAL_CPU_HYBRID',None)
 env['HIGHS_CERT_TELEMETRY']='1'
 env.pop('FARKAS_USE_LAZY_PRODUCTS',None)
 if method=='lazy':env['FARKAS_USE_LAZY_PRODUCTS']='1'
 return env
p.m.m.environment=environment
if __name__=='__main__':
 p.m.m.resource.setrlimit(p.m.m.resource.RLIMIT_CORE,(0,0))
 root=D/'lazy-products-preflight1';root.mkdir()
 ids={'Proof_00000','Proof_00004','Proof_00009','Proof_00075','Proof_05612'}
 selected=[json.loads(s) for s in (D/'input.jsonl').read_text().splitlines() if json.loads(s)['proof_id'] in ids]
 assert len(selected)==5
 (root/'input.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected))
 (root/'native-library.json').write_bytes((D/'native-library.json').read_bytes())
 p.m.m.D=root
 for method in ['eager','lazy','fast']:p.m.capture(root,method,method,'original-sources',True)
