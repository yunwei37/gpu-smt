"""Offline existing complete-capture attribution. No native workload or runtime change."""
from pathlib import Path
import collections,datetime,gzip,json,os
os.sched_setaffinity(0,{11})
R=Path('/workspaces/repository')
B=R/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
O=Path(__file__).parent
load=lambda p:json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
captures={n:load(B/n/'capture.json.gz')for n in ['native','prepared']}
# Match native registration/retirement records. Parent preparation ends at its
# handoff into backend-owned idle state, not at physical parent retirement.
register={};release={};phase_events=[];bytes_read=0;lines=0
with gzip.open(B/'driver.log.gz','rt')as f:
 for line in f:
  lines+=1;bytes_read+=len(line.encode())
  row=json.loads(line);a=row.get('fields',{});msg=a.get('message')
  if msg not in ['register active process','release active process ownership','backend lifecycle event']:continue
  tm=datetime.datetime.fromisoformat(row['timestamp'].replace('Z','+00:00')).timestamp()
  if msg=='backend lifecycle event':phase_events.append((tm,a));continue
  key=(a['pid'],a['start_ticks'])
  target=register if msg=='register active process'else release
  assert key not in target,key
  target[key]=tm
def union(spans):
 last=None;total=0
 for lo,hi in sorted(spans):
  assert hi>=lo
  if last is None:last=[lo,hi]
  elif lo<=last[1]:last[1]=max(last[1],hi)
  else:total+=last[1]-last[0];last=[lo,hi]
 return total+(last[1]-last[0]if last else 0)
output={'scope':'existing complete own-engine component pair; no matched warm result; self-review','cells':{},
'logging_retained':{'uncompressed_driver_bytes':bytes_read,'driver_rows':lines,'wall_overhead_seconds':None,
'reason':'bytes/row counts are not CPU or elapsed overhead; matched log-on/off control remains required'}}
for name,c in captures.items():
 rows=c['results'];term=load(B/name/'terminal.json');whole=term['external_cell_seconds']
 parent_ids={json.loads(e['detail'])['parent_pid']for v in rows for a in v['attempts']for e in a['backend_events']if e['stage']=='prepared_ready'}
 attempts=[];preparations=[];fallbacks=[]
 for v in rows:
  for a in v['attempts']:
   proc=[(p['pid'],p['start_ticks'])for p in a['processes']]
   kids=[k for k in proc if k[0]not in parent_ids]
   # At most one fresh/prototype process normally, but fallback can replace it.
   spans=[(register[k],release[k])for k in kids]
   assert all(k in register and k in release for k in proc)
   events=[e['stage']for e in a['backend_events']]
   item={'id':v['id'],'final_status':v['outcome']['status'],'attempt_status':a['status'],
     'exclusive':a['exclusive'],'preempted':a['preemption_rss_bytes']is not None,
     'seconds':a['elapsed_seconds'],'spans':spans,'fallback':events.count('fresh_fallback')>0}
   attempts.append(item)
   if item['fallback']:fallbacks.append(item)
   for k in proc:
    if k[0]in parent_ids:preparations.append((k,register[k],release[k]))
 unique_prep={k:(lo,hi)for k,lo,hi in preparations}
 groups={
  'exclusive_native_execution':[a for a in attempts if a['exclusive']],
  'final_resource_failure_native_execution':[a for a in attempts if a['final_status']=='resource_exhausted'],
  'final_timeout_native_execution':[a for a in attempts if a['final_status']=='timeout'],
  'nonexclusive_preempted_native_execution':[a for a in attempts if a['preempted']and not a['exclusive']],
  'fresh_fallback_attempts':fallbacks,
  'accepted_native_execution':[a for a in attempts if a['final_status']=='accepted'],
  'rejected_native_execution':[a for a in attempts if a['final_status']=='rejected']}
 ranked=[]
 for label,items in groups.items():
  spans=[sp for a in items for sp in a['spans']]
  ranked.append({'category':label,'attempts':len(items),'unique_sources':len({a['id']for a in items}),
  'registered_interval_union_seconds':union(spans),'overlapping_attempt_wall_sum_seconds':sum(a['seconds']for a in items),
  'union_fraction_of_external_cell':union(spans)/whole})
 prep_spans=list(unique_prep.values())
 ranked.append({'category':'parent_preparation_registration_to_handoff','preparations':len(unique_prep),
 'registered_interval_union_seconds':union(prep_spans),'overlapping_attempt_wall_sum_seconds':None,
 'union_fraction_of_external_cell':union(prep_spans)/whole})
 # Exact occupied-child count integration from lifecycle events, not CPU usage.
 endpoints=[]
 for a in attempts:
  for lo,hi in a['spans']:endpoints.extend([(lo,1),(hi,-1)])
 endpoints.sort();hist=collections.defaultdict(float);active=0;previous=endpoints[0][0]
 for t,delta in endpoints:
  hist[active]+=t-previous;active+=delta;previous=t
 assert active==0
 native_span=endpoints[-1][0]-endpoints[0][0]
 hist['outside_native_span']=max(0,whole-native_span)
 sample_hist=collections.defaultdict(float);sample_count=collections.Counter();peak=0;observed_cpu={}
 last=None
 with gzip.open(B/name/'rss-cpu.jsonl.gz','rt')as f:
  for line in f:
   row=json.loads(line);tm=row['seconds'];leaders=[p for p in row['registered_leaders']if p['identity']['pid']not in parent_ids]
   count=len(leaders);sample_count[count]+=1;peak=max(peak,row['aggregate_rss_bytes'])
   if last:sample_hist[last[1]]+=tm-last[0]
   last=(tm,count)
   for p in row['registered_leaders']:
    key=(p['identity']['pid'],p['identity']['start_ticks'])
    ticks=p.get('cpu_ticks')
    if ticks is not None:observed_cpu[key]=max(observed_cpu.get(key,0),sum(ticks.values()))
 # Source correlation table; queue sums deliberately not treated as whole-wall work.
 heavy=sorted([{'id':v['id'],'status':v['outcome']['status'],'attempt_seconds_sum':sum(a['elapsed_seconds']for a in v['attempts']),
 'attempts':len(v['attempts']),'exclusive_attempts':sum(a['exclusive']for a in v['attempts'])}for v in rows],
 key=lambda x:x['attempt_seconds_sum'],reverse=True)
 output['cells'][name]={'external_cell_seconds':whole,'lifecycle_seconds':c['lifecycle_seconds'],
 'external_minus_lifecycle_seconds':whole-c['lifecycle_seconds'],'ranked_overlapping_categories':sorted(ranked,key=lambda x:-x['registered_interval_union_seconds']),
 'occupied_native_children_seconds_by_count':dict(hist),'sampled_registered_children_seconds_by_count':dict(sample_hist),
 'sample_counts_by_registered_children':dict(sample_count),'sampled_peak_aggregate_rss_bytes':peak,
 'occupied_child_slot_seconds':sum(int(k)*v for k,v in hist.items()if isinstance(k,int)),
 'occupied_slot_fraction_of_4cpu_cell':sum(int(k)*v for k,v in hist.items()if isinstance(k,int))/(4*whole),
 'observed_registered_process_cpu_seconds_lower_bound':sum(observed_cpu.values())/os.sysconf('SC_CLK_TCK'),
 'cpu_scope':'max sampled cumulative process ticks; misses short unsampled processes/final tails and idle unregistered-parent CPU; not exhaustive CPU or utilization',
 'top20_attempt_cost_sources':heavy[:20],'parent_preparations':len(unique_prep),
 'fallback_event_rows':sum(e['stage']=='fresh_fallback'for v in rows for a in v['attempts']for e in a['backend_events']),
 'fallback_attempts':len(fallbacks),
 'not_separated':['within-native imports versus elaboration/checking','mutex/admission waiting versus idle natural gaps','watchdog/procscan CPU','logging CPU/wall'],
 'warning':'Categories overlap. Never add their seconds or infer removable/Amdahl time. Occupied native children are not CPU utilization or a counterfactual warm result.'}

