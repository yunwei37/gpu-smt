"""One native diagnostic group; fixed real baseline-selected source IDs."""
from pathlib import Path
import argparse,asyncio,datetime,gzip,json,os,runpy,shutil,sys,traceback
R=Path('/workspaces/repository');B=R/'bench/lean-failure-profile';A=R/'artifacts/lean-failure-profile-2026-10-25'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
def rows(p):
 with gzip.open(p,'rt')as f:return [json.loads(l)for l in f]
async def main(args):
 d=runpy.run_path(str(R/'bench/lean-counterexample/qualify.py'))
 capture,settings,build=d['capture'],d['args'],d['build']
 os.environ['GPU_SMT_CEX_MODE']='off'
 native=Path(json.loads((A/'build.json').read_text())['original'])
 profiled=Path(json.loads((A/'build.json').read_text())['binary'])
 cohort=json.loads((A/'cohort.json').read_text())
 source=rows(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz')
 raw=rows(R/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off/results.jsonl.gz')
 statuses={x['proof_id']:x['status']for x in raw}
 pair=__import__('csv').DictReader((R/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/analysis/paired-sources.csv').open())
 times={x['source_id']:float(x['off_HTTP_seconds'])for x in pair}
 selected=cohort['selected_ids']
 if args.phase=='preflight':
  ordinary=sorted((i for i in selected if statuses[i]=='lean_error'),key=lambda i:times[i])[:18]
  timeout=min(cohort['native_timeout_ids'],key=lambda i:int(i.split('-')[1]))
  allocation=min((i for i in selected if statuses[i]=='resource_failure'),key=lambda i:times[i])
  selected=['minif2f-0','minif2f-1','minif2f-289','minif2f-291']+ordinary+[timeout,allocation]
  assert len(set(selected))==24
 items=[dict(proof_id=i,code=source[int(i.split('-')[1])]['code'])for i in selected]
 args.out.mkdir(exist_ok=False)
 (args.out/'selected.json').write_text(json.dumps(dict(ids=selected,baseline_statuses={i:statuses[i]for i in selected},baseline_HTTP_seconds={i:times[i]for i in selected}),indent=2)+'\n')
 src=args.out/'source';src.mkdir()
 for p in B.glob('*'):
  if p.is_file():shutil.copy2(p,src/p.name)
 shutil.copy2(A/'build.json',src/'build.json')
 if args.reuse_native:
  if args.phase!='preflight':raise ValueError('Only reuse the completed native qualification control')
  term=json.loads((args.reuse_native/'terminal.json').read_text())
  control=rows(args.reuse_native/'results.jsonl.gz')
  if term['state']!='complete'or term['memory_watchdog']['error']or term['owned_live_descendants_after_shutdown']:raise RuntimeError('Native control not complete/retired')
  assert [x['proof_id']for x in control]==selected
  assert term['source_concurrency']==2 and term['per_native_repl_address_limit_bytes']==24*1024**3
  (args.out/'reused-native.json').write_text(json.dumps(dict(directory=str(args.reuse_native),whole_lifecycle_seconds=term['whole_lifecycle_seconds'],reason='Same unchanged native control retained after diagnostic-only C ABI repair.'),indent=2)+'\n')
 modes=['native','profile']if args.phase=='preflight'and not args.reuse_native else['profile']
 summary=[]
 for mode in modes:
  out=args.out/mode
  settings.repl=native if mode=='native'else profiled
  if mode=='profile':
   profiles=args.out/'profiles';profiles.mkdir()
   os.environ['GPU_SMT_NATIVE_PROFILE_DIRECTORY']=str(profiles)
  else:os.environ.pop('GPU_SMT_NATIVE_PROFILE_DIRECTORY',None)
  print(json.dumps(dict(event='cell_start',mode=mode,sources=len(items),pid=os.getpid())),flush=True)
  result=await capture['cell'](settings,'stock',out,items,build)
  result.update(own_diagnostic='stock runtime profileit boundaries'if mode=='profile'else'untouched native control',phase=args.phase)
  (out/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
  summary.append(result)
  if result['state']!='complete'or result['returned']!=len(items)or result['memory_watchdog']['error']or result['owned_live_descendants_after_shutdown']:
   raise RuntimeError('Retain incomplete diagnostic and resource/retirement failures')
  for p in list(out.iterdir()):
   if p.is_file()and p.suffix in ['.jsonl','.log']:
    data=p.read_bytes();z=gzip.compress(data,mtime=0);assert gzip.decompress(z)==data
    p.with_name(p.name+'.gz').write_bytes(z);p.unlink()
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(dict(event='group_complete',sources=len(items),modes=modes)),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=['preflight','full'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--reuse-native',type=Path);args=p.parse_args()
 code=0;error=None
 try:asyncio.run(main(args))
 except BaseException as ex:
  code=ex.code if isinstance(ex,SystemExit)and isinstance(ex.code,int)else 1;error=traceback.format_exc();raise
 finally:
  if args.out.exists():(args.out/'client-exit.json').write_text(json.dumps(dict(exit=code,error=error,pid=os.getpid(),finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
