"""Native first-success verification scheduling; no arithmetic oracle changes."""
from pathlib import Path
import argparse,asyncio,collections,datetime,gzip,json,os,psutil,runpy,sys,time,traceback
ROOT=Path('/workspaces/repository')
BASE=ROOT/'bench/lean-candidate-scheduling'
ART=ROOT/'artifacts/candidate-scheduling-2026-10-25'
ACTIVE_PROFILE=ROOT/'artifacts/lean-failure-profile-2026-10-25/full480'
OWNED_OUTPUT=None
def input_rows():
 with gzip.open(ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as f:return [json.loads(l)for l in f]
def record(path,event,**values):
 with path.open('a')as f:f.write(json.dumps(dict(event=event,time_ns=time.monotonic_ns(),**values),ensure_ascii=False)+'\n')
def install_scheduler(mode,out):
 import kimina_client
 from kimina_client.models import CheckResponse,ReplResponse
 original=kimina_client.AsyncKiminaClient
 strip=runpy.run_path(str(BASE/'analyze.py'))['strip_comments']
 predictor=runpy.run_path(str(BASE/'features.py'))if mode=='first-predicted'else None
 models=json.loads((ART/'crossfit/models.json').read_text())['models']if predictor else None
 class Client(original):
  async def check(self,snips,timeout=60,debug=False,reuse=True,infotree=None,batch_size=8,max_workers=5,show_progress=True):
   if not isinstance(snips,list)or not snips or not all(getattr(x,'id','').startswith('minif2f-')for x in snips):
    return await super().check(snips,timeout,debug,reuse,infotree,batch_size,max_workers,show_progress)
   groups=collections.defaultdict(list)
   for snip in snips:groups[int(snip.id.split('-')[1])//32].append(snip)
   if mode=='first-short':
    for group in groups.values():group.sort(key=lambda x:(len(strip(x.code)),int(x.id.split('-')[1])))
   if mode=='first-predicted':
    for task,group in groups.items():
     group.sort(key=lambda x:(-predictor['score'](x.code,models[task%5]),int(x.id.split('-')[1])))
   results={};semaphore=asyncio.Semaphore(max_workers);ledger=out/'scheduler-events.jsonl'
   async def task_group(task,items):
    winner=None
    for snip in items:
     if winner is not None:
      # A consumer cancellation is not a native rejection or a zero-cost proof.
      results[snip.id]=ReplResponse(id=snip.id,error='cancelled_after_checked_success:'+winner)
      record(ledger,'cancelled_before_start',source_id=snip.id,task_id=task,winner=winner)
      continue
     async with semaphore:
      record(ledger,'source_started',source_id=snip.id,task_id=task)
      response=await super(Client,self).check([snip],timeout,debug,reuse,infotree,1,1,False)
      assert len(response.results)==1 and response.results[0].id==snip.id
      result=response.results[0];results[snip.id]=result
      status=result.analyze().status.value
      record(ledger,'source_returned',source_id=snip.id,task_id=task,status=status)
      if status=='valid':
       raw=result.response or{}
       assert not raw.get('sorries')and not any(m.get('severity')=='error'for m in raw.get('messages',[]))
       winner=snip.id
       record(ledger,'task_solved',source_id=snip.id,task_id=task)
    record(ledger,'task_finished',task_id=task,winner=winner)
   await asyncio.gather(*(task_group(task,items)for task,items in groups.items()))
   assert set(results)=={s.id for s in snips}
   return CheckResponse(results=[results[s.id]for s in snips])
 kimina_client.AsyncKiminaClient=Client
 return original
async def main(args):
 global OWNED_OUTPUT
 # Preserve the sole existing collection. This is the user's resource invariant,
 # not a performance/novelty admission condition.
 if psutil.pid_exists(275822):
  owner=psutil.Process(275822)
  if abs(owner.create_time()-1792894799.05)<.01 and owner.status()!=psutil.STATUS_ZOMBIE:
   raise RuntimeError('Existing full480 diagnostic is live; do not start a second collection')
 if not(ACTIVE_PROFILE/'client-exit.json').exists():
  raise RuntimeError('First resolve the existing capture terminal/retirement evidence')
 done=json.loads((ACTIVE_PROFILE/'profile/terminal.json').read_text())
 if done.get('owned_live_descendants_after_shutdown'):raise RuntimeError('Existing capture still owns live descendants')
 d=runpy.run_path(str(ROOT/'bench/lean-counterexample/qualify.py'))
 capture,settings,build=d['capture'],d['args'],d['build']
 os.environ['GPU_SMT_CEX_MODE']='off'
 inputs=input_rows()
 ids=list(range(7808))if args.phase=='full'else[0,1,2,3,64,65,66,67]
 items=[dict(proof_id=f'minif2f-{i}',code=inputs[i]['code'])for i in ids]
 args.out.mkdir(exist_ok=False);OWNED_OUTPUT=args.out
 (args.out/'source').mkdir()
 for file in BASE.glob('*.py'):(args.out/'source'/file.name).write_bytes(file.read_bytes())
 (args.out/'selected.json').write_text(json.dumps(dict(ids=[x['proof_id']for x in items],phase=args.phase,input_changed=False),indent=2)+'\n')
 modes=['all','first-original','first-short']
 summaries=[];original_client=None
 import kimina_client
 for mode in modes:
  out=args.out/mode
  consumer_start=time.monotonic_ns()
  if mode!='all':original_client=install_scheduler(mode,out)
  try:
   value=await capture['cell'](settings,'stock',out,items,build)
  finally:
   if original_client is not None:kimina_client.AsyncKiminaClient=original_client;original_client=None
  value.update(consumer='all-candidate native'if mode=='all'else'first checked success per producer task',
   scheduler_policy=mode,actual_same_task_max_in_flight=1 if mode!='all'else None,
   scope='Same original native inputs and transport; no proof-state/certificate reuse. Pending siblings cancelled, not native failures. Not per-candidate RL rewards.')
  (out/'terminal.json').write_text(json.dumps(value,indent=2)+'\n')
  summaries.append(value)
  if value['state']!='complete'or value['returned']!=len(items)or value['memory_watchdog']['error']or value['owned_live_descendants_after_shutdown']:
   raise RuntimeError('Preserve actual failed or incomplete scheduler cell')
  # Keep original transport slots and distinguish actual responses from cancellations.
  rows=[json.loads(l)for l in(out/'results.jsonl').open()]
  consumer=[]
  for row in rows:
   error=row['result'].get('error','')
   if error.startswith('cancelled_after_checked_success:'):
    row=dict(row,status='cancelled_after_success',native_response_returned=False,winner=error.split(':',1)[1])
    row['result']=dict(row['result'],time=None)
   else:row=dict(row,native_response_returned=True)
   consumer.append(row)
  value['transport_slot_counts']=value['counts']
  value['consumer_counts']=dict(collections.Counter(row['status']for row in consumer))
  with gzip.open(out/'consumer-results.jsonl.gz','wt')as f:
   for row in consumer:f.write(json.dumps(row,ensure_ascii=False)+'\n')
  for path in list(out.iterdir()):
   if path.is_file()and path.suffix in ['.jsonl','.log']:
    data=path.read_bytes();compressed=gzip.compress(data,mtime=0)
    assert gzip.decompress(compressed)==data
    path.with_name(path.name+'.gz').write_bytes(compressed);path.unlink()
  value['consumer_complete_lifecycle_seconds']=(time.monotonic_ns()-consumer_start)/1e9
  value['consumer_cost_scope']='Includes model loading, source ranking, native transport lifecycle, queued cancellation, result mapping and raw compression. Offline training/shared input materialization reported separately.'
  (out/'terminal.json').write_text(json.dumps(value,indent=2)+'\n')
  print(json.dumps(dict(event='cell_complete',mode=mode,whole=value['whole_lifecycle_seconds'],complete_consumer=value['consumer_complete_lifecycle_seconds'])),flush=True)
 (args.out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--phase',choices=['qualification','full'],required=True)
 parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
 code=0;error=None
 try:asyncio.run(main(args))
 except BaseException:
  code=1;error=traceback.format_exc();raise
 finally:
  if OWNED_OUTPUT is not None:(OWNED_OUTPUT/'client-exit.json').write_text(json.dumps(dict(exit=code,error=error,pid=os.getpid(),UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
