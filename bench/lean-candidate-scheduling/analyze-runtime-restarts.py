"""Runtime-only age/preemption analysis: no source features,success model or native calls."""
import argparse,bisect,collections,gzip,heapq,json,math,pathlib,time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
OLD=ROOT/'artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730'
def read(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def data():
 # Only routing/budget metadata are retained;the policy never receives source text.
 meta=[{k:c[k] for k in ['id','task_id','timeout_ms']} for c in read(PAIR/'input7808.json.gz')['candidates']]
 run=read(PAIR/'engine.stdout.gz')
 current={x['id']:{'cost':sum(a['elapsed_seconds'] for a in x['attempts']),
   'accepted':x['outcome']['status']=='accepted','status':x['outcome']['status'],
   'exclusive_cost':sum(a['elapsed_seconds'] for a in x['attempts'] if a['exclusive'])} for x in run['results']}
 old={}
 with gzip.open(OLD/'all/results.jsonl.gz','rt') as f:
  for l in f:
   x=json.loads(l);old[x['proof_id']]={'accepted':x['status']=='valid','status':x['status']}
 with gzip.open(OLD/'all/http.jsonl.gz','rt') as f:
  for l in f:
   x=json.loads(l)
   if x.get('event')!='response':continue
   req=json.loads(x['request']);snips=req.get('snippets',[])
   if len(snips)==1 and snips[0]['id'] in old:
    sid=snips[0]['id'];assert 'cost' not in old[sid];old[sid]['cost']=(x['end_ns']-x['start_ns'])/1e9
 assert len(meta)==len(current)==len(old)==7808
 assert all(x['cost']>0 and math.isfinite(x['cost']) for point in [current,old] for x in point.values())
 return meta,[('current_four_worker_composed_attempt_cost',4,current),('historical_two_worker_HTTP_cost_proxy',2,old)]
class RuntimePrior:
 """Empirical completion-time stopping index. No code,task success or final labels."""
 def __init__(self,costs):
  self.x=np.sort(np.array(costs,dtype=float));self.s=np.concatenate(([0.],np.cumsum(self.x)));self.cache={}
 def plan(self,observed_age,restart):
  key=(observed_age,restart)
  if key in self.cache:return self.cache[key]
  i=int(np.searchsorted(self.x,observed_age,side='right'));n=len(self.x)
  if i==n:
   answer=(math.inf,max(1.,2*observed_age));self.cache[key]=answer;return answer
  ends=self.x[i:];j=np.arange(i,n);count=j-i+1
  # Expected truncated work / probability of completion,conditioned on T>age.
  # Resume debits attained progress;restart pays the old prefix again.
  numerator=self.s[j+1]-self.s[i]+(n-j-1)*ends
  if not restart:numerator=numerator-(n-i)*observed_age
  rank=numerator/count
  k=int(np.argmin(rank));answer=(float(rank[k]),float(ends[k]))
  assert answer[0]>0 and answer[1]>observed_age
  self.cache[key]=answer;return answer
def simulate(meta,records,workers,priors,folds,policy):
 tasks=list(dict.fromkeys(x['task_id'] for x in meta));groups=collections.defaultdict(list)
 for i,x in enumerate(meta):groups[x['task_id']].append(i)
 assert len(tasks)==244 and all(len(g)==32 for g in groups.values())
 initial=[groups[t][k] for k in range(32) for t in tasks]
 positions={i:k for k,i in enumerate(initial)}
 jobs=[{'spent':0.,'progress':0.,'failed_prefix_bound':0.,'preemptions':0,'attempts':0,'discarded':0.,'terminal':None} for _ in meta]
 ready=[];events=[];active={};active_tasks=set();solved={};finished={};now=0.;seq=0
 def plan(i):
  j=jobs[i]
  if policy=='fifo':return (positions[i],math.inf)
  if policy.startswith('las'):
   chunk=1. if policy=='las_resume' else 2.**j['preemptions']
   return (j['spent'],j['progress']+chunk if policy=='las_resume' else chunk)
  restart=policy=='index_restart'
  age=j['failed_prefix_bound'] if restart else j['progress']
  return priors[folds[i]].plan(age,restart)
 def enqueue(i):
  nonlocal seq
  rank,cut=plan(i);seq+=1;heapq.heappush(ready,(rank,seq,i,cut))
 for i in initial:enqueue(i)
 def fill():
  nonlocal seq
  blocked=[]
  while len(active)<workers and ready:
   rank,order,i,cut=heapq.heappop(ready);job=jobs[i];task=meta[i]['task_id']
   if job['terminal'] is not None:continue
   if task in active_tasks:blocked.append((rank,order,i,cut));continue
   progress=job['progress'];remaining=records[meta[i]['id']]['cost']-progress
   # Actual completion cost is used only by this event generator,not by plan().
   duration=min(remaining,cut-progress)
   assert duration>0 and math.isfinite(duration),(policy,i,progress,cut,remaining)
   job['attempts']+=1;active[i]=(now,cut,progress);active_tasks.add(task);seq+=1
   heapq.heappush(events,(now+duration,seq,i))
  for item in blocked:heapq.heappush(ready,item)
 fill()
 while events:
  now,_,i=heapq.heappop(events);start,cut,progress=active.pop(i);job=jobs[i];task=meta[i]['task_id'];active_tasks.remove(task)
  served=now-start;job['spent']+=served;progress+=served
  actual=records[meta[i]['id']]
  if progress+1e-8>=actual['cost']:
   job['progress']=actual['cost'];job['terminal']=actual['status']
   if actual['accepted']:
    solved[task]=meta[i]['id'];finished[task]=now
    for other in groups[task]:
     if jobs[other]['terminal'] is None:jobs[other]['terminal']='cancelled_after_checked_success'
   elif all(jobs[k]['terminal'] is not None for k in groups[task]):finished[task]=now
  else:
   job['preemptions']+=1
   if policy.endswith('restart'):
    job['failed_prefix_bound']=max(job['failed_prefix_bound'],cut)
    job['discarded']+=progress;job['progress']=0.
   else:job['progress']=cut
   enqueue(i)
  fill()
 assert not active and not active_tasks and len(finished)==244
 target={t for t,ids in groups.items() if any(records[meta[i]['id']]['accepted'] for i in ids)}
 assert set(solved)==target
 for task,ids in groups.items():
  if task not in target:
   assert all(jobs[i]['terminal']==records[meta[i]['id']]['status'] for i in ids),'All unsolved candidates must finish.'
 spent=sum(x['spent'] for x in jobs)
 minimum=sum(min(records[meta[i]['id']]['cost'] for i in ids if records[meta[i]['id']]['accepted']) if task in target else sum(records[meta[i]['id']]['cost'] for i in ids) for task,ids in groups.items())
 assert spent+1e-6>=minimum
 restarts=sum(max(0,j['attempts']-1) for j in jobs) if policy.endswith('restart') else 0
 newly_over=[meta[i]['id'] for i,j in enumerate(jobs) if j['terminal']!='cancelled_after_checked_success'
   and j['spent']>meta[i]['timeout_ms']/1000 and records[meta[i]['id']]['cost']<=meta[i]['timeout_ms']/1000]
 native_restarts=[meta[i]['id'] for i,j in enumerate(jobs) if policy.endswith('restart') and j['attempts']>1]
 return {'policy':policy,'sources':7808,'tasks':244,'observed_solved_tasks':len(solved),'solved_task_ids':sorted(solved),
   'cpu_slot_proxy_makespan_seconds':now,'frozen_consumed_work_seconds':spent,'hindsight_minimum_work_seconds':minimum,
   'mean_task_completion_seconds':sum(finished.values())/244,'completed_native_sources':sum(j['terminal']!='cancelled_after_checked_success' for j in jobs),
   'preemptions':sum(j['preemptions'] for j in jobs),'restarts':restarts,
   'discarded_prefix_seconds':sum(j['discarded'] for j in jobs),
   'new_elapsed_budget_proxy_exceedances':newly_over,
   'restart_original_native_budget_eligibility_unknown_count':len(native_restarts),
   'prior_unsupported_tail_states':sum(1 for prior in priors for (rank,cut) in prior.cache.values() if math.isinf(rank)),
   'per_source':[{'id':meta[i]['id'],**j} for i,j in enumerate(jobs)],
   'scope':'One active process per task;runtime-only rank with FIFO ready ties. CPU-slot proxy ignores RSS,checkpoint/setup/signal/retirement overhead and causal timing changes. Resume retains progress without cost;restart discards/reexecutes prefixes with no new original-budget guarantee. Observed labels retained conditionally,not native parity.'}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();meta,points=data();tasks=list(dict.fromkeys(x['task_id'] for x in meta));taskfold={t:k%5 for k,t in enumerate(tasks)};folds=[taskfold[x['task_id']] for x in meta]
 for point,workers,records in points:
  priors=[RuntimePrior([records[x['id']]['cost'] for x in meta if taskfold[x['task_id']]!=k]) for k in range(5)]
  target={t for t in tasks if any(records[x['id']]['accepted'] for x in meta if x['task_id']==t)}
  groups=collections.defaultdict(list)
  for x in meta:groups[x['task_id']].append(x['id'])
  mandatory=sum(records[i]['cost'] for t,g in groups.items() if t not in target for i in g)
  minimum=mandatory+sum(min(records[i]['cost'] for i in g if records[i]['accepted']) for t,g in groups.items() if t in target)
  summary={'point':point,'sources':7808,'tasks':244,'observed_solved_tasks':142,'unsolved_tasks':102,
    'all_frozen_work_seconds':sum(x['cost'] for x in records.values()),'mandatory_unsolved_work_seconds':mandatory,'ideal_exact_first_success_work_seconds':minimum,
    'policy_information':'Only runtime age/elapsed prefix observation and prior runtimes of other heldout tasks. No code,tactic type,length,success probability model or outcome labels in planner.',
    'priors':[{'fold':k,'training_tasks':sum(v!=k for v in taskfold.values()),'heldout_tasks':sorted(t for t,v in taskfold.items() if v==k),'runtime_observations':len(p.x)} for k,p in enumerate(priors)],'policies':{}}
  for policy in ['fifo','las_resume','index_resume','las_restart','index_restart']:
   d=simulate(meta,records,workers,priors,folds,policy)
   with gzip.open(a.out/(point+'-'+policy+'.json.gz'),'wt') as f:json.dump(d,f)
   summary['policies'][policy]={k:v for k,v in d.items() if k not in ['per_source','solved_task_ids','new_elapsed_budget_proxy_exceedances','scope']}
   summary['policies'][policy]['new_elapsed_budget_proxy_exceedance_count']=len(d['new_elapsed_budget_proxy_exceedances'])
   print(json.dumps({'point':point,'policy':policy,'work':d['frozen_consumed_work_seconds'],'cpu_slot_proxy':d['cpu_slot_proxy_makespan_seconds'],'solved':d['observed_solved_tasks'],'preemptions':d['preemptions'],'restarts':d['restarts'],'discarded':d['discarded_prefix_seconds']}),flush=True)
  (a.out/(point+'.json')).write_text(json.dumps(summary,indent=2)+'\n')
 (a.out/'receipt.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'native_invocations':0,'source_predictor_training':False,'counterfactual_original_limits_and_RSS_parity':'unknown;do not enable from this proxy'},indent=2)+'\n')
if __name__=='__main__':main()
