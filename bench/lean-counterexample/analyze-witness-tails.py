"""Same-clock response tails of known exact witnesses; not saved whole time."""
from pathlib import Path
import collections,gzip,json,sys
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
K=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
sys.path[:0]=[str(K),str(K/'client')]
from kimina_client.models import ReplResponse
def rows(path):
 if path.exists():f=path.open()
 else:f=gzip.open(path.with_name(path.name+'.gz'),'rt')
 with f:
  for line in f:
   if not line.endswith('\n'):break
   if line.strip():yield json.loads(line)
def main():
 known=json.loads((A/'partial-coverage.json').read_text())['witnesses']
 witnesses=collections.defaultdict(list)
 for x in known:witnesses[x['source_id']].append(x['entry_ns'])
 attempts=collections.defaultdict(list)
 for event in rows(A/'full-observe/verification/http.jsonl'):
  if event.get('event')!='response':continue
  request=json.loads(event['request']);ids=[x['id']for x in request['snippets']]
  if len(ids)!=1 or ids[0]not in witnesses:continue
  sid=ids[0];response=json.loads(event['body'])
  for result in response.get('results',[]):
   if result.get('id')!=sid:continue
   typed=ReplResponse.model_validate(result)
   status='resource_failure'if(typed.error or'').startswith('resource_failure:')else typed.analyze().status.value
   entries=sorted(t for t in witnesses[sid]if event['start_ns']<=t<=event['end_ns'])
   attempts[sid].append(dict(source_id=sid,start_ns=event['start_ns'],end_ns=event['end_ns'],
    HTTP_seconds=(event['end_ns']-event['start_ns'])/1e9,reported_body_seconds=result.get('time'),
    status=status,observed_witness_entry_ns=entries,
    before_first_witness_seconds=(entries[0]-event['start_ns'])/1e9 if entries else None,
    response_tail_seconds=(event['end_ns']-entries[0])/1e9 if entries else None))
 output=dict(scope='Partial observed response intervals for the retained known witnesses; root self-review.',
  known_witness_sources=len(witnesses),sources_with_responses=len(attempts),attempts=dict(attempts),
  limitations=['Same host monotonic entry/HTTP clocks; no historical denominator is substituted.',
   'Response tail includes native tactic, subsequent commands, transport and possible waiting; it is not proven avoidable work.',
   'Returning a response does not prove native background threads or process cleanup are complete.',
   'Intervals can overlap; do not sum them into whole elapsed savings, CPU weights or an Amdahl bound.',
   'No response or no matched entry remains unobserved; a partial witness set is not full failure coverage.'])
 (A/'current-witness-response-tails.json').write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps(output,indent=2))
if __name__=='__main__':main()
