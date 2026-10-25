"""Retrospective task-availability model; never executes a verifier."""
import pathlib,json,collections,heapq,time,datetime,os,psutil
r=pathlib.Path('/workspaces/repository');a=pathlib.Path(__file__).resolve().parent
os.sched_setaffinity(0,{8,9,10,11})
start=time.monotonic()
rows=json.loads((r/'artifacts/candidate-scheduling-2026-10-25/offline-v2/source-features.json').read_text())
records={v['source_id']:v for v in rows}
assert len(records)==7808
tasks=collections.OrderedDict()
for row in sorted(rows,key=lambda v:v['index']):tasks.setdefault(row['task'],[]).append(row['source_id'])
assert len(tasks)==244 and all(len(v)==32 for v in tasks.values())
expected={k for k,v in tasks.items()if any(records[i]['valid']for i in v)}
assert len(expected)==142
def stats(values):
 values=sorted(values)
 if not values:return None
 import math
 return dict(count=len(values),p50=values[math.ceil(len(values)*.5)-1],p90=values[math.ceil(len(values)*.9)-1],p99=values[math.ceil(len(values)*.99)-1],max=values[-1])
def model(order,workers):
 pending=collections.deque(order);active={};events=[];now=0.;solved={};calls=0;completed=0;waste=0.;consumed=0.;queued_cancel=0;active_cancel=0;sibling_starts=0;max_same=0
 def fill():
  nonlocal calls,queued_cancel,sibling_starts,max_same
  while pending and len(active)<workers:
   sid=pending.popleft();task=records[sid]['task']
   if task in solved:queued_cancel+=1;continue
   same=sum(records[i]['task']==task for i in active)
   sibling_starts+=int(same>0);max_same=max(max_same,same+1)
   finish=now+records[sid]['http_seconds']
   active[sid]=(now,finish);heapq.heappush(events,(finish,sid));calls+=1
 fill()
 while active:
  finish,sid=heapq.heappop(events)
  if sid not in active:continue
  now=finish;begin,_=active.pop(sid);completed+=1;consumed+=now-begin
  row=records[sid]
  if row['valid']:
   solved.setdefault(row['task'],now)
   for other,(begin,_)in list(active.items()):
    if records[other]['task']==row['task']:
     active_cancel+=1;waste+=now-begin;consumed+=now-begin;del active[other]
  fill()
 assert set(solved)==expected
 assert calls+queued_cancel==len(records) and completed+active_cancel==calls
 return dict(model_makespan_seconds=now,model_consumed_span_seconds=consumed,model_internal_task_first_success_seconds=solved,model_internal_solved_task_latency=stats(solved.values()),model_tasks_solved_by_seconds={str(t):sum(v<=t for v in solved.values())for t in [60,300,900,3600]},tasks_with_no_valid_observation=len(tasks)-len(solved),model_completed_candidates=completed,model_started_candidates=calls,model_cancelled_queued=queued_cancel,model_cancelled_active=active_cancel,model_cancelled_active_consumed_seconds=waste,model_starts_while_same_task_already_active=sibling_starts,model_max_same_task_inflight=max_same)
flat=[i for v in tasks.values()for i in v];interleaved=[v[k]for k in range(32)for v in tasks.values()]
reports={}
for workers in [2,4]:
 reports[str(workers)]={label:model(order,workers)for label,order in [('flat_first_success',flat),('task_interleaved_first_success',interleaved)]}
out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),population=7808,tasks=244,observed_solved_tasks=142,tasks_without_observed_success=102,models=reports,seconds=time.monotonic()-start,scope='Retrospective fixed observed HTTP intervals, not CPU/native service measurements. Lack of observed success is not theorem unsolvability; resource failures are operationally unresolved at the old point. Zero cancellation, packaging, prediction and cleanup overhead; costs/state unaffected by ordering/concurrency, no memory admission modeled. Four workers is a different hypothetical model, not a new measured resource point. Internal acceptance events are not client streaming: the existing batch adapter replies after all rows. Ordinary interleaving is prior technique; no new novelty or runtime speed result.')
(a/'model.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({w:{k:{x:v for x,v in val.items()if x!='model_internal_task_first_success_seconds'}for k,val in m.items()}for w,m in reports.items()},indent=2))
