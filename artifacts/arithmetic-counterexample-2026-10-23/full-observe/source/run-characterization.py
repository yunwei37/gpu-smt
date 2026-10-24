"""One full own-method observation of all original miniF2F candidates."""
from pathlib import Path
import asyncio,datetime,gzip,json,os,runpy,shutil,time
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23';B=R/'bench/lean-counterexample'
D=runpy.run_path(str(B/'qualify.py'));capture,args,build=D['capture'],D['args'],D['build']
root=A/'full-observe';root.mkdir(exist_ok=False)
source=root/'source';source.mkdir()
for name in ['Counterexample.lean','Prepare.lean','worker.py','prepare.py','run-characterization.py']:
 shutil.copy2(B/name,source/name)
shutil.copy2(A/'build.json',source/'build.json')
with gzip.open(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as f:
 rows=[json.loads(l)for l in f]
assert len(rows)==7808 and [x['index']for x in rows]==list(range(7808))
prep=root/'preparation';prep.mkdir()
# Use the same owned-tree watchdog during source-native parser preparation.
guard=capture['_memory'].MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,args.repl,prep)
def stop_preparation():
 for p in reversed(guard.owned()):
  if p.pid!=os.getpid():
   try:p.kill()
   except Exception:pass
guard.on_error=stop_preparation
guard.start();started=time.monotonic_ns()
try:
 snippets=runpy.run_path(str(source/'prepare.py'))['prepare'](rows,prep)
finally:guard.stop()
prep_seconds=(time.monotonic_ns()-started)/1e9
(prep/'memory-summary.json').write_text(json.dumps(guard.summary(),indent=2)+'\n')
assert not guard.error
out=root/'verification'
os.environ.update(GPU_SMT_CEX_MODE='observe',GPU_SMT_CEX_WORKER=str(source/'worker.py'),GPU_SMT_CEX_LOG=str(out/'goals.jsonl'))
(root/'launch.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),
 sources=len(snippets),preparation_seconds=prep_seconds,
 source_commit=__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
 scope='Own typed-goal characterization, not GPU performance or a new external-method comparison.'),indent=2)+'\n')
async def main():
 terminal=await capture['cell'](args,'stock',out,snippets,build)
 terminal.update(own_method_mode='observe',input_preparation_seconds=prep_seconds,
  whole_including_input_preparation_seconds=terminal['whole_lifecycle_seconds']+prep_seconds,
  scope='Complete originalminiF2F observation of our typed entry hook. No GPU active. Root self-review.')
 (out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
 if terminal['state']!='complete':raise RuntimeError('Preserve partial own characterization')
 assert terminal['returned']==7808 and not terminal['memory_watchdog']['error']and not terminal['owned_live_descendants_after_shutdown']
 archive=[]
 for p in list(out.iterdir()):
  if p.is_file()and p.suffix in['.jsonl','.log']:
   raw=p.read_bytes();target=p.with_name(p.name+'.gz')
   packed=gzip.compress(raw,mtime=0);assert gzip.decompress(packed)==raw
   target.write_bytes(packed);p.unlink()
   archive.append(dict(path=p.name,original_bytes=len(raw),gzip_bytes=len(packed),roundtrip_equal=True))
 (out/'raw-archive.json').write_text(json.dumps(archive,indent=2)+'\n')
 print(json.dumps(dict(event='own_full_characterization_closed',terminal=terminal)),flush=True)
asyncio.run(main())
