from pathlib import Path
import types,sys,os,json
D=Path(__file__).parent
source=(D/'run-gc-repaired-header.py').read_text().replace('8002','8004').replace('preflight-gc-input.jsonl','highs-preflight-input.jsonl')
m=types.ModuleType('fullHighsNativeCapture');m.__file__=str(D/'run-highs-native-cpu.py')
exec(compile(source,str(D/'run-gc-repaired-header.py'),'exec'),m.__dict__)
base=m.environment
current_profile=False;current_folder=None
def environment(method):
 env=base('compiled')
 for key in ['FARKAS_CORPUS_FILE','FARKAS_EXTERNAL_CPU_HYBRID','HIGHS_CERT_TELEMETRY']:
  env.pop(key,None)
 env['LEAN_SERVER_REPL_PATH']=str(m.T/'repl-kimina-farkas-header-repair/.lake/build/bin/repl')
 build=m.T/'farkas427'
 paths=[str(build/'.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (build/'.lake/packages').iterdir() if p.is_dir()]
 env['LEAN_PATH']=os.pathsep.join(paths+([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
 env['FARKAS_NATIVE_BIN']=str(D/'highs-certificate-oracle.py' if method=='highs' else D/'farkas-external-support')
 if method=='hybrid':env['FARKAS_EXTERNAL_CPU_HYBRID']='1'
 if current_profile:
  env['FARKAS_CORPUS_FILE']=str(current_folder/'oracle.jsonl')
  if method=='highs':env['HIGHS_CERT_TELEMETRY']='1'
 return env
m.environment=environment
def capture(out,label,method,ds,profile=False):
 global current_profile,current_folder
 current_profile=profile;current_folder=out/label
 return m.capture(out,label,ds,method,profile)
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{4,5,6,7})
 action=sys.argv[1]
 if action=='preflight':
  selected=[]
  for line in (D/'input.jsonl').read_text().splitlines():
   row=json.loads(line)
   if row['proof_id'] in ['Proof_00000','Proof_00004','Proof_00009','Proof_00075']:selected.append(row)
  assert len(selected)==4
  (D/'highs-preflight-input.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected))
  out=D/'highs-native-cpu-preflight1';out.mkdir()
  for method in ['tiered','hybrid','highs']:capture(out,method,method,'preflight',True)
 elif action=='full':
  out=D/'highs-native-cpu-full1';out.mkdir()
  for rep,order in enumerate([('tiered','hybrid','highs'),('highs','tiered','hybrid'),('hybrid','highs','tiered')]):
   trio={}
   for method in order:trio[method]=capture(out,f'goedel427-rep{rep}-{method}',method,'goedel427')
   for method in ['hybrid','highs']:
    differences=[i for i in trio['tiered'] if trio['tiered'][i]!=trio[method].get(i)]
    (out/f'goedel427-rep{rep}-{method}-basic-differences.json').write_text(json.dumps(differences)+'\n')
  for method in ['tiered','hybrid','highs']:capture(out,f'goedel427-profile-{method}',method,'goedel427',True)
  (out/'acquisition-completed.md').write_text('All12complete CPU solverconditions returned. Fullresultreviewrequired, noautomaticRQ/deviceclaim.\n')
 else:raise ValueError('preflight or full only')
