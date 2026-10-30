"""Complete existing-data exact-first-success comparison; never invokes Lean."""
import argparse, collections, gzip, heapq, json, math, pathlib, re, runpy, time
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
HERE=pathlib.Path(__file__).parent
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
OLD=ROOT/'artifacts/candidate-scheduling-2026-10-25/native-full7808-20261025T0730'
F=runpy.run_path(str(HERE/'features.py'))
STRIP=F['STRIP']
FAMILIES=['rfl','decide','simp_all','norm_num','nlinarith','linarith','omega','interval_cases','simp','rw','other']
def load(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def family(code):
 t=STRIP(code);m=re.search(r':=\s*by\b',t)
 if m:t=t[m.end():]
 m=re.search(r'\b(rfl|decide|simp_all|norm_num|nlinarith|linarith|omega|interval_cases|simp|rw)\b',t)
 return m.group(1) if m else 'other'
def datasets(inputs):
 run=load(PAIR/'engine.stdout.gz')
 current={}
 for row in run['results']:
  current[row['id']]={'valid':row['outcome']['status']=='accepted','status':row['outcome']['status'],
    'cost':sum(a['elapsed_seconds'] for a in row['attempts']),
    'ordinary_cost':sum(a['elapsed_seconds'] for a in row['attempts'] if not a['exclusive']),
    'exclusive_cost':sum(a['elapsed_seconds'] for a in row['attempts'] if a['exclusive'])}
 native={}
 with gzip.open(OLD/'all/results.jsonl.gz','rt') as f:
  for l in f:
   row=json.loads(l);native[row['proof_id']]={'valid':row['status']=='valid','status':row['status']}
 with gzip.open(OLD/'all/http.jsonl.gz','rt') as f:
  for l in f:
   row=json.loads(l)
   if row.get('event')!='response':continue
   req=json.loads(row['request'])
   snips=req.get('snippets',[])
   if len(snips)!=1 or snips[0]['id'] not in native:continue
   sid=snips[0]['id'];assert 'cost' not in native[sid]
   native[sid]['cost']=(row['end_ns']-row['start_ns'])/1e9
 assert set(current)==set(native)=={c['id'] for c in inputs}
 assert all(r['cost']>0 for r in native.values())
 return [('current_four_worker_attempt_cost',4,current),('historical_two_worker_HTTP_span_proxy',2,native)]
def fit(a,y,kind):
 penalty=np.eye(a.shape[1]);penalty[0,0]=0
 b=np.zeros(a.shape[1])
 if kind=='cost':b[0]=math.log(y.mean())
 def objective(v):
  z=np.clip(a@v,-30,30)
  return float((np.logaddexp(0,z)-y*z).sum() if kind=='probability' else (np.exp(z)-y*z).sum())+float(v@penalty@v/2)
 converged=False
 for iteration in range(100):
  z=np.clip(a@b,-30,30)
  mu=1/(1+np.exp(-z)) if kind=='probability' else np.exp(z)
  w=mu*(1-mu) if kind=='probability' else mu
  gradient=a.T@(mu-y)+penalty@b
  hessian=a.T@(w[:,None]*a)+penalty
  step=np.linalg.solve(hessian,gradient)
  scale=1.;old=objective(b)
  while scale>2**-24 and objective(b-scale*step)>old:scale/=2
  b-=scale*step
  if np.max(np.abs(scale*step))<1e-7:converged=True;break
 return b,{'kind':kind,'iterations':iteration+1,'converged':converged,'objective':objective(b)}
def train(inputs,records):
 texts=[STRIP(c['code']) for c in inputs]
 families=[family(c['code']) for c in inputs]
 x=np.array([F['vector'](c['code'])+[math.log1p(len(re.findall(r'\brfl\b',t)))]+[float(f==k) for k in FAMILIES] for c,t,f in zip(inputs,texts,families)])
 tasks=list(dict.fromkeys(c['task_id'] for c in inputs));task_index={t:i for i,t in enumerate(tasks)}
 fold=np.array([task_index[c['task_id']]%5 for c in inputs])
 y=np.array([records[c['id']]['valid'] for c in inputs],dtype=float)
 cost=np.array([records[c['id']]['cost'] for c in inputs])
 p=np.zeros(len(inputs));c=np.zeros(len(inputs));models=[];history={}
 for k in range(5):
  tr=fold!=k;te=~tr;mean=x[tr].mean(axis=0);scale=x[tr].std(axis=0);scale[scale==0]=1.
  a=np.column_stack([np.ones(tr.sum()),(x[tr]-mean)/scale])
  b=np.column_stack([np.ones(te.sum()),(x[te]-mean)/scale])
  beta,bstat=fit(a,y[tr],'probability');gamma,cstat=fit(a,cost[tr],'cost')
  p[te]=1/(1+np.exp(-np.clip(b@beta,-30,30)));c[te]=np.exp(np.clip(b@gamma,-30,30))
  # Beta-binomial intraclass correlation is fitted only on training tasks.
  for fam in FAMILIES:
   ids=[i for i in np.flatnonzero(tr) if families[i]==fam]
   groups=collections.defaultdict(list)
   for i in ids:groups[inputs[i]['task_id']].append(i)
   n=len(ids);success=sum(y[i] for i in ids);base=(success+1)/(n+2)
   pairs=sum(len(g)*(len(g)-1) for g in groups.values())
   both=sum(sum(y[i] for i in g)*(sum(y[i] for i in g)-1) for g in groups.values())
   cov=both/pairs-base*base if pairs else 0.
   rho=max(0.,min(.99,cov/(base*(1-base))))
   precision=(1-rho)/rho if rho>0 else None
   # Empirical distribution for a one-prefix probe index; outcomes are not test labels.
   dist=sorted((float(cost[i]),bool(y[i])) for i in ids)
   best=(0.,0.);prefix_cost=0.;prefix_success=0;j=0
   while j<len(dist):
    threshold=dist[j][0]
    while j<len(dist) and dist[j][0]==threshold:
     prefix_cost+=dist[j][0];prefix_success+=dist[j][1];j+=1
    denominator=prefix_cost+(len(dist)-j)*threshold
    if prefix_success and denominator>0:best=max(best,(prefix_success/denominator,threshold))
   history[(k,fam)]={'precision':precision,'probe_seconds':best[1],'probe_index':best[0],'train_sources':n}
  models.append({'fold':k,'mean':mean.tolist(),'scale':scale.tolist(),'logistic':beta.tolist(),'expected_cost_log_link':gamma.tolist(),'fit':[bstat,cstat],
   'train_tasks':sorted({inputs[i]['task_id'] for i in np.flatnonzero(tr)}),
   'test_tasks':sorted({inputs[i]['task_id'] for i in np.flatnonzero(te)})})
 assert np.all(np.isfinite(p)) and np.all(np.isfinite(c)) and np.all(c>0)
 return p,c,families,fold,models,history
def orders(inputs,records,p,c,families,fold,history,policy):
 groups=collections.defaultdict(list)
 for i,row in enumerate(inputs):groups[row['task_id']].append(i)
 out={};waste=0.;restarts=0;preemptions=0;budget_unknown=[];individual=[]
 for task,ids in groups.items():
  pending=ids.copy();done=[];observed=collections.defaultdict(list);probed=[]
  if policy=='oracle':
   valid=[i for i in ids if records[inputs[i]['id']]['valid']]
   pending=sorted(valid,key=lambda i:records[inputs[i]['id']]['cost'])+([i for i in ids if i not in valid] if valid else ids)
  elif policy=='size':pending.sort(key=lambda i:(len(STRIP(inputs[i]['code'])),i))
  elif policy in ('probability_cost','history','probe_restart'):
   pending.sort(key=lambda i:(-p[i]/c[i],i))
  while pending:
   if policy=='history':
    def score(i):
     prior=history[(int(fold[i]),families[i])]['precision'];seen=observed[families[i]]
     if prior is None or not seen:return p[i]/c[i]
     probability=p[i]*prior/(prior+len(seen))
     expected=(prior*c[i]+sum(seen))/(prior+len(seen))
     return probability/expected
    pending.sort(key=lambda i:(-score(i),i))
   if policy=='probe_restart':
    pending.sort(key=lambda i:(-history[(int(fold[i]),families[i])]['probe_index'],i))
   i=pending.pop(0);rec=records[inputs[i]['id']]
   if policy=='probe_restart':
    q=history[(int(fold[i]),families[i])]['probe_seconds']
    if q>0 and rec['cost']>q:
     probed.append((i,q));done.append((i,q,False,'discarded_probe'));waste+=q;preemptions+=1
     continue
   done.append((i,rec['cost'],rec['valid'],'complete'));observed[families[i]].append(rec['cost'])
   if rec['valid']:break
  if not any(z[2] for z in done) and policy=='probe_restart':
   for i,q in sorted(probed,key=lambda x:(-p[x[0]]/c[x[0]],x[0])):
    restarts+=1;budget_unknown.append(inputs[i]['id'])
    rec=records[inputs[i]['id']]
    done.append((i,rec['cost'],rec['valid'],'complete'))
    if rec['valid']:break
  complete=[i for i,cost,valid,kind in done if kind=='complete']
  solved=any(z[2] for z in done)
  if not solved:assert set(complete)==set(ids),'An unsolved task must complete all32'
  individual.append({'task':task,'work_seconds':sum(z[1] for z in done),'observed_solved':solved,'completed':len(complete),
   'attempt_ids':[inputs[i]['id'] for i,_,_,kind in done],'discarded_probe_seconds':sum(cost for i,cost,valid,kind in done if kind=='discarded_probe')})
  out[task]=done
 return out,individual,{'discarded_prefix_seconds':waste,'preemptions':preemptions,'restarts':restarts,'native_cumulative_budget_eligibility_unknown_ids':sorted(set(budget_unknown))}
def rr_simulate(groups,workers):
 # Lossless task handoff between whole modeled actions;one active candidate/task.
 queue=collections.deque((t,collections.deque(g)) for t,g in groups.items())
 events=[];now=0.;seq=0;finished={}
 def fill():
  nonlocal seq
  while len(events)<workers and queue:
   t,g=queue.popleft()
   i,c,v,k=g.popleft();seq+=1;heapq.heappush(events,(now+c,seq,t,g,v))
 fill()
 while events:
  now,_,t,g,valid=heapq.heappop(events)
  if valid or not g:finished[t]=now
  else:queue.append((t,g))
  fill()
 return {'cpu_slot_proxy_makespan_seconds':now,'mean_task_finish_seconds':sum(finished.values())/len(finished),'task_finish_seconds':finished}
def evaluate(inputs,records,p,c,families,fold,models,history,workers):
 groups=collections.defaultdict(list)
 for x in inputs:groups[x['task_id']].append(x['id'])
 unsolved={t for t,ids in groups.items() if not any(records[i]['valid'] for i in ids)}
 total=sum(z['cost'] for z in records.values());un=sum(records[i]['cost'] for t in unsolved for i in groups[t])
 ideal=un+sum(min(records[i]['cost'] for i in ids if records[i]['valid']) for t,ids in groups.items() if t not in unsolved)
 results={};per_task={}
 for policy in ['fifo','size','probability_cost','history','probe_restart','oracle']:
  scheduled,ind,extra=orders(inputs,records,p,c,families,fold,history,policy)
  model=rr_simulate(scheduled,workers)
  work=sum(x['work_seconds'] for x in ind)
  results[policy]={'frozen_work_seconds':work,'solved_tasks':sum(x['observed_solved'] for x in ind),'completed_sources':sum(x['completed'] for x in ind),
   'all_work_over_policy_ratio':total/work,'fifo_first_over_policy_ratio':None,**{k:v for k,v in model.items() if k!='task_finish_seconds'},**extra,
   'cpu_slot_proxy_ignores_RSS':True,'probe_index_scope':'One age-zero training-distribution prefix ratio;not a full Gittins policy or lossless native resume.','policy_scope':'Probe/restart verdicts optimistically retained despite unknown original cumulative-budget eligibility;not an exact-semantic qualified policy.' if policy=='probe_restart' else 'Frozen-cost ordering;CPU-slot timing ignores RSS admission,causal timing changes and overhead,not actual service performance.'}
  per_task[policy]=ind
 base=results['fifo']['frozen_work_seconds']
 for x in results.values():x['fifo_first_over_policy_ratio']=base/x['frozen_work_seconds']
 assert abs(results['oracle']['frozen_work_seconds']-ideal)<1e-6
 assert all(x['solved_tasks']==len(groups)-len(unsolved) for x in results.values())
 if 'exclusive_cost' in next(iter(records.values())):
  solo=sum(records[i]['exclusive_cost'] for t in unsolved for i in groups[t])
  ordinary_lower=un-solo+sum(min(records[i]['ordinary_cost'] for i in ids if records[i]['valid']) for t,ids in groups.items() if t not in unsolved)
 else:solo=ordinary_lower=None
 return {'sources':len(inputs),'tasks':len(groups),'solved_tasks':len(groups)-len(unsolved),'unsolved_tasks':len(unsolved),
  'all_frozen_work_seconds':total,'mandatory_unsolved_frozen_work_seconds':un,'minimum_first_success_frozen_work_seconds':ideal,
  'all_work_over_exact_first_success_oracle_ratio':total/ideal,
  'mandatory_unsolved_exclusive_cost_seconds':solo,
  'conditional_fixed_cost_ordinary_work_over_slots_plus_exclusive_lower_seconds':None if solo is None else solo+ordinary_lower/workers,
  'policies':results,'per_task':per_task,'models':models,'history_model':{str(k):v for k,v in history.items()},
  'interpretation':'The oracle must finish every observed-unsolved task and chooses the fastest accepted source on other tasks. Frozen operational labels/costs and zero scheduling overhead are conditional models,not global Amdahl bounds. One sequential observation per source cannot identify randomized restart distributions,resource curves,checkpoint cost or preserve exact timeout behavior.',
 }
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args()
 args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 inputs=load(PAIR/'input7808.json.gz')['candidates'];assert len(inputs)==7808
 reports={}
 for name,workers,records in datasets(inputs):
  p,c,families,fold,models,history=train(inputs,records)
  result=evaluate(inputs,records,p,c,families,fold,models,history,workers);reports[name]=result
  with gzip.open(args.out/(name+'-predictions.jsonl.gz'),'wt') as f:
   for i,x in enumerate(inputs):f.write(json.dumps({'id':x['id'],'task':x['task_id'],'fold':int(fold[i]),'probability':float(p[i]),'expected_observed_cost':float(c[i]),'family':families[i],'observed_status':records[x['id']]['status'],'observed_cost':records[x['id']]['cost']})+'\n')
  (args.out/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
  print(json.dumps({'point':name,**{k:v for k,v in result.items() if k not in ['per_task','models','history_model','interpretation']}},indent=2),flush=True)
 (args.out/'receipt.json').write_text(json.dumps({'analysis_seconds':time.monotonic()-start,'native_invocations':0,
  'features':F['NAMES']+['log_rfl']+['family_'+v for v in FAMILIES],
  'fitting':'Whole task modulo5heldout;ridge1logistic acceptance and Poisson quasi-likelihood log-link arithmetic expected observed complete cost. Same-task family failure/cost history only after modeled completion;empirical training-task correlation. No hyperparameter search;not fresh heldout benchmark validation.',
  'historical_measured_all_vs_short_ratio':1.439031292719,'historical_measured_source':'native-full7808-20261025T0730/full-result-review.md;not the simulation denominator'},indent=2)+'\n')
if __name__=='__main__':main()
