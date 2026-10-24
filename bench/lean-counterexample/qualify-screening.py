"""After characterization, qualify own Lean screening off/on on 24 originals."""
from pathlib import Path
import argparse,asyncio,gzip,json,os,runpy,shutil,time
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23';B=R/'bench/lean-counterexample'

async def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--host',required=True)
 parser.add_argument('--backend',choices=['device','cpu-reference'],required=True)
 parser.add_argument('--out',type=Path,required=True)
 args=parser.parse_args()
 terminal=A/'full-observe/verification/terminal.json'
 if not terminal.exists()or json.loads(terminal.read_text())['state']!='complete':
  raise RuntimeError('Preserve the active sole full observation; no concurrent Lean qualification')
 D=runpy.run_path(str(B/'qualify.py'));capture,settings,build=D['capture'],D['args'],D['build']
 from worker import provider_memory_sampler
 sampler=provider_memory_sampler(args.host,5001,args.backend);provider=sampler()
 settings.external_memory_sampler=sampler
 args.out.mkdir(exist_ok=False);source=args.out/'source';source.mkdir()
 for name in ['Counterexample.lean','Prepare.lean','worker.py','prepare.py','qualify-screening.py']:
  shutil.copy2(B/name,source/name)
 shutil.copy2(A/'build.json',source/'build.json')
 # The build's actual source is recorded; do not silently call old code the alias repair.
 built_source=Path(json.loads((A/'build.json').read_text())['build'])/'Counterexample.lean'
 source_matches_build=built_source.read_bytes()==(B/'Counterexample.lean').read_bytes()
 wanted=[379,802]+list(range(22))
 with gzip.open(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as f:
  originals=[json.loads(line)for line in f]
 selected=[originals[i]for i in wanted]
 assert len(selected)==24 and len(set(wanted))==24
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
 for mode in ['off','gpu']:
  out=args.out/mode
  os.environ.update(GPU_SMT_CEX_MODE=mode,GPU_SMT_CEX_LOG=str(out/'goals.jsonl'))
  result=await capture['cell'](settings,'stock',out,snippets,build)
  result.update(own_mode=mode,provider_backend=args.backend,scope='24 actual source qualification, not complete benchmark or speedup.')
  (out/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
  cells.append(result)
  if result['state']!='complete' or result['returned']!=24:raise RuntimeError('Preserve partial qualification')
  if result['memory_watchdog']['error']or result['owned_live_descendants_after_shutdown']:raise RuntimeError('Resource monitoring/child retirement incomplete')
 summary=dict(source_ids=[x['proof_id']for x in snippets],source_matches_build=source_matches_build,
  preparation_seconds=preparation_seconds,provider_identity=provider,
  cells=[dict(mode=x['own_mode'],state=x['state'],returned=x['returned'])for x in cells],
  scope='Own off/on qualification. Final per-source outcomes/backtracking, GPU events, exact witnesses and all cleanup require result review before a full pair.')
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':asyncio.run(main())
