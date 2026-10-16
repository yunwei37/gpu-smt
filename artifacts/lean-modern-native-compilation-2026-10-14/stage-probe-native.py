from pathlib import Path
import types,os
D=Path(__file__).parent
source=(D/'run-gc.py').read_text().replace('8002','8004')
source=source.replace("str(T/'repl-kimina-native-gc/.lake/build/bin/repl')","str(T/'repl-kimina-native-stage-profile/.lake/build/bin/repl')")
source=source.replace("'preflight-gc-input.jsonl'","'stage-probe-input.jsonl'")
m=types.ModuleType('nativeStageCapture');m.__file__=str(D/'stage-probe-native.py')
exec(compile(source,str(D/'run-gc.py'),'exec'),m.__dict__)
normal=m.environment;out=D/'stage-probe2';label='profile-compiled'
def environment(method):
 env=normal(method);env['LEAN_SERVER_PROFILE_DIRECTORY']=str(out/label/'native-profiles')
 return env
m.environment=environment
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{4,5,6,7})
 out.mkdir();m.capture(out,label,'preflight','compiled',True)
