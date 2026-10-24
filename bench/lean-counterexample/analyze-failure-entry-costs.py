"""Locate failed-request costs relative to actual arithmetic entry coverage."""
from pathlib import Path
import argparse,collections,csv,gzip,json,os,sys,time
R=Path('/workspaces/repository')
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path[:0]=[str(K),str(K/'client')]
from kimina_client.models import ReplResponse
from worker import verify,proposition,answer
def rows(path):
 source=path if path.exists()else path.with_name(path.name+'.gz')
 with(gzip.open(source,'rt')if source.suffix=='.gz'else source.open())as stream:
  for line in stream:
   if not line.endswith('\n'):raise RuntimeError('Use closed newline-complete inputs')
   if line.strip():yield json.loads(line)
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 args=p.parse_args();args.out.mkdir(exist_ok=False)
 entries=list(rows(args.snapshot/'goals.jsonl'));by=collections.defaultdict(list)
 for e in entries:by[e['source_id']].append(e)
 attempts=[];reasons=collections.Counter();per_source=collections.Counter();unmatched=[]
 for event in rows(args.snapshot/'http.jsonl'):
  if event.get('event')!='response':continue
  request=json.loads(event['request']);snippets=request.get('snippets',[])
  if len(snippets)!=1 or not snippets[0]['id'].startswith('minif2f-'):continue
  sid=snippets[0]['id'];per_source[sid]+=1
  native=next((x for x in json.loads(event['body']).get('results',[])if x.get('id')==sid),None)
  if native is None:
   unmatched.append(dict(source_id=sid,reason='No matching native response result'));continue
  typed=ReplResponse.model_validate(native)
  status='resource_failure'if(typed.error or'').startswith('resource_failure:')else typed.analyze().status.value
  local=[x for x in by[sid]if event['start_ns']<=x['entry_ns']<=event['end_ns']]
  supported=[x for x in local if x['payload']['supported']]
  coverage='supported_entry'if supported else'unsupported_only'if local else'no_observed_entry'
  first=min((x['entry_ns']for x in local),default=None)
  first_supported=min((x['entry_ns']for x in supported),default=None)
  row=dict(source_id=sid,status=status,coverage=coverage,
   HTTP_seconds=(event['end_ns']-event['start_ns'])/1e9,entries=len(local),supported_entries=len(supported),
   first_entry_seconds=(first-event['start_ns'])/1e9 if first is not None else None,
   first_supported_entry_seconds=(first_supported-event['start_ns'])/1e9 if first_supported is not None else None,
   response_after_first_supported_seconds=(event['end_ns']-first_supported)/1e9 if first_supported is not None else None)
  attempts.append(row)
  if status!='valid':
   reasons.update(x['payload']['reason']for x in local if not x['payload']['supported'])
 groups=[]
 for status,coverage in sorted({(x['status'],x['coverage'])for x in attempts}):
  cohort=[x for x in attempts if x['status']==status and x['coverage']==coverage]
  groups.append(dict(status=status,coverage=coverage,response_attempts=len(cohort),
   HTTP_sum_seconds=sum(x['HTTP_seconds']for x in cohort),entries=sum(x['entries']for x in cohort),
   supported_entries=sum(x['supported_entries']for x in cohort)))
 ground=[];started=time.perf_counter_ns()
 for e in entries:
  if not e['payload']['supported']or e['payload']['ast']['variables']:continue
  ast=e['payload']['ast']
  expected=verify(ast,[]);q=dict(e,mode='gpu')
  reply=answer(q)
  if reply.get('evaluation_backend')!='cpu_closed' or reply['exact_counterexample']!=expected or reply.get('fallback_error'):
   raise RuntimeError('Closed real entry should not contact the point provider')
  ground.append(dict(source_id=e['source_id'],entry_ns=e['entry_ns'],exact_counterexample=expected,
   all_exact_hypotheses=all(proposition(h,[])for h in ast['hypotheses']),
   exact_goal=proposition(ast['goal'],[]),evaluation_backend=reply['evaluation_backend']))
 output=dict(scope='Partial immutable actual-goal/current-HTTP census, not complete7808coverage or performance.',
  source_snapshot=str(args.snapshot),response_attempts=len(attempts),unique_returned_sources=len({x['source_id']for x in attempts}),
  status_counts=dict(collections.Counter(x['status']for x in attempts)),partitions=groups,
  repeated_response_sources={k:v for k,v in per_source.items()if v>1},unmatched_response_results=unmatched,
  unsupported_failed_entry_reasons=dict(reasons),
  closed_exact_control=dict(entries=len(ground),source_count=len({x['source_id']for x in ground}),
   exact_counterexamples=sum(x['exact_counterexample']for x in ground),
   false_hypothesis_contexts=sum(not x['all_exact_hypotheses']for x in ground),
   true_hypothesis_and_true_goal=sum(x['all_exact_hypotheses']and x['exact_goal']for x in ground),
   no_provider_RPC=True,control_wall_seconds=(time.perf_counter_ns()-started)/1e9,
   note='One exact evaluation for a fully supported closed goal; no GPU or Lean execution in this replay.'),
  timeout_attempts=[x for x in attempts if x['status']=='timeout_error'],
  limitations=['A missing arithmetic entry does not locate the actual slow native component or prove a larger hook cannot help.',
   'Unsupported arithmetic remains unknown; the later alias build is not retroactively attributed to the frozen observer.',
   'HTTP intervals include waiting/import/transport and can overlap, so partition sums are not whole elapsed or an Amdahl bound.',
   'A timeout containing an exact supported goal is not necessarily a false goal; inconsistent branch assumptions admit no counterexample.',
   'Partial currently returned sources are not a random sample or fullfalsegoal fraction; in-flight sources are excluded.',
   'Closed worker controls establish exact/dispatch behavior on actual entries, not complete native outcome equivalence or an end-to-end saving.'])
 with(args.out/'response-entry-costs.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(attempts[0]),lineterminator='\n');w.writeheader();w.writerows(attempts)
 with(args.out/'closed-exact-controls.jsonl').open('w')as f:
  for x in ground:f.write(json.dumps(x,separators=(',',':'))+'\n')
 (args.out/'result.json').write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps({k:v for k,v in output.items()if k not in ['unsupported_failed_entry_reasons','timeout_attempts','limitations']},indent=2))
if __name__=='__main__':main()
