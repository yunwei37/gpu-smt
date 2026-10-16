from pathlib import Path
import types,os,json
D=Path(__file__).parent
source=(D/'product-application-probe.py').read_text().replace("'8008'","'8009'")
p=types.ModuleType('heavy_real_lp_capture');p.__file__=str(D/'heavy-real-lp-preflight.py')
exec(compile(source,str(D/'product-application-probe.py'),'exec'),p.__dict__)
base=p.environment
def environment(method):
 env=base('fast-products')
 if method=='highs':
  env['FARKAS_NATIVE_BIN']=str(D/'highs-certificate-oracle.py')
  env.pop('FARKAS_EXTERNAL_CPU_HYBRID',None)
  env['HIGHS_CERT_TELEMETRY']='1'
 return env
p.m.m.environment=environment
if __name__=='__main__':
 p.m.m.resource.setrlimit(p.m.m.resource.RLIMIT_CORE,(0,0))
 root=D/'heavy-real-lp-preflight1';root.mkdir()
 selected=[json.loads(s) for s in (D/'input.jsonl').read_text().splitlines() if json.loads(s)['proof_id']=='Proof_05612']
 assert len(selected)==1
 (root/'input.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected))
 (root/'native-library.json').write_bytes((D/'native-library.json').read_bytes())
 p.m.m.D=root
 for method in ['hybrid','highs']:p.m.capture(root,method,method,'heavy-real',True)
