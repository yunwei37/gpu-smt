# Exclusive retry headroom in the retained complete component pair

This is retrospective resource evidence from the already completed7808-candidate
native/prepared pair,not a new acquisition or a matched warm-service result.
The old sources,failed attempts,actual resource point and compiled-library
confound remain as recorded in the parent result review. It does not validate
the current13d4606full pair or the later source repairs.

## Question and method

Can the86%exclusive share of single-candidate occupancy be read as48GiB
saturation,or as time removed by moving retries to the tail? Neither follows.
Use exact PID/birth registrations/releases plus the existing owned RSS samples.
Exclude prepared parents when identifying an active candidate,but keep their
memory in aggregate RSS. Retain consecutive samples only when both have the
same sole exclusive candidate and both fall within its owned lifetime.
Do not bridge a registration,retirement or different candidate. Exact lifecycle
intervals additionally prove that no second candidate appeared and retired
between the two endpoints,which endpoint sampling alone would miss.
All44native and42prepared exclusive attempts have retained interiors.

The reference size is each historical cell's observed upper median of nonzero
first nonexclusive attempt peaks:3,763,990,528bytes(native) and488,558,592bytes
(prepared). These are retrospectively selected measured values,not new runtime
settings or safe future peaks. The prepared reference reflects COW child/
sampling behavior and cannot be substituted for a fresh-worker memory need.
Short unsampled peaks remain a limitation.

|Historical cell|Exclusive attempt seconds|Same-candidate sampled interiors|Headroom at both endpoints for one own-cell reference|Three references|
|---|---:|---:|---:|---:|
|native|9480.135|9435.004|8521.007s(90.313%)|7163.004s(75.919%)|
|prepared|8927.470|8882.005|8718.003s(98.154%)|8556.010s(96.330%)|

At least one ordinary first attempt was still unstarted throughout all retained
exclusive interiors in these old immediate-retry captures. This is identified
by future exact registrations in the complete trace,not inferred from a
persistent queue file. No child PID is attributed by PID without its birth.
Largest retained sample gaps are1.0071s(native) and1.0249s(prepared).

A resource-failed attempt still owns time while growing toward the budget.
Endpoint headroom does not bound between-sample memory,forecast a new source,
promise a CPU slot or prove a safe overlap. The41resource failures per cell and
3native/1prepared exclusive timeouts remain failures;none is promoted to a
rejection certificate or cacheable result.

## Consequence for the current repair

Source13d4606already moves retries behind a finite ordinary frontier. Source
6252a78makes the future warm adapter follow that order too. This avoids the
old ordinary-frontier drain barrier. It does not make the later exclusive
work parallel:once ordinary work is finished,there are no ordinary candidates
left to backfill those retries. It is therefore incorrect to count the86%
occupancy figure,or the headroom seconds above,as eliminated whole-batch time.

As a transparent planning calculation,freeze each recorded attempt duration,
allow perfect packing of all nonexclusive work into four slots,and retain
every exclusive attempt serially. The resulting optimistic fixed-duration
schedule is ordinary_attempt_seconds/4+exclusive_attempt_seconds:

|Cell|Ordinary attempt seconds|Exclusive seconds|Model seconds|Observed external seconds / model|
|---|---:|---:|---:|---:|
|native|68448.774|9480.135|26592.328|1.06768|
|prepared|49801.536|8927.470|21377.854|1.07080|

This is not an Amdahl bound or a bound on a real implementation. Attempt
durations change with contention and resource protocol;source/library versions
differ;the model omits preparation,queue,observation and cleanup constraints.
It supports a smaller claim:tail movement alone is not evidence of a dramatic
gain,even under an optimistic fixed-duration rearrangement.

## Root disposition and validation

Keep the existing finite full pair unchanged and review its complete outcomes.
Do not enable new overlapping retries merely because an old sampled median
fits. In particular,a preempted peak is a censored observation,not an upper
bound,and a retry preempted with peers cannot be labelled a solo resource
failure. An overlapping design would have to retain requeue/retirement and a
true solo final attempt,count all wasted attempts,and obey the existing
largest-owned-process watchdog. Its performance remains unmeasured and is not
silently enabled here.