# Exact historical warm cell named in the user request. Different AS/retry
# contracts: retain the comparison, never call it a matched final baseline.
warm=R/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off'
term=load(warm/'terminal.json')
with gzip.open(warm/'results.jsonl.gz','rt')as f:old={x['proof_id']:x for x in map(json.loads,f)}
request_spans=collections.defaultdict(list)
with gzip.open(warm/'http.jsonl.gz','rt')as f:
 for line in f:
  row=json.loads(line)
  if row.get('event')!='response':continue
  snippets=json.loads(row['request']).get('snippets',[])
  if len(snippets)==1 and snippets[0]['id']in old:
   request_spans[snippets[0]['id']].append((row['start_ns']/1e9,row['end_ns']/1e9))
assert len(old)==len(request_spans)==7808 and all(len(x)==1 for x in request_spans.values())
mapping={'valid':'accepted','lean_error':'rejected','timeout_error':'timeout','resource_failure':'resource_exhausted'}
warm_groups={}
for status in sorted({v['status']for v in old.values()}):
 ids=[i for i,v in old.items()if v['status']==status]
 spans=[span for i in ids for span in request_spans[i]]
 warm_groups[status]={'sources':len(ids),'HTTP_envelope_sum_seconds':sum(hi-lo for lo,hi in spans),
 'HTTP_envelope_union_seconds':union(spans)}
changes={}
for name,c in captures.items():
 changes[name]=[{'id':v['id'],'historical_warm':mapping[old[v['id']]['status']],'engine':v['outcome']['status']}
 for v in c['results']if mapping[old[v['id']]['status']]!=v['outcome']['status']]
fallback_detail=collections.defaultdict(lambda:{'attempts':0,'overlapping_attempt_wall_sum_seconds':0,'exclusive_attempts':0})
for v in captures['prepared']['results']:
 for a in v['attempts']:
  for e in a['backend_events']:
   if e['stage']=='fresh_fallback':
    g=fallback_detail[e['detail']];g['attempts']+=1;g['overlapping_attempt_wall_sum_seconds']+=a['elapsed_seconds'];g['exclusive_attempts']+=a['exclusive']
output['historical_warm']={'source':str(warm.relative_to(R)),'whole_lifecycle_seconds':term['whole_lifecycle_seconds'],
'workers':term['source_concurrency'],'per_process_AS_bytes':term['per_native_repl_address_limit_bytes'],
'aggregate_memory_bytes':term['aggregate_memory_budget_bytes'],'counts':term['counts'],'HTTP_groups_overlapping':warm_groups,
'engine_status_differences':changes,'prepared_elapsed_over_historical_warm':output['cells']['prepared']['external_cell_seconds']/term['whole_lifecycle_seconds'],
'warning':'Historical only:2workers/24GiB-AS versus4workers/no-AS/exclusive retries; different complete cost boundaries and fixed source order. Accepted set is not equal. Do not claim engine benefit or infer causal slowdown from this ratio.'}
output['prepared_fallback_details']=dict(fallback_detail)

(O/'analysis.json').write_text(json.dumps(output,indent=2)+'\n')
for n,c in output['cells'].items():
 print(n,json.dumps({k:v for k,v in c.items()if k!='top20_attempt_cost_sources'},indent=2))
print('logging',output['logging_retained'])
