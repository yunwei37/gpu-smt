"""Analyze closed native CPU/GPU cells, real candidate spans and batch evidence."""
from pathlib import Path
import argparse,collections,gzip,json,math
HEADER='import Mathlib\nimport Aesop\n'
def rows(p):
 with(gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as f:return [json.loads(l)for l in f]
def retained_file(root,name):
 return next((p for p in [root/name,root/(name+'.gz')]if p.exists()),None)
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
 timing=rows(retained_file(p,'candidate-times.jsonl'))
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
 calls_path=retained_file(backend,'support-calls.jsonl')
 calls=rows(calls_path)if calls_path else[]
 batches={tuple(x['reply']['batch_ids']):x['reply']for x in calls if'batch_ids'in x['reply']}
 return {'terminal':terminal,'responses':responses,'byidx':byidx,'calls':calls,'batches':list(batches.values()),'missing_candidate_spans':missing,'unmatched_candidate_spans':unmatched}
def gpu_job_evidence(root,name):
 backend=root/('rep1-'+name+'-backend')
 path=retained_file(backend,'support-calls.jsonl.batches')
 if path is None:return {'available':False,'scope':'No job-event stream; received-result counters do not establish all submitted/cancelled GPU work.'}
 events=rows(path)
 submitted={x['job_id']:x for x in events if x['event']=='submit'}
 results={x['job_id']:x for x in events if x['event']=='result'}
 retired={x['job_id']:x for x in events if x['event']=='job_retired'}
 cancelled={x['job_id']for x in events if x['event']in ['cancel_withdrawn_member','cancel_no_live_clients']}
 return {'available':True,'submitted_jobs':len(submitted),'result_jobs':len(results),
  'cancel_requested_jobs':len(cancelled),'client_retired_jobs':len(retired),
  'submitted_batch_size_histogram':dict(collections.Counter(len(x['batch_ids'])for x in submitted.values())),
  'submitted_distinct_source_histogram':dict(collections.Counter(str(x.get('batch_distinct_sources','unknown'))for x in submitted.values())),
  'server_reported_result_solver_seconds':sum(x.get('batch_solver_seconds_shared')or 0 for x in results.values()),
  'submitted_without_result_ids':sorted(set(submitted)-set(results)),
  'submitted_without_client_retirement_ids':sorted(set(submitted)-set(retired)),
  'summed_client_batch_retirement_wall_seconds':sum((x['end_ns']-x['batch_client_start_ns'])/1e9 for x in retired.values()),
  'dispatcher_retirement':[x for x in events if x['event']=='dispatcher_retired'],
  'cancelled_job_device_compute_seconds':None,
  'scope':'All submitted jobs, including discarded/cancelled batches. Server solve_time exists only for result records. Client batch/RPC/retirement wall is not device compute or a disjoint portion of native whole wall. Unknown cancelled device time is not zero.'}

def tail_summary(c,ids):
 spans=[c['byidx'][i]for i in ids if i in c['byidx']];times=[(x['end_ns']-x['start_ns'])/1e9 for x in spans]
 windows=[(x['start_ns'],x['end_ns'])for x in spans]
 overlap=[x for x in c['calls']if any(x['start_ns']<b and x['end_ns']>a for a,b in windows)]
 return {'candidate_count':len(ids),'observed_spans':len(spans),'missing_span_indices':[i for i in ids if i not in c['byidx']],'service_span_seconds':spread(times),'sum_overlapping_service_seconds':sum(times),'occupied_interval_union_seconds':intervals_union(windows),'backend_calls_overlapping_selected_service_intervals':len(overlap),'scope':'Actual command task entry to return, not asynchronous reclamation attribution. Whole cell includes final retirement. Interval union is occupancy, not a removable critical-path cost; backend overlap is group-level evidence, never uniquely assigned to a candidate without an ID.'}

def load_phase_profile(inputs):
    # The retained all-call profile is only joined to its original complete
    # source cohort. Smaller qualification subsets are not treated as full data.
    root=Path(__file__).resolve().parents[3]
    artifact=root/'artifacts/linarith-oracle-2026-10-17'
    original=rows(artifact/'input-top1000.jsonl')
    if inputs!=original:return None
    path=artifact/'gpu-stage/full1000-baseline/recovered-cost-analysis.json.gz'
    if not path.exists():return None
    with gzip.open(path,'rt')as f:profile=json.load(f)
    byidx={x['index']:x for x in profile['per_source']}
    if len(byidx)!=len(profile['per_source']):raise ValueError('duplicate profile source index')
    for i,x in byidx.items():
        if inputs[i]['proof_id']!=x['proof_id']:raise ValueError('profile/source ID disagreement')
    return {'path':str(path.relative_to(root)),'byidx':byidx,'raw':profile}

def phase_profile_tail(profile,ids):
    if profile is None:return None
    total=collections.Counter();missing=[]
    for i in ids:
        source=profile['byidx'].get(i)
        if source is None:missing.append(i)
        else:total.update(source['component_cpu_seconds'])
    unknown=collections.Counter()
    for call in profile['raw']['calls']:
        if call['index']is None:unknown.update(call['phase_cpu_seconds'])
    bindings=profile['raw']['unlabelled_requests_wave_binding']
    intersects=any(set(x['candidate_indices'])&set(ids)for x in bindings)
    return {
        'profile':profile['path'],
        'selection': 'Real candidate task-wall ranking from the named primary method; phase counters from the separate complete native baseline profile, joined by original index and proof_id.',
        'matched_sources':len(ids)-len(missing),'missing_profile_indices':missing,
        'native_profile_component_CPU_seconds':dict(total),
        'native_profile_external_LP_CPU_seconds':total['fp_solve']+total['exact_lp'],
        'native_profile_preprocess_linearize_CPU_seconds':total['lean_preprocess']+total['lean_linearize'],
        'native_profile_product_proof_CPU_seconds':total['lean_products'],
        'native_profile_certificate_CPU_seconds':total['lean_certificate']+total['lean_direct_check'],
        'unlabelled_profile_call_count':len(bindings),
        'unlabelled_calls_may_intersect_selected_sources':intersects,
        'conservative_unassigned_component_CPU_upper_addition':dict(unknown)if intersects else{},
        'profile_whole_seconds':profile['raw']['terminal']['whole_ns']/1e9,
        'profile_predates_arithmetic_header_correction':True,
        'scope':'Earlier diagnostic-header workload composition, not a clean-header phase decomposition, measured GPU-stage CPU or primary per-source elapsed decomposition. Do not divide CPU counters by primary wall, sum parent/child phases as disjoint elapsed, or call these counters causal GPU savings. Missing labels are bounded, never assigned to an invented candidate.'
    }

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--input',type=Path,default=Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'));p.add_argument('--limit',type=int,default=0);p.add_argument('--methods',nargs='+',default=['fast-hybrid','oracle-highs','oracle-gpu']);p.add_argument('--historical-phase-profile',action='store_true',help='Explicitly attach the old stacked-header profile; never current cell attribution');a=p.parse_args()
 inputs=rows(a.input)
 if a.limit:inputs=inputs[:a.limit]
 phase_profile=load_phase_profile(inputs) if a.historical_phase_profile else None
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
  out['methods'][n]={'whole_seconds':c['terminal']['whole_ns']/1e9,'native_reference_ratio':ref['terminal']['whole_ns']/c['terminal']['whole_ns'],'counts':c['terminal']['counts'],'missing_candidate_span_indices':c['missing_candidate_spans'],'unmatched_candidate_spans':c['unmatched_candidate_spans'],'outcome_differences':verdict,'full_native_JSON_differences':changes,'non_message_differences':non_message,'backend_requests':len(c['calls']),'backend_request_counter_scope':'Accepted connection records, including unparsed/aborted input; not all are LP solves.','backend_complete_parsed_requests':sum(isinstance(x.get('input'),dict)for x in c['calls']),'backend_errors':sum('error'in x['reply']for x in c['calls']),'GPU_batches':len(c['batches']),'GPU_batch_size_histogram':dict(collections.Counter(x['batch_size']for x in c['batches'])),'GPU_unique_batch_solver_seconds':sum(x.get('batch_solver_seconds_shared')or 0 for x in c['batches']),'candidate_service_seconds':spread([(x['end_ns']-x['start_ns'])/1e9 for x in c['byidx'].values()]),'terminal':c['terminal']}
 for n in cells:out['methods'][n]['GPU_job_events']=gpu_job_evidence(a.root,n)
 for selected,refcell in cells.items():
  rank=sorted(refcell['byidx'],key=lambda i:refcell['byidx'][i]['end_ns']-refcell['byidx'][i]['start_ns'],reverse=True)
  out['tails'][selected]={}
  for fraction in [.01,.10]:
   count=math.ceil(len(inputs)*fraction);ids=rank[:count]
   out['tails'][selected][str(fraction)]={'selected_on':selected,'complete_selection_coverage':not refcell['missing_candidate_spans'],'selection_missing_indices':refcell['missing_candidate_spans'],'indices':ids,'proof_ids':[inputs[i]['proof_id']for i in ids],'methods':{n:tail_summary(c,ids)for n,c in cells.items()},'native_baseline_phase_profile':phase_profile_tail(phase_profile,ids)}
 (a.root/'paired-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='tails'},indent=2))
if __name__=='__main__':main()
