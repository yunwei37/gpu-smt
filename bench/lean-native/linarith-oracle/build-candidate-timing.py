"""Add per-source job intervals to existing REPL; outputs separate binary."""
from pathlib import Path
import os,subprocess,shutil,resource
R=Path('/workspaces/repository');U=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle')
T=Path('/tmp/gpu-smt-goedel427-20261014');B=T/'repl-kimina-native-gc-header-repair'
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{0,1,2,3})
p=B/'REPL/Main.lean';s=p.read_text()
marker='initialize candidateTimingMutex'
if marker not in s:
 a=s.index('unsafe def batchVerifySequential')
 s=s[:a]+'''initialize candidateTimingMutex : Std.Mutex Unit ← Std.Mutex.new ()

private def candidateTimed (cmd : Command) (action : IO α) : IO α := do
  let start ← IO.monoNanosNow
  try action
  finally
    let finish ← IO.monoNanosNow
    if let some path ← IO.getEnv "GPU_SMT_CANDIDATE_TIMING" then
      candidateTimingMutex.atomically do
        let row := Json.mkObj [("source",toJson cmd.cmd),("start_ns",toJson start),("end_ns",toJson finish)]
        let f ← IO.FS.Handle.mk path IO.FS.Mode.append
        f.putStrLn row.compress
        f.flush

'''+s[a:]
 old='IO.asTask (commandRunner cmd)'
 assert old in s;s=s.replace(old,'IO.asTask (candidateTimed cmd (commandRunner cmd))')
 p.write_text(s)
(U/'REPL-Main-candidate-timing.lean').write_text(s)
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
with (U/'build-candidate-timing.log').open('w')as log:
 subprocess.run(['lake','build','repl'],cwd=B,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
shutil.copy2(B/'.lake/build/bin/repl',U/'repl-candidate-timing')
print('BUILT separate REPL candidate timing binary')
