"""Interpret real timeout goals, without changing the running screener."""
from pathlib import Path
from fractions import Fraction as Q
import gzip,json,sys,runpy
R=Path('/workspaces/repository');D=Path(__file__).parent
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path[:0]=[str(K),str(K/'client')]
from kimina_client.models import ReplResponse
worker=runpy.run_path(str(R/'bench/lean-counterexample/worker.py'))
def rows(name):
 with gzip.open(D/name,'rt')as f:return [json.loads(line)for line in f]
entries=rows('goals.jsonl.gz');events=rows('http.jsonl.gz');originals=rows('originals.jsonl.gz')
# m,n>1 and m*n=2005 imply 2<=m<=2005. Thus this divisor enumeration
# covers every assignment of the original natural-number assumptions.
feasible=[dict(m=m,n=2005//m)for m in range(2,2006)if 2005%m==0 and 2005//m>1]
assert feasible==[dict(m=5,n=401),dict(m=401,n=5)]
assert all(x['m']+x['n']==406 for x in feasible)
checks=[]
for e in entries:
 assert e['payload']['supported'];ast=e['payload']['ast']
 names=[x['name']for x in ast['variables']]
 assert set(names)=={'m','n'}and len(names)==2 and all(x['domain']=='nat'for x in ast['variables'])
 vm=['v',names.index('m')];vn=['v',names.index('n')];one=['q','1','1'];product=['q','2005','1']
 flattened=sum((worker['flatten'](h)for h in ast['hypotheses']),[])
 assert ['lt',one,vm]in flattened and ['lt',one,vn]in flattened
 assert ['eq',['*',vm,vn],product]in flattened or ['eq',['*',vn,vm],product]in flattened
 # The exported context explicitly retains all three original assumptions.
 # Therefore every model of this context is among the two enumerated models.
 models=[]
 for assignment in feasible:
  point=[Q(assignment[name])for name in names]
  holds=all(worker['proposition'](h,point)for h in ast['hypotheses'])
  conclusion=worker['proposition'](ast['goal'],point)
  refuted=worker['verify'](ast,point)
  assert not refuted
  models.append(dict(assignment=assignment,context_holds=holds,goal_holds=conclusion,exact_counterexample=refuted))
 assert all(x['goal_holds']for x in models if x['context_holds'])
 checks.append(dict(source_id=e['source_id'],entry_ns=e['entry_ns'],goal=ast['goal'],
  complete_original_premises_present=True,feasible_context_models=sum(x['context_holds']for x in models),
  models=models,no_counterexample_in_complete_context_domain=True))
requests=[]
for event in events:
 sid=json.loads(event['request'])['snippets'][0]['id']
 result=next(x for x in json.loads(event['body'])['results']if x['id']==sid)
 typed=ReplResponse.model_validate(result)
 status='resource_failure'if(typed.error or'').startswith('resource_failure:')else typed.analyze().status.value
 local=[x for x in entries if x['source_id']==sid]
 assert all(event['start_ns']<=x['entry_ns']<=event['end_ns']for x in local)
 assert status=='timeout_error'and result['time']==300.0
 last=max(x['worker_end_ns']for x in local)
 requests.append(dict(source_id=sid,status=status,reported_request_seconds=result['time'],
  HTTP_seconds=(event['end_ns']-event['start_ns'])/1e9,captured_goal_entries=len(local),
  HTTP_after_last_observer_worker_reply_seconds=(event['end_ns']-last)/1e9,
  original_contains_nested_interval_cases=next(x['code']for x in originals if 'minif2f-'+str(x['index'])==sid).count('interval_cases')>=2))
summary=dict(scope='Three returned timeout requests from a fixed subset of the ongoing observation; source/AST analysis only.',
 requests=requests,captured_goal_entries=len(checks),all9captured_goals_have_no_counterexample_in_complete_context_domain=all(x['no_counterexample_in_complete_context_domain']for x in checks),
 complete_original_feasible_assignments=feasible,
 original_conclusion_holds_on_all_original_models=True,
 total_HTTP_sum_seconds=sum(x['HTTP_seconds']for x in requests),
 boundaries=['The finite-domain argument is specific to the observed Nat factorization assumptions, not a generic Lean validity checker or formal Lean proof certificate.',
 'True observed arithmetic obligations cannot be rejected by a sound counterexample proposal/recheck at those hook points, irrespective of GPU point throughput.',
 'This does not certify every later unobserved proof obligation or prove every timeout in the population has a true target.',
 'Nested interval_cases is visible in source, but no dynamic exit/phase timing is collected here: the last-hook-to-response interval can include that last arithmetic search and later work.',
 'HTTP request intervals overlap and include waiting/transport; their sum is not whole elapsed, CPU work or a global GPU Amdahl bound.',
 'No new solver, native proof run, device run, runtime optimization or externally reproduced method is introduced. The live observer is unchanged.'])
(D/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
(D/'goal-checks.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(x,separators=(',',':'))+'\n'for x in checks)).encode(),mtime=0))
print(json.dumps(summary,indent=2))
