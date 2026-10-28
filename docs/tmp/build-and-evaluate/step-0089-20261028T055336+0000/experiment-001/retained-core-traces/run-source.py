from pathlib import Path
import subprocess,os,time,json,gzip,datetime,signal,psutil
r=Path('/workspaces/repository')
sdk=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
project=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/mathlib4')
base=Path(Path('/tmp/gpu-smt-step0089-path.txt').read_text())/'experiment-001'
out=base/os.environ['GPU_SMT_TEST_CELL'];out.mkdir(exist_ok=False)
tmp=Path('/tmp/gpu-smt-source-cost-crossfit-20261026')
current=json.loads((Path(Path('/tmp/gpu-smt-active-prepared-policy7808.txt').read_text())/'manifest.json').read_text())
l={'pid':current['controller_pid'],'start_ticks':current['controller_start_ticks']}
old=psutil.Process(l['pid'])
continuation=psutil.Process(499365)
assert int(Path('/proc/499365/stat').read_text().rsplit(')',1)[1].split()[19])==159426315
assert int((Path('/proc')/str(old.pid)/'stat').read_text().rsplit(')',1)[1].split()[19])==l['start_ticks']
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR='/tmp/gpu-smt-rust-engine-build-20261025/target',CARGO_BUILD_JOBS='1',PATH='/tmp/gpu-smt-code-verification-20261025/leanmlir-sdk/lean-4.27.0-nightly-2025-12-01-linux/bin:/usr/local/cargo/bin:'+os.environ['PATH'],LEAN_SYSROOT='/tmp/gpu-smt-code-verification-20261025/leanmlir-sdk/lean-4.27.0-nightly-2025-12-01-linux',LEAN_PATH='/tmp/gpu-smt-lrat-fused-build-20261028')
module=Path('/tmp/gpu-smt-source-memory-crossfit-20261027.py')
commands=json.loads(os.environ['GPU_SMT_TEST_COMMAND'])
os.sched_setaffinity(0,{11})
root=psutil.Process();samples=[];pressure=False;errors=[];start=time.monotonic();receipts=[]
def sample():
 owned={}
 for owner in [root,old,continuation]:
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
   p=subprocess.Popen(cmd,cwd=r,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
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
 cwd=str(r),seconds=time.monotonic()-start,samples=len(samples),
 combined_peak_rss_bytes=max(x['rss_bytes']for x in samples),budget_bytes=48*1024**3,
 pressure_aborted_only_new_compiler=pressure,monitor_errors=errors,
 offline_native_core_diagnosis=True,native_candidate_executions=0,original_group=old.pid,
 original_group_start_ticks=l['start_ticks'],original_generated_candidate_elaboration=False,native_development_module_elaboration=False,analysis_commands=sum(x['exit']is not None for x in receipts))
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(out/'memory-samples.jsonl.gz').write_bytes(gzip.compress(
 ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))

(out/'run-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(receipt),flush=True)
for f in sorted(out.glob('*.log')):print(f.name,f.read_text()[-6000:],flush=True)
raise SystemExit(0 if len(receipts)==len(commands) and receipts[-1]['exit']==0 else 1)
