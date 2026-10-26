from pathlib import Path
import subprocess,os,time,json,gzip,datetime,signal,psutil
r=Path('/workspaces/repository')
sdk=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
project=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
base=r/'artifacts/hotspot-mechanisms-2026-10-25/simp-all-profile/phase-completion-20261026'
out=base/'analyzer-validation-001';out.mkdir(exist_ok=False)
tmp=Path('/tmp/gpu-smt-simp-phases-20261026')
l=json.loads(Path('/tmp/gpu-smt-resource-pair-20261025/active-full.json').read_text())
old=psutil.Process(l['pid'])
assert int((Path('/proc')/str(old.pid)/'stat').read_text().rsplit(')',1)[1].split()[19])==l['start_ticks']
original_env=dict(part.split(b'=',1)for part in (Path('/proc')/str(old.pid)/'environ').read_bytes().split(b'\0')if b'='in part)
env=dict(os.environ,PATH=str(sdk/'bin')+os.pathsep+os.environ['PATH'],LEAN_SYSROOT=str(sdk))
env['LEAN_PATH']=os.pathsep.join([str(tmp),'/tmp/gpu-smt-interval-continuation-20261025',
 '/tmp/gpu-smt-simp-all-profile-20261025','/tmp/gpu-smt-interval-bound-profile-20261025',
 original_env[b'LEAN_PATH'].decode()])
module=r/'bench/lean-failure-profile/simp-all-profile/SimpAllProfile.lean'
commands=[['python3','-B','-m','unittest','discover','-s','tests','-p','test_simp_stage_attribution.py','-v']]
project=r
os.sched_setaffinity(0,{11})
root=psutil.Process();samples=[];pressure=False;errors=[];start=time.monotonic();receipts=[]
def sample():
 owned={}
 for owner in [root,old]:
  try:
   for q in [owner]+owner.children(recursive=True):
    try:owned[(q.pid,q.create_time())]=q.memory_info().rss
    except psutil.NoSuchProcess:pass
  except psutil.NoSuchProcess:pass
 total=sum(owned.values());samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total))
 return total
for i,cmd in enumerate(commands):
 p=None;begin=time.monotonic()
 with(out/('command-%d.log'%i)).open('wb')as f:
  try:
   if sample()>=48*1024**3:raise RuntimeError('No aggregate headroom for new compiler/parser')
   p=subprocess.Popen(cmd,cwd=project,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   while True:
    if sample()>48*1024**3 and p.poll()is None:
     pressure=True;os.killpg(p.pid,signal.SIGKILL)
    if p.poll()is not None:break
    time.sleep(1)
  except BaseException as e:errors.append(repr(e))
  finally:
   if p is not None:
    if p.poll()is None:os.killpg(p.pid,signal.SIGKILL)
    code=p.wait()
   else:code=None
 receipts.append(dict(command=cmd,exit=code,seconds=time.monotonic()-begin))
 if code!=0:break
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),commands=receipts,
 cwd=str(project),seconds=time.monotonic()-start,samples=len(samples),
 combined_peak_rss_bytes=max(x['rss_bytes']for x in samples),budget_bytes=48*1024**3,
 pressure_aborted_only_new_compiler=pressure,monitor_errors=errors,
 python_diagnostic_tests=True,native_candidate_executions=0,original_group=old.pid,
 original_group_start_ticks=l['start_ticks'],native_body_elaboration=False)
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(out/'memory-samples.jsonl.gz').write_bytes(gzip.compress(
 ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
(out/'module-source.lean').write_bytes(module.read_bytes())
(out/'run-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(receipt),flush=True)
for f in sorted(out.glob('*.log')):print(f.name,f.read_text()[-6000:],flush=True)
raise SystemExit(0 if len(receipts)==len(commands) and receipts[-1]['exit']==0 else 1)
