from pathlib import Path
import types,sys,os,json
D=Path(__file__).parent
source=(D/'run-gc.py').read_text().replace('8002','8005')
m=types.ModuleType('fullNativeOracleCapture');m.__file__=str(D/'run-native-oracle.py')
exec(compile(source,str(D/'run-gc.py'),'exec'),m.__dict__)
base=m.environment
current_profile=False;current_folder=None
def environment(method):
 env=base('compiled')
 env.pop('FARKAS_CORPUS_FILE',None)
 if method=='native':
  env['LEAN_SERVER_REPL_PATH']=str(m.T/'repl-kimina-farkas/.lake/build/bin/repl')
  build=m.T/'farkas427'
  paths=[str(build/'.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (build/'.lake/packages').iterdir() if p.is_dir()]
  env['LEAN_PATH']=os.pathsep.join(paths+([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
  env['FARKAS_NATIVE_BIN']='/workspaces/.agent-state/gpu-smt-deps/lean49-arithmetic/build3/upstream/oracle/native/target/release/farkas-oracled'
  if current_profile:env['FARKAS_CORPUS_FILE']=str(current_folder/'oracle.jsonl')
 return env
m.environment=environment
def capture(out,label,method,ds,profile=False):
 global current_profile,current_folder
 current_profile=profile;current_folder=out/label
 return m.capture(out,label,ds,method,profile)
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{0,1,2,3})
 action=sys.argv[1]
 if action=='preflight':
  out=D/'native-oracle-main-preflight1';out.mkdir()
  for method in ['aot','native']:capture(out,method,method,'preflight')
 elif action=='full':
  out=D/'native-oracle-full1';out.mkdir()
  for rep,order in enumerate([('aot','native'),('native','aot'),('aot','native')]):
   pair={}
   for method in order:pair[method]=capture(out,f'goedel427-rep{rep}-{method}',method,'goedel427')
   differences=[i for i in pair['aot'] if pair['aot'][i]!=pair['native'].get(i)]
   (out/f'goedel427-rep{rep}-basic-differences.json').write_text(json.dumps(differences)+'\n')
  for method in ['aot','native']:capture(out,f'goedel427-profile-{method}',method,'goedel427',True)
  (out/'acquisition-completed.md').write_text('All8nativeoraclecomparisonconditionsreturned. Fullresultreviewrequired; noautomaticRQ/deviceclaim.\n')
 else:raise ValueError('preflight or full only')
