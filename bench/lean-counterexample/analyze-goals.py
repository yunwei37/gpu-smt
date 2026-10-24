"""Typed actual-goal coverage. Partial mode is a labelled diagnostic only."""
from pathlib import Path
import argparse,collections,csv,gzip,json,time
from point_proposals import find
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def load_rows(p):
 if p.exists():
  f=p.open()
 else:f=gzip.open(p.with_name(p.name+'.gz'),'rt')
 with f:
  for line in f:
   if not line.endswith('\n'):break
   if line.strip():yield json.loads(line)
def main():
 p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');p.add_argument('--qualification',action='store_true');args=p.parse_args()
 directory=A/('qualification32v3-observe'if args.qualification else'full-observe/verification')
 terminal=directory/'terminal.json'
 if not args.partial:
  assert terminal.exists()and json.loads(terminal.read_text())['state']=='complete'
 results={x['proof_id']:x for x in load_rows(directory/'results.jsonl')}if (terminal.exists()or(directory/'results.jsonl').exists())else{}
 with(A/'failure-source-costs.csv').open()as f:costs={x['proof_id']:x for x in csv.DictReader(f)}
 rows=list(load_rows(directory/'goals.jsonl'));supported=[x for x in rows if x['payload']['supported']]
 witnesses=[];unknown=[];started=time.monotonic()
 for x in supported:
  try:w=find(x['payload']['ast'])
  except Exception as ex:unknown.append(dict(source_id=x['source_id'],entry_ns=x['entry_ns'],error=repr(ex)));continue
  if w:witnesses.append(dict(source_id=x['source_id'],entry_ns=x['entry_ns'],witness=w,ast=x['payload']['ast']))
 ids=sorted({x['source_id']for x in witnesses})
 by_status=collections.Counter(results[i]['status']if i in results else'no_final_current_response_yet'for i in ids)
 known_old_failure=[i for i in ids if costs[i]['failed']=='True']
 out=dict(scope='PARTIAL_PREFIX_DIAGNOSTIC, not a fullcoverage result'if args.partial else('Real first32qualification only'if args.qualification else'Complete original7808ownhook observation'),
 observed_entries=len(rows),observed_source_count=len({x['source_id']for x in rows}),
 supported_entries=len(supported),supported_source_count=len({x['source_id']for x in supported}),
 unsupported_reasons=dict(collections.Counter(x['payload'].get('reason')for x in rows if not x['payload']['supported'])),
 witness_entries=len(witnesses),witness_source_count=len(ids),witness_source_IDs=ids,witnesses=witnesses,
 witness_current_statuses=dict(by_status),historical_failure_witness_IDs=known_old_failure,
 historical_failure_witness_HTTP_sum_seconds=sum(float(costs[i]['recorded_HTTP_seconds'])for i in known_old_failure),
 historical_witness_timeouts=[i for i in ids if costs[i]['status']=='timeout_error'],
 proposal_errors=unknown,analysis_seconds=time.monotonic()-started,point_count=4096,seed=0,
 limitations=['No witness is unknown, not validity or falsity proof.',
 'Historical request spans overlap and are associations, not savedwholewall or currentprofilefractions.',
 'A witness in an acceptedcandidate may be an abandonedfalsebranch; failonlythat tactic, neverkillthewholecandidate.',
 'Unsupported terms/fullcontext conditions retain nativefallback. GPU is not running in this census.'])
 # One denominator ledger: unknown is explicit, never reclassified as true.
 expected=sorted(results if args.qualification else costs)
 grouped=collections.defaultdict(list)
 for row in rows:grouped[row['source_id']].append(row)
 witness_ids=set(ids);error_ids={x['source_id']for x in unknown}
 ledger=[]
 for sid in expected:
  entries=grouped[sid];ok=sum(bool(x['payload']['supported'])for x in entries)
  state=('exact_witness'if sid in witness_ids else'proposal_error'if sid in error_ids
   else'supported_no_witness'if ok else'unsupported_only'if entries else'no_observed_entry')
  old=costs[sid];current=results.get(sid)
  ledger.append(dict(source_id=sid,observation_class=state,observed_entries=len(entries),
   supported_entries=ok,unsupported_entries=len(entries)-ok,
   exporter_sum_ns=sum(x.get('export_ns',0)for x in entries),
   current_status=current['status']if current else'not_returned',
   current_reported_body_seconds=(current.get('result',{}).get('time')if current else None),
   historical_status=old['status'],historical_failed=old['failed']=='True',
   historical_reported_body_seconds=float(old['reported_body_seconds']),
   historical_recorded_HTTP_seconds=float(old['recorded_HTTP_seconds'])))
 partitions={}
 for status_field in ['current_status','historical_status']:
  groups=collections.defaultdict(list)
  for row in ledger:groups[(row[status_field],row['observation_class'])].append(row)
  partitions[status_field]=[
   dict(status=status,observation_class=kind,sources=len(items),
    observed_entries=sum(x['observed_entries']for x in items),
    supported_entries=sum(x['supported_entries']for x in items),
    historical_body_sum_seconds=sum(x['historical_reported_body_seconds']for x in items),
    historical_HTTP_sum_seconds=sum(x['historical_recorded_HTTP_seconds']for x in items))
   for(status,kind),items in sorted(groups.items())]
 out.update(expected_sources=len(expected),source_class_counts=dict(collections.Counter(x['observation_class']for x in ledger)),
  source_partitions=partitions,
  exporter_sum_seconds=sum(x['exporter_sum_ns']for x in ledger)/1e9,
  denominator_note='Source partitions cover the declared input; unobserved/unsupported/no-witness remain unknown. Historical spans overlap and cannot be credited as eliminated work. Current diagnostic body timings include observation cost.')
 prefix='qualification32v3'if args.qualification else'partial'if args.partial else'full'
 dest_csv=A/(prefix+'-source-coverage.csv')
 with dest_csv.open('w',newline='')as f:
  writer=csv.DictWriter(f,fieldnames=list(ledger[0]),lineterminator='\n')
  writer.writeheader();writer.writerows(ledger)
 out['source_ledger']=str(dest_csv.relative_to(R))
 dest=A/('qualification32v3-coverage.json'if args.qualification else'partial-coverage.json'if args.partial else'full-coverage.json')
 dest.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k not in['witnesses','unsupported_reasons','limitations']},indent=2))
if __name__=='__main__':main()
