from pathlib import Path
import types,os,sys,json,datetime
D=Path(__file__).parent
# Reuse the established stock-HTTP capture; only the separate profiler's port/backend change.
source=(D/'run-gc.py').read_text().replace('127.0.0.1:8002','127.0.0.1:8003').replace("LEAN_SERVER_PORT=\'8002\'","LEAN_SERVER_PORT=\'8003\'")
source=source.replace("str(T/'repl-kimina-gc/.lake/build/bin/repl')","str(T/'repl-kimina-gc-dynamic-profile/.lake/build/bin/repl')")
source=source.replace("'backend':'exact4.27producer initialOptions; compiled native-load only when method=compiled'","'backend':'Official producer4.27 traceprofiler/Firefox export, profile observer costs included; no primary performance claim'")
source=source.replace('privatePort8002','privatePort8003')
m=types.ModuleType('modernDynamicProfileCapture');m.__file__=str(D/'dynamic-profile.py')
exec(compile(source,str(D/'run.py'),'exec'),m.__dict__)
original_environment=m.environment
def environment(method):
 env=original_environment(method)
 env['LEAN_SERVER_PROFILE_DIRECTORY']=str(profile_dir)
 return env
m.environment=environment
if __name__=='__main__':
 m.resource.setrlimit(m.resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{12,13,14,15})
 action=sys.argv[1]
 if action=='preflight':
  out=D/'dynamic-profile-gc-preflight1';out.mkdir()
  label='profile-original';profile_dir=out/label/'native-profiles'
  m.capture(out,label,'preflight','profile-original',True)
 elif action=='full':
  out=D/'dynamic-profile-gc-full1';out.mkdir()
  label='goedel427-profile-original';profile_dir=out/label/'native-profiles'
  m.capture(out,label,'goedel427','profile-original',True)
 else:raise ValueError('preflight or full only')
