"""Offline native-process envelope decomposition; no native invocation."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import gzip,json,time,os
os.sched_setaffinity(0,{11})
t0=time.monotonic()
ROOT=Path(__file__).resolve().parents[3]
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
def read(name):
 with gzip.open(PAIR/name,'rt') as f:return json.load(f)
run=read('engine.stdout.gz')
reg={};rel={};parents=set();sample_times=[]
def when(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
with gzip.open(PAIR/'engine.stderr.gz','rt') as f:
 for line in f:
  event=json.loads(line);d=event['fields'];m=d['message'];stamp=when(event['timestamp'])
  if m in ('register active process','release active process ownership'):
   key=(d['pid'],d['start_ticks'])
   target=reg if m=='register active process' else rel
   assert key not in target,('duplicate identity',key)
   target[key]=(stamp,d['origin_id'],d['execution_id'])
  elif m=='backend lifecycle event' and d['stage']=='prepared_ready':
   parents.add(json.loads(d['detail'])['parent_pid'])
  elif m=='owned RSS sample':sample_times.append(stamp)
assert set(reg)==set(rel)
intervals=[];missing=[]
for row in run['results']:
 for index,attempt in enumerate(row['attempts']):
  identities=[(x['pid'],x['start_ticks']) for x in attempt['processes'] if x['pid'] not in parents]
  if not identities:
   missing.append([row['id'],index,attempt['status']]);continue
  assert all(x in reg and x in rel for x in identities)
  ids={(reg[x][1],reg[x][2]) for x in identities}
  assert len(ids)==1 and next(iter(ids))[0]==row['id']
  lo=min(reg[x][0] for x in identities);hi=max(rel[x][0] for x in identities)
  assert hi>=lo
  intervals.append(dict(id=row['id'],attempt=index,status=attempt['status'],exclusive=attempt['exclusive'],start=lo,end=hi,reported_attempt_seconds=attempt['elapsed_seconds']))
start=run['started_unix_ms']/1000;end=start+run['lifecycle_seconds']
# A normal serialized timestamp can differ by <1ms from the internal steady-clock
# boundary; report that discrepancy rather than moving the declared denominator.
assert min(x['start'] for x in intervals)>=start-0.01
assert max(x['end'] for x in intervals)<=end+0.01
events=defaultdict(lambda:[0,0])
for x in intervals:
 lo=max(start,x['start']);hi=min(end,x['end'])
 events[lo][0]+=1;events[hi][0]-=1
 if x['exclusive']:events[lo][1]+=1;events[hi][1]-=1
hist=defaultdict(float);active=exclusive=0;prev=start
for stamp,delta in sorted(events.items()):
 hist[(active,exclusive)]+=stamp-prev
 active+=delta[0];exclusive+=delta[1];prev=stamp
 assert active>=0 and 0<=exclusive<=active
hist[(active,exclusive)]+=end-prev
assert active==exclusive==0
assert abs(sum(hist.values())-run['lifecycle_seconds'])<1e-6
assert all(a<=4 for a,e in hist)
ordinary=[x for x in intervals if not x['exclusive']]
solo=[x for x in intervals if x['exclusive']]
frontier_end=max(x['end'] for x in ordinary)
solo_start=min(x['start'] for x in solo)
assert not missing,missing
assert len(intervals)==sum(len(r['attempts']) for r in run['results'])
assert all(a==1 for a,e in hist if e and hist[(a,e)]>0)
exclusive_time=sum(s for (a,e),s in hist.items() if e)
single=sum(s for (a,e),s in hist.items() if a==1)
aloneordinary=hist[(1,0)]
warm=read('warm/results.json.gz')
warmsolo=[a for rows in warm['attempts'].values() for a in rows if a['exclusive']]
result={
 'observed_utc':datetime.now(timezone.utc).isoformat(),
 'source':'complete frozen13d4606 full7808 actual native roots; prepared parents excluded',
 'denominator_internal_lifecycle_seconds':run['lifecycle_seconds'],
 'physical_attempts':len(intervals),'ordinary_attempts':len(ordinary),'exclusive_attempts':len(solo),
 'prepared_parent_pids_excluded':sorted(parents),'registered_retired_identities':len(reg),
 'intervals_without_native_roots':missing,
 'process_envelope_seconds_by_active_count':{str(n):sum(s for (a,e),s in hist.items() if a==n) for n in range(5)},
 'single_candidate_seconds':single,'single_candidate_exclusive_seconds':exclusive_time,
 'single_candidate_ordinary_seconds':aloneordinary,
 'exclusive_fraction_of_single_candidate_time':exclusive_time/single,
 'exclusive_fraction_of_whole_lifecycle':exclusive_time/run['lifecycle_seconds'],
 'last_ordinary_release_utc':datetime.fromtimestamp(frontier_end,timezone.utc).isoformat(),
 'first_exclusive_register_utc':datetime.fromtimestamp(solo_start,timezone.utc).isoformat(),
 'retry_tail_follows_all_ordinary_native_retirement':solo_start>=frontier_end,
 'gap_before_retry_tail_seconds':solo_start-frontier_end,
 'exclusive_status_counts':dict(Counter(x['status'] for x in solo)),
 'exclusive_reported_attempt_seconds_sum':sum(x['reported_attempt_seconds'] for x in solo),
 'three_unused_core_seconds_during_exclusive_process_envelopes':3*exclusive_time,
 'warm_immediate_exclusive_attempts':len(warmsolo),
 'warm_exclusive_wall_envelopes_sum':sum(x['wall_seconds'] for x in warmsolo),
 'clock_and_scope':'registration through ownership release, not candidate CPU use or whole lease; zero count includes queue/admission/setup/retirement gaps, not attributed overhead',
 'causal_limits':['No isolated old/new queue policy A/B','No safe memory ceiling inferred from censored peak','Warm and engine envelope bounds differ','Do not credit unused slots as safe overlap or free speedup','Shared-host support analysis on CPU11 is disclosed'],
 'analysis_elapsed_seconds':time.monotonic()-t0
}
out=Path(__file__).parent
(out/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
with gzip.open(out/'attempt-envelopes.jsonl.gz','wt') as f:
 for x in intervals:f.write(json.dumps(x)+'\n')
print(json.dumps(result,indent=2))
