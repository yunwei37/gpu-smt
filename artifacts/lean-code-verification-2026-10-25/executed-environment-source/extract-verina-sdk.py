from pathlib import Path
import os,subprocess,time,tarfile,json,runpy,psutil,zstandard,gzip
R=Path('/workspaces/repository');O=R/'artifacts/lean-code-verification-2026-10-25'
P=Path('/tmp/gpu-smt-code-verification-20261025');M=O/'sdk-extraction2-memory';M.mkdir()
W=runpy.run_path(str(R/'bench/lean-native/linarith-oracle/memory_budget.py'))['MemoryWatchdog']
w=W(os.getpid(),48*1024**3,48*1024**3,2,'/tmp/gpu-smt-failure-profiler-20261025/repl',M)
if psutil.pid_exists(275822):
 proc=psutil.Process(275822);assert abs(proc.create_time()-1792894799.05)<.01
 w.include_owned_tree(275822,int(Path('/proc/275822/stat').read_text().rsplit(')',1)[1].split()[19]),R/'artifacts/lean-failure-profile-2026-10-25/full480/profile')
w.start();start=time.time()
try:
 with (P/'downloads/lean-4.18.0-linux.tar.zst').open('rb')as f,zstandard.ZstdDecompressor().stream_reader(f)as stream,tarfile.open(fileobj=stream,mode='r|')as tar:
  tar.extractall(P/'sdk',filter='data')
 binary=P/'sdk/lean-4.18.0-linux/bin/lean'
 q=subprocess.run([str(binary),'--version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 report=dict(exit=q.returncode,version=q.stdout,seconds=time.time()-start,SDK=str(binary.parent.parent),scope='Existing Python zstandard stream extraction replaces missing system zstd; version query only, not a proof collection.')
 # Reconstruct only original Verina project source/metadata, no code edits.
 V=P/'verina';V.mkdir(exist_ok=True)
 with gzip.open(O/'sunblaze-ucb--verina-sources.jsonl.gz','rt')as f:
  for line in f:
   item=json.loads(line);rel=Path(item['path'])
   assert not rel.is_absolute()and '..'not in rel.parts
   dest=V/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(item['text'].encode())
 report['Verina_original_project']=str(V)
 (O/'sdk-extraction2.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
finally:
 w.stop();(O/'sdk-extraction2-memory-summary.json').write_text(json.dumps(w.summary(),indent=2)+'\n')
