"""Complete closed-census timeout applicability; no new verification/device run."""
from pathlib import Path
from fractions import Fraction as Q
import collections,csv,gzip,json,re,runpy,time,datetime
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23';O=Path(__file__).parent
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def rows(p):
 with gzip.open(p,'rt')as f:return [json.loads(s)for s in f]
originals=rows(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz')
results={e['proof_id']:e for e in rows(A/'full-observe/verification/results.jsonl.gz')}
assert len(originals)==len(results)==7808
coverage=json.loads((A/'full-coverage-analysis-20261024T0907/full-coverage.json').read_text())
witnesses=set(coverage['witness_source_IDs'])
source={};unresolved=[]
for e in originals:
 sid='minif2f-'+str(e['index']);names=re.findall(r'^theorem\s+([^\s(:]+)',e['code'],re.M)
 if len(names)==1:name=names[0]
 else:name=None;unresolved.append(sid)
 source[sid]=dict(task_name=name,index=e['index'])
entries=rows(A/'full-observe/verification/goals.jsonl.gz')
by=collections.defaultdict(list)
for e in entries:by[e['source_id']].append(e)
timing={}
for e in rows(A/'full-observe/verification/http.jsonl.gz'):
 if e.get('event')!='response':continue
 sn=json.loads(e['request']).get('snippets',[])
 if len(sn)==1 and sn[0]['id']in results:
  sid=sn[0]['id'];assert sid not in timing;timing[sid]=(e['end_ns']-e['start_ns'])/1e9
assert len(timing)==7808
timeouts=sorted(sid for sid in results if results[sid]['status']=='timeout_error')
assert len(timeouts)==78 and not(set(timeouts)&set(unresolved))
worker=runpy.run_path(str(R/'bench/lean-counterexample/worker.py'))
closed=[];factor=[];classification=[]
feasible=[dict(m=m,n=2005//m)for m in range(2,2006)if 2005%m==0 and 2005//m>1]
assert feasible==[dict(m=5,n=401),dict(m=401,n=5)]
for sid in timeouts:
 supported=[e for e in by[sid]if e['payload']['supported']]
 local_closed=0;local_factor=0
 for e in supported:
  ast=e['payload']['ast']
  if not ast['variables']:
   hs=all(worker['proposition'](h,[])for h in ast['hypotheses'])
   goal=worker['proposition'](ast['goal'],[])
   refuted=worker['verify'](ast,[])
   closed.append(dict(source_id=sid,entry_ns=e['entry_ns'],all_exact_hypotheses=hs,exact_goal=goal,exact_counterexample=refuted))
   local_closed+=1
  if source[sid]['task_name']=='mathd_numbertheory_541':
   names=[v['name']for v in ast['variables']]
   if len(names)!=2 or set(names)!={'m','n'}or any(v['domain']!='nat'for v in ast['variables']):continue
   vm=['v',names.index('m')];vn=['v',names.index('n')];one=['q','1','1'];product=['q','2005','1']
   hs=sum((worker['flatten'](h)for h in ast['hypotheses']),[])
   if not(['lt',one,vm]in hs and ['lt',one,vn]in hs and(['eq',['*',vm,vn],product]in hs or ['eq',['*',vn,vm],product]in hs)):continue
   models=[]
   for assignment in feasible:
    point=[Q(assignment[name])for name in names]
    context=all(worker['proposition'](h,point)for h in ast['hypotheses'])
    goal=worker['proposition'](ast['goal'],point)
    refuted=worker['verify'](ast,point)
    models.append(dict(assignment=assignment,context_holds=context,goal_holds=goal,exact_counterexample=refuted))
   assert not any(z['exact_counterexample']for z in models)
   factor.append(dict(source_id=sid,entry_ns=e['entry_ns'],models=models,complete_original_premises_present=True,no_counterexample_in_complete_context_domain=True))
   local_factor+=1
 classification.append(dict(source_id=sid,task_name=source[sid]['task_name'],HTTP_seconds=timing[sid],
  entries=len(by[sid]),supported_entries=len(supported),closed_supported_entries=local_closed,
  finite_domain_excluded_entries=local_factor,
  coverage='no_entry'if not by[sid]else'unsupported_only'if not supported else'supported_no_witness'))
assert not any(z['exact_counterexample']for z in closed)
tasks=[]
for task in sorted({e['task_name']for e in classification}):
 items=[e for e in classification if e['task_name']==task]
 tasks.append(dict(task_name=task,timeout_candidates=len(items),
  no_entry_sources=sum(e['coverage']=='no_entry'for e in items),
  unsupported_only_sources=sum(e['coverage']=='unsupported_only'for e in items),
  supported_sources=sum(e['supported_entries']>0 for e in items),
  supported_entries=sum(e['supported_entries']for e in items),
  closed_entries=sum(e['closed_supported_entries']for e in items),
  finite_domain_excluded_entries=sum(e['finite_domain_excluded_entries']for e in items),
  HTTP_sum_seconds=sum(e['HTTP_seconds']for e in items)))
tasks.sort(key=lambda e:e['timeout_candidates'],reverse=True)
summary=dict(scope='Complete7808 observation, all78timeouts; existing raw analysis only, root self-review.',
 started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 all_source_task_names_resolved=7808-len(unresolved),unresolved_task_source_IDs=unresolved,
 distinct_resolved_task_names=len({x['task_name']for x in source.values()if x['task_name']}),
 timeout_sources=len(timeouts),timeout_task_names=len(tasks),timeout_tasks=tasks,
 closed_timeout_entries=dict(entries=len(closed),source_count=len({x['source_id']for x in closed}),
  exact_counterexamples=sum(x['exact_counterexample']for x in closed),
  false_hypothesis_contexts=sum(not x['all_exact_hypotheses']for x in closed),
  true_hypothesis_true_goal=sum(x['all_exact_hypotheses']and x['exact_goal']for x in closed)),
 factorization_timeout_complete_domain=dict(entries=len(factor),sources=len({x['source_id']for x in factor}),models=feasible,
  all_captured_supported_entries_of_task_checked=len(factor)==sum(x['supported_entries']for x in classification if x['task_name']=='mathd_numbertheory_541'),
  no_counterexample_at_checked_entries=True),
 witness_resolved_task_names=sorted({source[sid]['task_name']for sid in witnesses if source[sid]['task_name']}),
 witness_unresolved_source_IDs=sorted(witnesses&set(unresolved)),
 limits=['The statement-name scan is source metadata only;18malformed/no-theorem inputs remain unresolved instead of inferred from index groups.',
  'Same-task candidates and repeated entries are not independent benchmark problems; task-level coverage is reported separately.',
  'Closed exact evaluation reuses our existing checker, not an independent proof or new CPU/GPU execution.',
  'Finite Nat factorization argument is specific to explicitly retained m,n>1 and m*n=2005; no generic solver or theorem checker is introduced.',
  'Excluded captured entries do not establish validity of every later unseen goal or remove timeout candidates from timing denominators.',
  'No-entry/unsupported/no-witness do not prove absence of a future acceleration opportunity.',
  'HTTP sums overlap and include observation costs, never whole-wall savings or an Amdahl bound.',
  'This short analysis coexecuted with the nativeoff full pair on the shared host; that run is not claimed isolated.'])
with(O/'timeout-sources.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(classification[0]),lineterminator='\n');w.writeheader();w.writerows(classification)
for name,data in [('closed-timeout-entries.jsonl.gz',closed),('factorization-timeout-entries.jsonl.gz',factor)]:
 (O/name).write_bytes(gzip.compress(''.join(json.dumps(e,separators=(',',':'))+'\n'for e in data).encode(),mtime=0))
(O/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k not in ['limits','unresolved_task_source_IDs']},indent=2))
