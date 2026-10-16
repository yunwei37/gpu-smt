from pathlib import Path
import types,os,sys
D=Path(__file__).parent
source=(D/'run-highs-native-cpu.py').read_text().replace('8004','8006')
m=types.ModuleType('fastNativeStageCapture');m.__file__=str(D/'fast-native-stage.py')
exec(compile(source,str(D/'run-highs-native-cpu.py'),'exec'),m.__dict__)
base=m.environment
current_profile_directory=None
def environment(method):
 env=base(method)
 env['LEAN_SERVER_REPL_PATH']=str(m.m.T/'repl-kimina-farkas-native-stage-profile/.lake/build/bin/repl')
 env['LEAN_SERVER_PROFILE_DIRECTORY']=str(current_profile_directory)
 return env
m.m.environment=environment
if __name__=='__main__':
 m.m.resource.setrlimit(m.m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{16,17,18,19})
 out=D/'fast-native-stage1';out.mkdir()
 for method in ['tiered','hybrid','highs']:
  current_profile_directory=out/method/'native-profiles'
  m.capture(out,method,method,'preflight',True)
