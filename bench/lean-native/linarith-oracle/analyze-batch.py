"""Analyze closed native CPU/GPU cells, real candidate spans and batch evidence."""
from pathlib import Path
import argparse,collections,gzip,json,math
HEADER='import Mathlib\nimport Aesop\n'
def rows(p):
 with(gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as f:return [json.loads(l)for l in f]
def intervals_union(xs):
 end=None;total=0
 for a,b in sorted(xs):
  if end is None or a>end:total+=b-a;end=b
  elif b>end:total+=b-end;end=b
 return total/1e9
def spread(xs):
 if not xs:return None
 ys=sorted(xs);n=len(ys)
 return {'count':n,'min':ys[0],'median':ys[n//2],'p90':ys[int(.9*(n-1))],'p99':ys[int(.99*(n-1))],'max':ys[-1]}
def cell(root,name,inputs):
 p=root/('rep1-'+name);terminal=json.loads((p/'terminal.json').read_text())
 if terminal['state']!='complete' or terminal['attempts']!=len(inputs):raise ValueError('complete fixed-cohort cell required: '+name)
 responses=rows(p/'responses.jsonl.gz');assert len(responses)==len(inputs)
 mapping=collections.defaultdict(list)
 for i,x in enumerate(inputs):
  assert x['code'].startswith(HEADER)
  mapping['\n\n'+x['code'][len(HEADER):]].append(i)
 timing=rows(p/'candidate-times.jsonl')
 duplicate_sources={k:len(v)for k,v in mapping.items()if len(v)>1}
 byidx={};unmatched=[]
 for x in timing:
  ids=mapping.get(x['source'],[])
  if len(ids)!=1:unmatched.append({'source_matches':len(ids)});continue
  i=ids[0]
  if i in byidx:raise ValueError('duplicate job timing for source '+str(i))
  assert x['end_ns']>=x['start_ns'];byidx[i]=x
 missing=sorted(set(range(len(inputs)))-set(byidx))
 backend=root/('rep1-'+name+'-backend')
 if(backend/'terminal.json').exists():terminal=json.loads((backend/'terminal.json').read_text())
 calls=rows(backend/'support-calls.jsonl')if(backend/'support-calls.jsonl').exists()else[]
 batches={tuple(x['reply']['batch_ids']):x['reply']for x in calls if'batch_ids'in x['reply']}
 return {'terminal':terminal,'responses':responses,'byidx':byidx,'calls':calls,'batches':list(batches.values()),'missing_candidate_spans':missing,'unmatched_candidate_spans':unmatched}
def tail_summary(c,ids):
 spans=[c['byidx'][i]for i in ids if i in c['byidx']];times=[(x['end_ns']-x['start_ns'])/1e9 for x in spans]
 windows=[(x['start_ns'],x['end_ns'])for x in spans]
 overlap=[x for x in c['calls']if any(x['start_ns']<b and x['end_ns']>a for a,b in windows)]
 return {'candidate_count':len(ids),'observed_spans':len(spans),'missing_span_indices':[i for i in ids if i not in c['byidx']],'service_span_seconds':spread(times),'sum_overlapping_service_seconds':sum(times),'occupied_interval_union_seconds':intervals_union(windows),'backend_calls_overlapping_selected_service_intervals':len(overlap),'scope':'Actual command task entry to return, not asynchronous reclamation attribution. Whole cell includes final retirement. Interval union is occupancy, not a removable critical-path cost; backend overlap is group-level evidence, never uniquely assigned to a candidate without an ID.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--input',type=Path,default=Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'));p.add_argument('--limit',type=int,default=0);p.add_argument('--methods',nargs='+',default=['fast-hybrid','oracle-highs','oracle-gpu']);a=p.parse_args()
 inputs=rows(a.input)
 if a.limit:inputs=inputs[:a.limit]
 cells={n:cell(a.root,n,inputs)for n in a.methods};ref=cells['fast-hybrid'];out={'count':len(inputs),'methods':{},'tails':{},'scope':'Root self-review. Closed real native cells, exact IDs and actual per-candidate spans. No GPU claim from numeric-only replay.'}
 for n,c in cells.items():
  changes=[];verdict=[];non_message=[]
  for i,(x,y)in enumerate(zip(c['responses'],ref['responses'])):
   assert x['proof_id']==y['proof_id']==inputs[i]['proof_id']
   if x['outcome']!=y['outcome']:verdict.append(i)
   if x['response']!=y['response']:
    changes.append(i)
    without_messages=lambda v:{key:value for key,value in v.items()if key!='messages'}if isinstance(v,dict)else v
    if without_messages(x['response'])!=without_messages(y['response']):non_message.append(i)
  out['methods'][n]={'whole_seconds':c['terminal']['whole_ns']/1e9,'native_reference_ratio':ref['terminal']['whole_ns']/c['terminal']['whole_ns'],'counts':c['terminal']['counts'],'missing_candidate_span_indices':c['missing_candidate_spans'],'unmatched_candidate_spans':c['unmatched_candidate_spans'],'outcome_differences':verdict,'full_native_JSON_differences':changes,'non_message_differences':non_message,'backend_requests':len(c['calls']),'backend_errors':sum('error'in x['reply']for x in c['calls']),'GPU_batches':len(c['batches']),'GPU_batch_size_histogram':dict(collections.Counter(x['batch_size']for x in c['batches'])),'GPU_unique_batch_solver_seconds':sum(x.get('batch_solver_seconds_shared')or 0 for x in c['batches']),'candidate_service_seconds':spread([(x['end_ns']-x['start_ns'])/1e9 for x in c['byidx'].values()]),'terminal':c['terminal']}
 for selected,refcell in cells.items():
  rank=sorted(refcell['byidx'],key=lambda i:refcell['byidx'][i]['end_ns']-refcell['byidx'][i]['start_ns'],reverse=True)
  out['tails'][selected]={}
  for fraction in [.01,.10]:
   count=math.ceil(len(inputs)*fraction);ids=rank[:count]
   out['tails'][selected][str(fraction)]={'selected_on':selected,'complete_selection_coverage':not refcell['missing_candidate_spans'],'selection_missing_indices':refcell['missing_candidate_spans'],'indices':ids,'proof_ids':[inputs[i]['proof_id']for i in ids],'methods':{n:tail_summary(c,ids)for n,c in cells.items()}}
 (a.root/'paired-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='tails'},indent=2))
if __name__=='__main__':main()
