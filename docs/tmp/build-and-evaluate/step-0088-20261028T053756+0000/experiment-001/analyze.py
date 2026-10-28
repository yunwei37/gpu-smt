"""Disjoint interpretation of existing prepared-cell singleton occupancy.
No new native collection and no invented admission-decision phase clock.
"""
from pathlib import Path
import collections,datetime,gzip,json,os
os.sched_setaffinity(0,{11})
R=Path('/workspaces/repository')
B=R/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
c=json.loads(gzip.decompress((B/'prepared/capture.json.gz').read_bytes()))
parent_ids={json.loads(e['detail'])['parent_pid']for v in c['results']for a in v['attempts']for e in a['backend_events']if e['stage']=='prepared_ready'}
needed={(p['pid'],p['start_ticks'])for v in c['results']for a in v['attempts']for p in a['processes']}
reg={};end={}
with gzip.open(B/'driver.log.gz','rt')as f:
 for line in f:
  row=json.loads(line);a=row.get('fields',{});msg=a.get('message')
  if msg not in ['register active process','release active process ownership']:continue
  key=(a['pid'],a['start_ticks'])
  if key not in needed:continue
  t=datetime.datetime.fromisoformat(row['timestamp'].replace('Z','+00:00')).timestamp()
  target=reg if msg=='register active process'else end
  assert key not in target;target[key]=t
events=collections.defaultdict(list);attempts={};first={};pending=[];empty=[]
for v in c['results']:
 grouped=[]
 for i,a in enumerate(v['attempts']):
  keys=[(p['pid'],p['start_ticks'])for p in a['processes']if p['pid']not in parent_ids]
  key=(v['id'],i);spans=[]
  for p in keys:
   assert p in reg and p in end
   if end[p]>reg[p]:
    events[reg[p]].append(('start',p,key));events[end[p]].append(('end',p,key));spans.append((reg[p],end[p]))
  attempts[key]={'source':v['id'],'attempt':i,'exclusive':a['exclusive'],
   'final_status':v['outcome']['status'],'attempt_status':a['status'],
   'preempted':a['preemption_rss_bytes']is not None,'spans':spans}
  grouped.append((a,spans))
 if grouped and grouped[0][1]:first[v['id']]=min(lo for lo,hi in grouped[0][1])
 else:empty.append(v['id'])
 for i,(a,spans)in enumerate(grouped[:-1]):
  following,after=grouped[i+1]
  if a['preemption_rss_bytes']is not None and not a['exclusive']and following['exclusive']and spans and after:
   lo=max(hi for lo,hi in spans);hi=min(lo for lo,hi in after)
   assert hi>=lo
   events[lo].append(('retry_pending_start',v['id'],None))
   events[hi].append(('retry_pending_end',v['id'],None))
   pending.append({'source':v['id'],'from_confirmed_native_retirement':lo,'to_retry_native_registration':hi,'seconds':hi-lo})
assert len(first)==7808 and not empty
last_first=max(first.values())
live={};waiting=set();previous=None
totals=collections.defaultdict(float);by_status=collections.defaultdict(lambda:collections.defaultdict(float))
by_source=collections.defaultdict(lambda:collections.defaultdict(float));unresolved=[]
for t,changes in sorted(events.items()):
 if previous is not None and t>previous and len(live)==1:
  p,key=next(iter(live.items()));a=attempts[key];duration=t-previous
  if a['exclusive']:kind='actual_exclusive_native_attempt'
  elif waiting:kind='other_native_while_resource_retry_pending_inferred'
  elif previous>=last_first:kind='end_of_batch_tail_no_first_attempt_unstarted'
  else:kind='remaining_with_unstarted_native_work_reason_unlogged'
  totals[kind]+=duration;by_status[kind][a['final_status']]+=duration;by_source[kind][a['source']]+=duration
  if kind.startswith('remaining'):unresolved.append({'source':a['source'],'start_utc':previous,'end_utc':t,'seconds':duration})
 for kind,p,key in changes:
  if kind=='start':assert p not in live;live[p]=key
  elif kind=='end':assert p in live;live.pop(p)
  elif kind=='retry_pending_start':waiting.add(p)
  else:waiting.remove(p)
 previous=t
assert not live and not waiting
singleton=sum(totals.values())
old=json.loads((R/'docs/tmp/build-and-evaluate/step-0086-20261028T041734+0000/experiment-001/analysis.json').read_text())['cells']['prepared']
expected=float(old['occupied_native_children_seconds_by_count']['1'])
assert abs(singleton-expected)<0.001,(singleton,expected)
summary={'source':str(B.relative_to(R)),'singleton_seconds':singleton,
'whole_seconds':old['external_cell_seconds'],'singleton_fraction_of_whole':singleton/old['external_cell_seconds'],
'disjoint_singleton_categories':[{'category':k,'seconds':v,'fraction_of_singleton':v/singleton,
 'fraction_of_whole':v/old['external_cell_seconds'],'final_status_seconds':dict(by_status[k]),
 'top_sources':sorted(by_source[k].items(),key=lambda x:-x[1])[:20]}for k,v in sorted(totals.items(),key=lambda x:-x[1])],
'pending_retry_windows':pending,'remaining_unlogged_intervals':unresolved,'all_first_attempts_registered':len(first),
'boundary':'Exact singleton/exclusive process spans from registered birth ownership. Retry-pending range uses backend retirement→next native registration,not a logged solo-waiter/lease transition;contains small backend/engine gaps. Tail means all first native starts observed,not exact queue-lease count.',
'causal_limits':'Occupied process time is not CPU use. Remaining nonexclusive intervals with unstarted work do not prove conservative forecasts: no actual reservation/admission reasons were logged. Do not change required exclusive retries or infer removable time/speedup.'}
Path(__file__).with_name('analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k not in ['pending_retry_windows','remaining_unlogged_intervals']},indent=2))
