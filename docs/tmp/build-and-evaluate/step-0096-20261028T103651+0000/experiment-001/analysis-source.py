
import pathlib,json,gzip,collections,statistics,datetime
r=pathlib.Path('/workspaces/repository')
s=r/pathlib.Path('/tmp/gpu-smt-step0096-path.txt').read_text().strip()/'experiment-001'
a=r/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/prepared'
cap=json.loads(gzip.decompress((a/'capture.json.gz').read_bytes()))
budget=cap['resources']['memory_bytes']
exclusive={}
ordinary=[]
for row in cap['results']:
 for i,attempt in enumerate(row['attempts']):
  if attempt['exclusive']:
   value={'id':row['id'],'attempt':i,'final_status':row['outcome']['status'],
          'status':attempt['status'],'seconds':attempt['elapsed_seconds'],
          'peak_lower_bound_bytes':attempt['peak_rss_bytes'],
          'preemption_total_bytes':attempt.get('preemption_rss_bytes'),
          'processes':attempt['processes'],'samples':0,'alone_samples':0,
          'aggregate_headroom_min_bytes':None,'headroom_counts':collections.Counter()}
   for p in attempt['processes']:
    key=(p['pid'],p['start_ticks']);assert key not in exclusive;exclusive[key]=value
  elif attempt['status']in ['accepted','rejected']and attempt['peak_rss_bytes']>0:
   ordinary.append(attempt['peak_rss_bytes'])
rows=list({id(x):x for x in exclusive.values()}.values())
sample_count=0;unknown_exclusive_samples=0
thresholds=[256*1024**2,1024**3,2*1024**3,4*1024**3,8*1024**3,16*1024**3]
for line in gzip.decompress((a/'rss-cpu.jsonl.gz').read_bytes()).splitlines():
 sample=json.loads(line);sample_count+=1
 leaders=sample['registered_leaders']
 active=[]
 for leader in leaders:
  p=leader['identity'];key=(p['pid'],p['start_ticks'])
  if key in exclusive:active.append(exclusive[key])
 for value in {id(v):v for v in active}.values():
  value['samples']+=1
  if len(leaders)==1:
   value['alone_samples']+=1
   headroom=max(0,budget-sample['aggregate_rss_bytes'])
   value['aggregate_headroom_min_bytes']=min(value['aggregate_headroom_min_bytes'] or headroom,headroom)
   for n in thresholds:
    if headroom>=n:value['headroom_counts'][str(n)]+=1
# Correct min with a separately collected sequence; zero is a real observation.
for value in rows:value['aggregate_headroom_min_bytes']=None
for line in gzip.decompress((a/'rss-cpu.jsonl.gz').read_bytes()).splitlines():
 sample=json.loads(line);leaders=sample['registered_leaders']
 if len(leaders)!=1:continue
 p=leaders[0]['identity'];value=exclusive.get((p['pid'],p['start_ticks']))
 if value is not None:
  headroom=max(0,budget-sample['aggregate_rss_bytes'])
  before=value['aggregate_headroom_min_bytes']
  value['aggregate_headroom_min_bytes']=headroom if before is None else min(before,headroom)
def quantiles(values):
 v=sorted(values)
 return {'count':len(v),'min':v[0],'p10':v[(len(v)-1)//10],'median':statistics.median(v),
         'p90':v[(len(v)-1)*9//10],'max':v[-1]}if v else{}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capture':str(a.relative_to(r)),
 'budget_bytes':budget,'exclusive_attempts':len(rows),'outcomes':dict(collections.Counter(x['status']for x in rows)),
 'native_peak_lower_bounds_bytes':quantiles([x['peak_lower_bound_bytes']for x in rows]),
 'exclusive_resource_peak_lower_bounds_bytes':quantiles([x['peak_lower_bound_bytes']for x in rows if x['status']=='resource_exhausted']),
 'exclusive_attempt_seconds':quantiles([x['seconds']for x in rows]),
 'ordinary_accepted_rejected_peak_lower_bounds_bytes':quantiles(ordinary),
 'exclusive_peak_above_47GiB':sum(x['peak_lower_bound_bytes']>47*1024**3 for x in rows),
 'exclusive_peak_above_47_5GiB':sum(x['peak_lower_bound_bytes']>47.5*1024**3 for x in rows),
 'resource_samples_total':sample_count,'exclusive_alone_samples':sum(x['alone_samples']for x in rows),
 'headroom_sample_counts':{str(n):sum(x['headroom_counts'][str(n)]for x in rows)for n in thresholds},
 'exclusive_attempts_without_sampled_leader':sum(not x['samples']for x in rows),
 'per_attempt':rows,
 'limits':['Peak memory observations are lower bounds;headroom samples do not bound next-second growth.',
 'Samples are counts,not uniform time intervals or promised spareCPU/RSS capacity.',
 'Aggregate snapshots include other own engine/backend state,not just candidateleader.',
 'This historicalpoint omitted the native Mathlib library;do not transfer its costs to the running repairedpoint.',
 'Do not infer rejection or success from memory measurements,or add overlapping retries without native pairedvalidation.']}
(s/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='per_attempt'},indent=2))