This supports RQ3resource-protocol interpretation;it does not answer RQ3,
establish warm parity or add novelty. Raw [per-attempt accounting](retry-headroom-20261028.json)
retains all44+42attempts,coverage,statuses and reference definitions.
Partition checks require per-attempt interiors to equal their cell total,
all headroom sets to nest,and no endpoint to escape its birth-matched lifetime.
The maximum-gap/coverage limits are explicit. Root only,self-review.
No new native cohort,logger,watcher,parser utility or runtime setting is added.

## Exact offline reproduction

Run the following in the owning repository with its retained artifacts.
It uses one existing CPU for offline analysis and writes only an OS-temporary
result. The historical source files are read-only. The fixed-duration model
and headroom output reproduce the JSON above. The script is documentation for
this calculation,not an installed observer or new experiment runner.

```python
from pathlib import Path
import gzip,json,datetime,collections,bisect,statistics,os
os.sched_setaffinity(0,{11})
R=Path('/workspaces/repository')
B=R/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
captures={n:json.loads(gzip.decompress((B/n/'capture.json.gz').read_bytes()))for n in ['native','prepared']}
registrations={};releases={};samples=[]
with gzip.open(B/'driver.log.gz','rt')as f:
 for line in f:
  row=json.loads(line);a=row.get('fields',{});m=a.get('message')
  if m not in ['register active process','release active process ownership','owned RSS sample']:continue
  tm=datetime.datetime.fromisoformat(row['timestamp'].replace('Z','+00:00')).timestamp()
  if m=='owned RSS sample':
   samples.append((tm,a['rss_bytes'],[(p['identity']['pid'],p['identity']['start_ticks'])for p in json.loads(a['processes'])]))
  else:
   key=(a['pid'],a['start_ticks']);d=registrations if m=='register active process'else releases
   assert key not in d;d[key]=tm
report={'source':str(B.relative_to(R)),'scope':'retrospective sampled headroom, not safe admission bounds, removed wall time or measured backfill speedup','cells':{}}
for name,c in captures.items():
 budget=c['resources']['memory_bytes']
 parents={json.loads(e['detail'])['parent_pid']for row in c['results']for a in row['attempts']for e in a['backend_events']if e['stage']=='prepared_ready'}
 process={};ordinary_starts=[];ordinary_peaks=[];exclusive=[]
 for row in c['results']:
  first=row['attempts'][0]
  assert not first['exclusive'], 'historical first attempt was not ordinary'
  kids=[(p['pid'],p['start_ticks'])for p in first['processes']if p['pid']not in parents]
  ordinary_starts.append(min(registrations[k]for k in kids))
  if not first['exclusive'] and first['peak_rss_bytes']>0:ordinary_peaks.append(first['peak_rss_bytes'])
  for index,a in enumerate(row['attempts']):
   kids=[(p['pid'],p['start_ticks'])for p in a['processes']if p['pid']not in parents]
   for k in kids:
    assert k not in process;process[k]=(row['id'],index,a)
   if a['exclusive']:exclusive.append((row['id'],index,a,kids))
 ordinary_starts.sort()
 upper_median=sorted(ordinary_peaks)[len(ordinary_peaks)//2]
 thresholds={k:budget-k*upper_median for k in [1,2,3]}
 lo=min(registrations[k]for k in process);hi=max(releases[k]for k in process)
 cell_samples=[s for s in samples if lo<=s[0]<=hi]
 child_starts=sorted(registrations[k]for k in process)
 child_ends=sorted(releases[k]for k in process)
 spans=[];covered=0.;head={k:0. for k in thresholds};pending_head={k:0. for k in thresholds}
 statuses=collections.defaultdict(float);sampled_attempts=set();pending_seconds=0.;gapmax=0.
 for left,right in zip(cell_samples,cell_samples[1:]):
  lt,lr,lk=left;rt,rr,rk=right
  leftkids=[k for k in lk if k in process]
  rightkids=[k for k in rk if k in process]
  if len(leftkids)!=1 or leftkids!=rightkids:continue
  key=leftkids[0];id,index,a=process[key]
  if not a['exclusive']:continue
  assert registrations[key]<=lt<=rt<=releases[key]
  assert bisect.bisect_left(child_starts,rt)-bisect.bisect_right(child_ends,lt)==1, 'another child overlaps the sample interior'
  dt=rt-lt;assert dt>=0
  covered+=dt;statuses[a['status']]+=dt;gapmax=max(gapmax,dt);sampled_attempts.add((id,index))
  pending=len(ordinary_starts)-bisect.bisect_right(ordinary_starts,lt)
  if pending:pending_seconds+=dt
  for k,threshold in thresholds.items():
   if max(lr,rr)<=threshold:
    head[k]+=dt
    if pending:pending_head[k]+=dt
  spans.append({'id':id,'attempt_index':index,'from_unix':lt,'to_unix':rt,'rss_left':lr,'rss_right':rr,'pending_ordinary_first_starts':pending})
 sum_exclusive=sum(a['elapsed_seconds']for _,_,a,_ in exclusive)
 per_attempt=[]
 for id,index,a,kids in exclusive:
  selected=[s for s in spans if s['id']==id and s['attempt_index']==index]
  total=sum(s['to_unix']-s['from_unix']for s in selected)
  per_attempt.append({'id':id,'attempt_index':index,'status':a['status'],'attempt_seconds':a['elapsed_seconds'],'peak_rss_bytes':a['peak_rss_bytes'],'registered_children_seconds':sum(releases[k]-registrations[k]for k in kids),'covered_sample_interiors_seconds':total,'pending_ordinary_sample_interiors_seconds':sum(s['to_unix']-s['from_unix']for s in selected if s['pending_ordinary_first_starts']>0),'headroom_one_observed_median_seconds':sum(s['to_unix']-s['from_unix']for s in selected if max(s['rss_left'],s['rss_right'])<=thresholds[1])})
 assert abs(sum(v['covered_sample_interiors_seconds']for v in per_attempt)-covered)<1e-5
 assert all(0<=v<=covered+1e-6 for v in head.values())
 assert all(pending_head[k]<=head[k]+1e-6 for k in thresholds)
 assert head[3]<=head[2]<=head[1]<=covered+1e-6
 assert sum(statuses.values())<=covered+1e-6
 report['cells'][name]={'budget_bytes':budget,'exclusive_attempts':len(exclusive),'exclusive_status_counts':dict(collections.Counter(a['status']for _,_,a,_ in exclusive)),'exclusive_monotonic_attempt_sum_seconds':sum_exclusive,'exclusive_sample_interior_seconds':covered,'sampled_exclusive_attempts':len(sampled_attempts),'maximum_retained_sample_gap_seconds':gapmax,'sample_interior_seconds_by_attempt_status':dict(statuses),'sample_interior_seconds_with_unstarted_ordinary_requests':pending_seconds,'ordinary_first_attempt_nonzero_peak_observations':len(ordinary_peaks),'ordinary_observed_upper_median_peak_bytes':upper_median,'headroom_reference_counts':{str(k):{'endpoint_headroom_bytes':k*upper_median,'sample_interior_seconds':head[k],'sample_interior_fraction':head[k]/covered,'with_unstarted_ordinary_requests_seconds':pending_head[k]}for k in thresholds},'per_attempt':per_attempt}
out=Path('/tmp/gpu-smt-exclusive-headroom-analysis-20261028.json');out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**report,'cells':{n:{k:v for k,v in c.items()if k!='per_attempt'}for n,c in report['cells'].items()}},indent=2))

# The same retained attempts support this explicitly fixed-duration model.
v=json.loads(out.read_text())
for name,c in captures.items():
 a=[a for row in c['results']for a in row['attempts']]
 ordinary=sum(x['elapsed_seconds']for x in a if not x['exclusive'])
 serial=sum(x['elapsed_seconds']for x in a if x['exclusive'])
 whole=json.loads((B/name/'terminal.json').read_text())['external_cell_seconds']
 lower=ordinary/4+serial
 v['cells'][name]['fixed_duration_exclusive_model']={'ordinary_attempt_seconds_sum':ordinary,'exclusive_attempt_seconds_sum':serial,'external_cell_seconds':whole,'four_slot_perfect_ordinary_packing_plus_unchanged_serial_seconds':lower,'descriptive_ratio_to_model':whole/lower,'scope':'optimistic fixed-duration scheduling model only; measured contention-sensitive durations are not invariant across protocols, so this is not a real-system speedup ceiling or Amdahl bound'}
out.write_text(json.dumps(v,indent=2)+'\n')

```
