from pathlib import Path
import os,json,urllib.request,time,concurrent.futures,tarfile,runpy,psutil,zstandard,gzip
R=Path('/workspaces/repository');O=R/'artifacts/lean-code-verification-2026-10-25';P=Path('/tmp/gpu-smt-code-verification-20261025')
M=O/'leanmlir-prepare-memory';M.mkdir();W=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/memory_budget.py'))['MemoryWatchdog']
w=W(os.getpid(),48*1024**3,48*1024**3,2,'/tmp/gpu-smt-failure-profiler-20261025/repl',M)
if psutil.pid_exists(275822):
 p=psutil.Process(275822);assert abs(p.create_time()-1792894799.05)<.01
 w.include_owned_tree(275822,int(Path('/proc/275822/stat').read_text().rsplit(')',1)[1].split()[19]),R/'artifacts/lean-failure-profile-2026-10-25/full480/profile')
w.start();report=dict(started_UTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),scope='Pinned SDK/source preparation, not proof collection or reproduction of a comparison system.')
def download(url,name):
 dest=P/'downloads'/name;start=time.time();count=0
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'gpu-smt-research'}),timeout=60)as f,dest.open('wb')as out:
  while data:=f.read(1024**2):out.write(data);count+=len(data)
 return dict(url=url,path=str(dest),bytes=count,seconds=time.time()-start)
try:
 tasks=[('https://github.com/leanprover/lean4-nightly/releases/download/nightly-2025-12-01/lean-4.27.0-nightly-2025-12-01-linux.tar.zst','lean-nightly-20251201-linux.tar.zst'),
  ('https://codeload.github.com/leanprover-community/mathlib4-nightly-testing/tar.gz/2100ee662d0d4b3233534f70716a04f15f74c300','mathlib-nightly-2100ee66.tar.gz'),
  ('https://codeload.github.com/opencompl/lean-mlir/tar.gz/b8c4a771319a044854a4bbb49b8821381ef86ff8','lean-mlir-b8c4a771.tar.gz')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
  report['downloads']=list(pool.map(lambda q:download(*q),tasks))
 print('DOWNLOADS',json.dumps(report['downloads']),flush=True)
 target=P/'leanmlir-sdk';target.mkdir(exist_ok=True)
 with(P/'downloads/lean-nightly-20251201-linux.tar.zst').open('rb')as f,zstandard.ZstdDecompressor().stream_reader(f)as stream,tarfile.open(fileobj=stream,mode='r|')as tar:tar.extractall(target,filter='data')
 for archive,name in [('mathlib-nightly-2100ee66.tar.gz','mathlib-nightly'),('lean-mlir-b8c4a771.tar.gz','lean-mlir')]:
  out=P/name;out.mkdir(exist_ok=True)
  with tarfile.open(P/'downloads'/archive,'r:gz')as tar:
   for entry in tar:
    parts=Path(entry.name).parts[1:]
    if not parts:continue
    entry.name=str(Path(*parts));tar.extract(entry,out,filter='data')
 report['SDK']=str(next(target.glob('*/bin/lean')).parent.parent)
 report['mathlib']=str(P/'mathlib-nightly');report['project']=str(P/'lean-mlir')
 report['finished_UTC']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
 (O/'leanmlir-preparation.json').write_text(json.dumps(report,indent=2)+'\n');print('PREPARED',json.dumps(report))
finally:
 w.stop();(O/'leanmlir-prepare-memory-summary.json').write_text(json.dumps(w.summary(),indent=2)+'\n')
