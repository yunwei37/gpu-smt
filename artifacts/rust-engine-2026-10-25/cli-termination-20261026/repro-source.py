from pathlib import Path
import subprocess,os,time,signal,json,datetime
r=Path('/workspaces/repository');a=r/'artifacts/rust-engine-2026-10-25/cli-termination-20261026'
os.sched_setaffinity(0,{11})
binary=Path('/tmp/gpu-smt-rust-engine-build-20261025/target/debug/gpu-smt')
cmd=[str(binary),'serve','--repl','/usr/bin/python3','--project','/tmp','--environment','idle-signal-reproduction-no-native','--cpus','11','--listen','127.0.0.1:0']
with(a/'repro-before.log').open('wb')as log:
 p=subprocess.Popen(cmd,cwd=r,stdin=subprocess.DEVNULL,stdout=log,stderr=log)
 try:
  time.sleep(.3);assert p.poll()is None
  stat=Path('/proc')/str(p.pid)/'stat'
  birth=int(stat.read_text().rsplit(')',1)[1].split()[19])
  children=Path('/proc')/str(p.pid)/'task'/str(p.pid)/'children'
  assert not children.read_text().strip(),'idle reproduction must launch no backend child'
  os.kill(p.pid,signal.SIGTERM);code=p.wait(timeout=5)
 finally:
  if p.poll()is None:p.kill();p.wait()
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source='cdaae0021ac7069e9f1833e1b0f343b991204800',command=cmd,pid=p.pid,start_ticks=birth,exit=code,expected_graceful_exit=0,defect_reproduced=code==-signal.SIGTERM,native_candidate_executions=0,backend_children=0,binary_mtime=binary.stat().st_mtime)
(a/'repro-before.json').write_text(json.dumps(receipt,indent=2)+chr(10))
print(json.dumps(receipt),flush=True)
assert code==-signal.SIGTERM
