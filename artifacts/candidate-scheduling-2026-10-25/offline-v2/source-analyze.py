"""Existing-data first-success scheduling analysis; no Lean or solver process."""
from pathlib import Path
import argparse,collections,csv,gzip,heapq,json,re
ROOT=Path('/workspaces/repository')
INPUT=ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz'
NATIVE=ROOT/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off'
PAIRED=ROOT/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-layout-fixed-20261024T1650/analysis/paired-sources.csv'
def rows(path):
 with gzip.open(path,'rt')as f:return [json.loads(l)for l in f]
def strip_comments(text):
 out=[];i=0;depth=0;string=False
 while i<len(text):
  if depth:
   if text.startswith('/-',i):depth+=1;i+=2
   elif text.startswith('-/',i):depth-=1;i+=2
   else:
    if text[i]=='\n':out.append('\n')
    i+=1
  elif string:
   out.append(text[i])
   if text[i]=='\\'and i+1<len(text):out.append(text[i+1]);i+=2;continue
   if text[i]=='"':string=False
   i+=1
  elif text.startswith('/-',i):depth=1;out.append(' ');i+=2
  elif text.startswith('--',i):
   end=text.find('\n',i);i=len(text)if end<0 else end
  else:
   if text[i]=='"':string=True
   out.append(text[i]);i+=1
 if depth or string:raise ValueError('Unsupported unclosed input lexical region')
 return ''.join(out)
