from pathlib import Path
import types,os
D=Path(__file__).parent
source=(D/'run-gc.py').read_text().replace('8002','8005')
source=source.replace("str(T/'repl-kimina-native-gc/.lake/build/bin/repl')","str(T/'repl-kimina-farkas/.lake/build/bin/repl')")
source=source.replace("'preflight-gc-input.jsonl'","'stage-probe-input.jsonl'")
m=types.ModuleType('nativeOracleCapture');m.__file__=str(D/'native-oracle-probe.py')
exec(compile(source,str(D/'run-gc.py'),'exec'),m.__dict__)
base=m.environment;out=D/'native-oracle-probe1';label='native-oracle'
def environment(method):
 env=base(method)
 build=m.T/'farkas427'
 paths=[str(build/'.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (build/'.lake/packages').iterdir() if p.is_dir()]
 env['LEAN_PATH']=os.pathsep.join(paths+([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
 env['FARKAS_NATIVE_BIN']='/workspaces/.agent-state/gpu-smt-deps/lean49-arithmetic/build3/upstream/oracle/native/target/release/farkas-oracled'
 env['FARKAS_CORPUS_FILE']=str(out/label/'oracle.jsonl')
 return env
m.environment=environment
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{4,5,6,7})
 out.mkdir();m.capture(out,label,'preflight','compiled',True)
