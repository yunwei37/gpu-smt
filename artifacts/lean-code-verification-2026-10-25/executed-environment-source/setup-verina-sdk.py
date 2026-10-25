from pathlib import Path
import os,json,urllib.request,time,concurrent.futures,subprocess,tarfile,runpy,psutil,shutil
R=Path('/workspaces/repository');O=R/'artifacts/lean-code-verification-2026-10-25'
P=Path('/tmp/gpu-smt-code-verification-20261025');P.mkdir(exist_ok=True)
D=P/'downloads';D.mkdir(exist_ok=True);M=O/'sdk-preparation-memory';M.mkdir()
W=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/memory_budget.py'))['MemoryWatchdog']
w=W(os.getpid(),48*1024**3,48*1024**3,2,'/tmp/gpu-smt-failure-profiler-20261025/repl',M)
if psutil.pid_exists(275822):
 proc=psutil.Process(275822);assert abs(proc.create_time()-1792894799.05)<.01
 w.include_owned_tree(275822,int(Path('/proc/275822/stat').read_text().rsplit(')',1)[1].split()[19]),R/'artifacts/lean-failure-profile-2026-10-25/full480/profile')
w.start();report=dict(started_UTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),root=str(P),scope='Official pinned SDK and source download/extraction only; no Lean proof verification or second collection.')
def download(url,name):
 dest=D/name;size=0;start=time.time()
 request=urllib.request.Request(url,headers={'User-Agent':'gpu-smt-research'})
 with urllib.request.urlopen(request,timeout=60)as response,dest.open('wb')as out:
  while chunk:=response.read(1024*1024):out.write(chunk);size+=len(chunk)
 return dict(url=url,path=str(dest),bytes=size,seconds=time.time()-start)
try:
 urls=[('https://github.com/leanprover/lean4/releases/download/v4.18.0/lean-4.18.0-linux.tar.zst','lean-4.18.0-linux.tar.zst'),
  ('https://codeload.github.com/leanprover-community/mathlib4/tar.gz/aa936c36e8484abd300577139faf8e945850831a','mathlib4-aa936c36.tar.gz')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  jobs=[pool.submit(download,*q)for q in urls];report['downloads']=[]
  for job in jobs:
   try:
    row=job.result();report['downloads'].append(row);print('DOWNLOADED',json.dumps(row),flush=True)
   except Exception as ex:report['downloads'].append(dict(error=repr(ex)));print('DOWNLOAD_ERROR',repr(ex),flush=True)
 if (D/'mathlib4-aa936c36.tar.gz').exists():
  target=P/'mathlib-source';target.mkdir(exist_ok=True)
  with tarfile.open(D/'mathlib4-aa936c36.tar.gz','r:gz')as source:
   for entry in source:
    parts=Path(entry.name).parts[1:]
    if not parts:continue
    entry.name=str(Path(*parts));source.extract(entry,target,filter='data')
  report['mathlib_source']=str(target)
 if (D/'lean-4.18.0-linux.tar.zst').exists()and(D/'lean-4.18.0-linux.tar.zst').stat().st_size>0:
  sdk=P/'sdk';sdk.mkdir(exist_ok=True)
  cmd=['tar','--zstd','-xf',str(D/'lean-4.18.0-linux.tar.zst'),'-C',str(sdk)]
  q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  report['sdk_extract']=dict(command=cmd,exit=q.returncode,output=q.stdout)
  if q.returncode==0:
   binary=sdk/'lean-4.18.0-linux/bin/lean'
   # Version query is not a theorem/proof collection.
   version=subprocess.run([str(binary),'--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   report['sdk_version']=dict(exit=version.returncode,output=version.stdout)
 print(json.dumps(report,indent=2),flush=True)
finally:
 w.stop();report['finished_UTC']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
 (O/'sdk-preparation.json').write_text(json.dumps(report,indent=2)+'\n')
 (O/'sdk-preparation-memory-summary.json').write_text(json.dumps(w.summary(),indent=2)+'\n')