def simulate(records,order,workers,stop):
 waiting=collections.deque(order);active={};events=[];now=0.;spent=0.;solved=set();completed=[];cancelled=[]
 def fill():
  while len(active)<workers and waiting:
   sid=waiting.popleft();row=records[sid]
   if row['task']in solved:cancelled.append(dict(source_id=sid,kind='not_started',model_seconds=0.));continue
   active[sid]=(now,now+row['http_seconds'])
   heapq.heappush(events,(now+row['http_seconds'],sid))
 fill()
 while active:
  end,sid=heapq.heappop(events)
  if sid not in active:continue
  now=end;start,_=active.pop(sid);row=records[sid]
  spent+=now-start;completed.append(sid)
  if stop and row['valid']:
   solved.add(row['task'])
   for other,(begin,finish)in list(active.items()):
    if records[other]['task']==row['task']:
     spent+=now-begin
     cancelled.append(dict(source_id=other,kind='in_flight',model_seconds=now-begin))
     del active[other]
  fill()
 return dict(model_makespan_seconds=now,model_consumed_span_seconds=spent,
  completed_sources=len(completed),completed_valid_sources=sum(records[i]['valid']for i in completed),
  solved_tasks=len(solved)if stop else len({records[i]['task']for i in completed if records[i]['valid']}),
  solved_task_ids=sorted(solved)if stop else sorted({records[i]['task']for i in completed if records[i]['valid']}),
  cancelled_before_start=sum(x['kind']=='not_started'for x in cancelled),
  cancelled_in_flight=sum(x['kind']=='in_flight'for x in cancelled),
  cancelled_observed_timeouts=sum(records[x['source_id']]['status']=='timeout_error'for x in cancelled),
  cancelled_sources=cancelled)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=2)
 a=p.parse_args();a.out.mkdir(exist_ok=False)
 src=rows(INPUT);native={x['proof_id']:x for x in rows(NATIVE/'results.jsonl.gz')}
 with PAIRED.open()as f:paired={x['source_id']:x for x in csv.DictReader(f)}
 assert len(src)==len(native)==len(paired)==7808
 meta=rows(ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/task-prefix-counts.jsonl.gz')
 task_names={}
 for t in meta:
  if t['dataset']=='minif2f':
   names=re.findall(r'^\s*theorem\s+([^\s(:]+)',strip_comments(t['statement']),re.M)
   assert len(names)==1;task_names[t['task']]=names[0]
 assert len(task_names)==244
 records={};tasks=collections.defaultdict(list);missing_declarations=[]
 for index,row in enumerate(src):
  assert row['index']==index
  sid=f'minif2f-{index}';text=strip_comments(row['code'])
  declarations=re.findall(r'^\s*theorem\s+([^\s(:]+)',text,re.M)
  task=task_names[index//32];item=native[sid]
  if declarations!=[task]:
   if not declarations and row['code'].strip()=='None':
    assert item['status']=='lean_error';missing_declarations.append(sid)
   else:raise ValueError((sid,task,declarations))
  assert item['status']==paired[sid]['off_status']
  if item['status']=='valid':
   response=item['result'].get('response',{})
   assert not response.get('sorries')
   assert not any(m.get('severity')=='error'for m in response.get('messages',[]))
  rec=dict(source_id=sid,index=index,task=task,status=item['status'],valid=item['status']=='valid',
   http_seconds=float(paired[sid]['off_HTTP_seconds']),code_characters=len(text))
  records[sid]=rec;tasks[task].append(sid)
 assert len(tasks)==244 and all(len(v)==32 for v in tasks.values())
 # Verify task identity rather than assuming an arbitrary32-record grouping.
 assert all(len({records[f'minif2f-{i}']['task']for i in range(base,base+32)})==1 for base in range(0,7808,32))
 taskrows=[];original={};short={};oracle={}
 for task,ids in tasks.items():
  original[task]=sorted(ids,key=lambda i:records[i]['index'])
  short[task]=sorted(ids,key=lambda i:(records[i]['code_characters'],records[i]['index']))
  oracle[task]=sorted(ids,key=lambda i:(not records[i]['valid'],records[i]['http_seconds'],records[i]['index']))
  successes=[i for i in ids if records[i]['valid']]
  first=next((i for i,x in enumerate(original[task])if records[x]['valid']),None)
  work=sum(records[i]['http_seconds']for i in ids)
  oracle_cost=min(records[i]['http_seconds']for i in successes)if successes else work
  taskrows.append(dict(task=task,candidates=32,valid=len(successes),timeouts=sum(records[i]['status']=='timeout_error'for i in ids),
   cumulative_native_HTTP_seconds=work,original_first_success_rank=None if first is None else first+1,
   original_stop_first_span_seconds=sum(records[i]['http_seconds']for i in original[task][:first+1])if first is not None else work,
   hindsight_minimum_span_seconds=oracle_cost))
 groups=list(tasks)
 def flatten(order,interleave):
  return [order[t][k]for k in range(32)for t in groups]if interleave else [i for t in groups for i in order[t]]
 policies={}
 for name,order,interleave,stop in [
  ('all_candidates_original_order',original,False,False),
  ('stop_first_original_order',original,False,True),
  ('stop_first_short_code',short,False,True),
  ('round_robin_original_order',original,True,True),
  ('round_robin_short_code',short,True,True),
  ('hindsight_valid_fastest_first',oracle,True,True)]:
  policies[name]=simulate(records,flatten(order,interleave),a.workers,stop)
 expected=sorted(t for t,ids in tasks.items()if any(records[i]['valid']for i in ids))
 assert all(q['solved_task_ids']==expected for q in policies.values())
 curves={}
 for name,order in [('original',original),('short_code',short),('hindsight',oracle)]:
  curves[name]={str(k):sum(any(records[i]['valid']for i in ids[:k])for ids in order.values())for k in [1,2,4,8,16,32]}
 total=sum(r['http_seconds']for r in records.values());floor=sum(x['hindsight_minimum_span_seconds']for x in taskrows)
 worst=max((min(records[i]['http_seconds']for i in ids if records[i]['valid'])if any(records[i]['valid']for i in ids)else max(records[i]['http_seconds']for i in ids))for ids in tasks.values())
 result=dict(dataset='original released miniF2F244tasks x32candidates',source_count=7808,task_count=244,workers=a.workers,
  status_counts=dict(collections.Counter(r['status']for r in records.values())),solvable_tasks=len(expected),
  task_mapping='Existing244task metadata plus producer32-record layout, verified against every present theorem declaration. All18literalNone rejected candidates retained.',
  missing_declaration_source_ids=missing_declarations,
  native_whole_seconds=json.loads((NATIVE/'terminal.json').read_text())['whole_lifecycle_seconds'],
  cumulative_native_HTTP_seconds=total,timeout_HTTP_seconds=sum(r['http_seconds']for r in records.values()if r['status']=='timeout_error'),
  timeout_sources_in_solvable_tasks=sum(r['status']=='timeout_error'and r['task']in expected for r in records.values()),
  hindsight_minimum_cumulative_span_seconds=floor,
  hindsight_span_work_ratio=total/floor,
  idealized_service_model_makespan_lower_bound_seconds=max(floor/a.workers,worst),
  ordered_first_k_solved_task_counts=curves,policies=policies,
  scope='Offline replay of observed HTTP spans as fixed task costs, not CPU or measured performance. Hindsight uses unavailable outcome/time knowledge. Zero cancellation/prediction/setup overhead and unchanged per-candidate costs are optimistic modeling assumptions. No bound on physical whole service, no RL every-candidate equivalence, no claimed novelty for ordinary first-success scheduling.')
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 with(a.out/'tasks.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(taskrows[0]));w.writeheader();w.writerows(taskrows)
 (a.out/'source-features.json').write_text(json.dumps(list(records.values()),indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='policies'},indent=2))
 print(json.dumps({k:{x:y for x,y in v.items()if x not in ['cancelled_sources','solved_task_ids']}for k,v in policies.items()},indent=2))
if __name__=='__main__':main()
