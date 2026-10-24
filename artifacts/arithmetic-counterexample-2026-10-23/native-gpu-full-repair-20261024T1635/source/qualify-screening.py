"""Own screening qualification, or one complete original miniF2F off/on pair."""
from pathlib import Path
import argparse,asyncio,datetime,gzip,json,os,runpy,shutil,sys,time,traceback
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23';B=R/'bench/lean-counterexample'

OWNED_OUTPUT=None

async def main():
 global OWNED_OUTPUT
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--host',required=True)
 parser.add_argument('--backend',choices=['device','cpu-reference'],required=True)
 parser.add_argument('--out',type=Path,required=True)
 parser.add_argument('--full',action='store_true',help='After reviewing native24, run all7808 original candidates; off uses untouched native sources.')
 parser.add_argument('--reuse-off',type=Path,help='Reuse a closed untouched-native cell after transport-only repair; rerun the complete GPU cell, never splice partial sources.')
 args=parser.parse_args()
 if args.reuse_off and not args.full:parser.error('--reuse-off requires the complete original population')
 terminal=A/'full-observe/verification/terminal.json'
 if not terminal.exists()or json.loads(terminal.read_text())['state']!='complete':
  raise RuntimeError('Preserve the active sole full observation; no concurrent Lean qualification')
 D=runpy.run_path(str(B/'qualify.py'));capture,settings,build=D['capture'],D['args'],D['build']
 from worker import provider_memory_sampler
 sampler=provider_memory_sampler(args.host,5001,args.backend);provider=sampler()
 settings.external_memory_sampler=sampler
 args.out.mkdir(exist_ok=False);OWNED_OUTPUT=args.out
 source=args.out/'source';source.mkdir()
 for name in ['Counterexample.lean','Prepare.lean','worker.py','prepare.py','qualify-screening.py','analyze-screening.py']:
  shutil.copy2(B/name,source/name)
 shutil.copy2(A/'build.json',source/'build.json')
 # The build's actual source is recorded; do not silently call old code the alias repair.
 built_source=Path(json.loads((A/'build.json').read_text())['build'])/'Counterexample.lean'
 source_matches_build=built_source.read_bytes()==(B/'Counterexample.lean').read_bytes()
 if not source_matches_build:raise RuntimeError('Build the current exporter before screening; do not label old binaries as the current source')
 wanted=[379,802]+list(range(22))
 with gzip.open(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as f:
  originals=[json.loads(line)for line in f]
 selected=originals if args.full else[originals[i]for i in wanted]
 assert len(selected)==(7808 if args.full else 24)
 assert [x['index']for x in originals]==list(range(7808))
 original_snippets=[dict(proof_id='minif2f-'+str(x['index']),code=x['code'])for x in selected]
 reused_off=None
 if args.reuse_off:
  read_cell=runpy.run_path(str(B/'analyze-screening.py'))['read_cell']
  reused_off,prior_sources,_=read_cell(args.reuse_off)
  if reused_off.get('own_mode')!='off' or len(prior_sources)!=7808 or list(prior_sources)!=[x['proof_id']for x in original_snippets]:
   raise RuntimeError('Only the completed original full nativeoff can be reused')
  expected=dict(source_concurrency=2,affinity=[8,9,10,11],aggregate_memory_budget_bytes=48*1024**3,
   per_native_repl_address_limit_bytes=24*1024**3,maximum_live_native_repls=2,
   native_library=build['native_library'])
  for key,value in expected.items():
   if reused_off.get(key)!=value:raise RuntimeError('Reused native resource/build mismatch: '+key)
 prep=args.out/'preparation';prep.mkdir()
 guard=capture['_memory'].MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,settings.repl,prep)
 guard.extra_memory=sampler
 def stop_owned():
  for p in reversed(guard.owned()):
   if p.pid!=os.getpid():
    try:p.kill()
    except Exception:pass
 guard.on_error=stop_owned
 guard.start();started=time.perf_counter()
 try:snippets=runpy.run_path(str(source/'prepare.py'))['prepare'](selected,prep)
 finally:guard.stop()
 (prep/'memory-summary.json').write_text(json.dumps(guard.summary(),indent=2)+'\n')
 if guard.error:raise RuntimeError(guard.error)
 preparation_seconds=time.perf_counter()-started
 os.environ.update(GPU_SMT_CEX_GPU_HOST=args.host,GPU_SMT_CEX_GPU_PORT='5001',
  GPU_SMT_CEX_WORKER=str(source/'worker.py'))
 cells=[]
 for mode in (['gpu']if reused_off else['off','gpu']):
  out=args.out/mode
  os.environ.update(GPU_SMT_CEX_MODE=mode,GPU_SMT_CEX_LOG=str(out/'goals.jsonl'))
  items=original_snippets if args.full and mode=='off'else snippets
  result=await capture['cell'](settings,'stock',out,items,build)
  result.update(own_mode=mode,provider_backend=args.backend,point_screening_device_requested=(mode=='gpu'and args.backend=='device'),scope=('One full original7808 matched pair; root review required, fixed off-first order.'if args.full else'24 actual source qualification, not complete benchmark or speedup.'))
  (out/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
  cells.append(result)
  if result['state']!='complete' or result['returned']!=len(selected):raise RuntimeError('Preserve partial qualification')
  if result['memory_watchdog']['error']or result['owned_live_descendants_after_shutdown']:raise RuntimeError('Resource monitoring/child retirement incomplete')
 summary=dict(reused_off_directory=str(args.reuse_off)if args.reuse_off else None,full_population=args.full,native_off_uses_untouched_originals=args.full,source_ids=[x['proof_id']for x in snippets],source_matches_build=source_matches_build,
  preparation_seconds=preparation_seconds,provider_identity=provider,
  cells=[dict(mode=x['own_mode'],state=x['state'],returned=x['returned'])for x in cells],
  scope='Own off/on original candidates. Qualification is not performance evidence; a full pair additionally requires per-source outcomes, complete cold provider costs, failure/timeout/tail analysis and self-review.')
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 # Both native cells have joined all children; preserve closed raw losslessly.
 archives=[]
 for cell in cells:
  directory=args.out/cell['own_mode']
  for raw in list(directory.iterdir()):
   if raw.is_file()and raw.suffix in ['.jsonl','.log']:
    data=raw.read_bytes();packed=gzip.compress(data,mtime=0)
    if gzip.decompress(packed)!=data:raise RuntimeError('Raw archive mismatch; original retained')
    raw.with_name(raw.name+'.gz').write_bytes(packed);raw.unlink()
    archives.append(dict(path=str(raw.relative_to(args.out)),raw_bytes=len(data),gzip_bytes=len(packed),roundtrip_equal=True))
 (args.out/'raw-archive.json').write_text(json.dumps(archives,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':
 exit_code=0;error=None
 try:asyncio.run(main())
 except BaseException as ex:
  exit_code=ex.code if isinstance(ex,SystemExit)and isinstance(ex.code,int)else 1
  error=traceback.format_exc();raise
 finally:
  # A replay that did not create this output must never overwrite its owner's exit.
  if OWNED_OUTPUT is not None:
   stat=Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()
   receipt=dict(pid=os.getpid(),start_ticks=int(stat[19]),exit=exit_code,error=error,
    finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
   (OWNED_OUTPUT/'client-exit.json').write_text(json.dumps(receipt,indent=2)+'\n')
