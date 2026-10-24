"""Typed actual-goal coverage. Partial mode is a labelled diagnostic only."""
from pathlib import Path
import argparse,collections,csv,gzip,json,math,time
from point_proposals import inspect
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def load_rows(p,strict=False):
 if p.exists():
  f=p.open()
 else:f=gzip.open(p.with_name(p.name+'.gz'),'rt')
 with f:
  for line in f:
   if not line.endswith('\n'):
    if strict:raise RuntimeError('Closed input has an incomplete final line: '+str(p))
    break
   if line.strip():yield json.loads(line)
def main():
 p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');p.add_argument('--qualification',action='store_true');p.add_argument('--goals',type=Path);p.add_argument('--output-dir',type=Path,default=A);args=p.parse_args()
 args.output_dir.mkdir(parents=True,exist_ok=True)
 directory=A/('qualification32v3-observe'if args.qualification else'full-observe/verification')
 terminal=directory/'terminal.json'
 closed=json.loads(terminal.read_text())if terminal.exists()else None
 if not args.partial:
  if not closed or closed['state']!='complete':raise RuntimeError('The original capture has not completed')
  if closed['memory_watchdog']['error']or closed['owned_live_descendants_after_shutdown']:
   raise RuntimeError('Capture monitoring or child retirement incomplete')
 result_rows=list(load_rows(directory/'results.jsonl',strict=not args.partial))if (terminal.exists()or(directory/'results.jsonl').exists()or(directory/'results.jsonl.gz').exists())else[]
 results={x['proof_id']:x for x in result_rows}
 if len(results)!=len(result_rows):raise RuntimeError('Duplicate final source IDs')
 if not args.partial and len(results)!=closed['expected']:raise RuntimeError('Closed source denominator incomplete')
 with(A/'failure-source-costs.csv').open()as f:costs={x['proof_id']:x for x in csv.DictReader(f)}
 rows=list(load_rows(args.goals or(directory/'goals.jsonl'),strict=not args.partial));supported=[x for x in rows if x['payload']['supported']]
 witnesses=[];unknown=[];sampling=[];started=time.monotonic()
 for x in supported:
  try:
   w,diagnostic=inspect(x['payload']['ast'])
   sampling.append(dict(source_id=x['source_id'],entry_ns=x['entry_ns'],**diagnostic))
  except Exception as ex:unknown.append(dict(source_id=x['source_id'],entry_ns=x['entry_ns'],error=repr(ex)));continue
  if w:witnesses.append(dict(source_id=x['source_id'],entry_ns=x['entry_ns'],witness=w,ast=x['payload']['ast']))
 ids=sorted({x['source_id']for x in witnesses})
 by_status=collections.Counter(results[i]['status']if i in results else'no_final_current_response_yet'for i in ids)
 known_old_failure=[i for i in ids if costs[i]['failed']=='True']
 out=dict(scope='PARTIAL_PREFIX_DIAGNOSTIC, not a fullcoverage result'if args.partial else('Real first32qualification only'if args.qualification else'Complete original7808ownhook observation'),
 input_goals=str(args.goals or(directory/'goals.jsonl')),observed_entries=len(rows),observed_source_count=len({x['source_id']for x in rows}),
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
 if not args.partial and set(results)!=set(expected):raise RuntimeError('Closed input source IDs differ from the declared population')
 http_path=(args.goals.parent/'http.jsonl')if args.goals else(directory/'http.jsonl')
 responses=collections.defaultdict(list)
 for event in load_rows(http_path,strict=not args.partial):
  if event.get('event')!='response':continue
  snippets=json.loads(event['request']).get('snippets',[])
  if len(snippets)!=1 or snippets[0]['id']not in expected:continue
  responses[snippets[0]['id']].append(event)
 duplicate_http={sid:len(es)for sid,es in responses.items()if len(es)!=1}
 missing_http=[sid for sid in expected if sid not in responses]
 if not args.partial and(duplicate_http or missing_http):raise RuntimeError('Closed source HTTP attempts missing or ambiguous')
 # Partial output remains explicit about missing/repeated current responses.
 # No historical clock is substituted for these current HTTP observations.
 grouped=collections.defaultdict(list)
 for row in rows:grouped[row['source_id']].append(row)
 witness_ids=set(ids);error_ids={x['source_id']for x in unknown}
 ledger=[]
 for sid in expected:
  entries=grouped[sid];ok=sum(bool(x['payload']['supported'])for x in entries)
  state=('exact_witness'if sid in witness_ids else'proposal_error'if sid in error_ids
   else'supported_no_witness'if ok else'unsupported_only'if entries else'no_observed_entry')
  old=costs[sid];current=results.get(sid)
  response=responses[sid][0]if len(responses[sid])==1 else None
  inside=[x for x in entries if response and response['start_ns']<=x['entry_ns']<=response['end_ns']]
  refuted_inside=[x for x in witnesses if x['source_id']==sid and response and response['start_ns']<=x['entry_ns']<=response['end_ns']]
  first_witness=min((x['entry_ns']for x in refuted_inside),default=None)
  ledger.append(dict(source_id=sid,observation_class=state,observed_entries=len(entries),
   supported_entries=ok,unsupported_entries=len(entries)-ok,
   exporter_sum_ns=sum(x.get('export_ns',0)for x in entries),
   current_status=current['status']if current else'not_returned',
   current_reported_body_seconds=(current.get('result',{}).get('time')if current else None),
   current_HTTP_seconds=(response['end_ns']-response['start_ns'])/1e9 if response else None,
   entries_inside_current_HTTP=len(inside),
   entries_outside_current_HTTP=(len(entries)-len(inside))if response else None,
   witnessed_entries_inside_current_HTTP=len(refuted_inside),
   response_tail_after_first_witness_seconds=(response['end_ns']-first_witness)/1e9 if first_witness is not None else None,
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
    historical_HTTP_sum_seconds=sum(x['historical_recorded_HTTP_seconds']for x in items),
    current_HTTP_sum_seconds=sum(x['current_HTTP_seconds']for x in items if x['current_HTTP_seconds']is not None),
    current_HTTP_missing_sources=sum(x['current_HTTP_seconds']is None for x in items),
    current_reported_body_sum_seconds=sum(x['current_reported_body_seconds']for x in items if x['current_reported_body_seconds']is not None),
    current_reported_body_missing_sources=sum(x['current_reported_body_seconds']is None for x in items))
   for(status,kind),items in sorted(groups.items())]
 out.update(expected_sources=len(expected),source_class_counts=dict(collections.Counter(x['observation_class']for x in ledger)),
  source_partitions=partitions,
  exporter_sum_seconds=sum(x['exporter_sum_ns']for x in ledger)/1e9,
  denominator_note='Source partitions cover the declared input; unobserved/unsupported/no-witness remain unknown. Historical spans overlap and cannot be credited as eliminated work. Current diagnostic body timings include observation cost.')
 def cohort(items):
  items=list(items)
  return dict(sources=len(items),current_statuses=dict(collections.Counter(x['current_status']for x in items)),
   classes=dict(collections.Counter(x['observation_class']for x in items)),
   exact_witness_sources=sum(x['observation_class']=='exact_witness'for x in items),
   exact_witness_inside_HTTP_sources=sum(x['witnessed_entries_inside_current_HTTP']>0 for x in items),
   HTTP_sum_seconds=sum(x['current_HTTP_seconds']for x in items if x['current_HTTP_seconds']is not None),
   HTTP_missing_sources=sum(x['current_HTTP_seconds']is None for x in items),
   reported_body_sum_seconds=sum(x['current_reported_body_seconds']for x in items if x['current_reported_body_seconds']is not None),
   reported_body_missing_sources=sum(x['current_reported_body_seconds']is None for x in items),
   witness_source_HTTP_sum_seconds=sum(x['current_HTTP_seconds']for x in items if x['observation_class']=='exact_witness'and x['current_HTTP_seconds']is not None))
 returned=[x for x in ledger if x['current_status']!='not_returned']
 ranked=sorted((x for x in returned if x['current_HTTP_seconds']is not None),key=lambda x:x['current_HTTP_seconds'],reverse=True)
 cohorts=dict(all_declared_sources=cohort(ledger),
  current_returned_sources=cohort(returned),
  current_failed_sources=cohort(x for x in returned if x['current_status']!='valid'),
  current_timeouts=cohort(x for x in returned if x['current_status']=='timeout_error'),
  current_resource_failures=cohort(x for x in returned if x['current_status']=='resource_failure'),
  observation_slowest_1_percent=cohort(ranked[:math.ceil(len(ranked)*.01)]),
  observation_slowest_10_percent=cohort(ranked[:math.ceil(len(ranked)*.1)]))
 out.update(current_HTTP_input=str(http_path),current_HTTP_missing_IDs=missing_http,
  current_HTTP_duplicate_IDs=duplicate_http,current_observation_cohorts=cohorts,
  entries_outside_matched_current_HTTP=sum(x['entries_outside_current_HTTP']or 0 for x in ledger),
  current_capture_clocks=({k:closed.get(k)for k in ['expected','returned','own_method_mode','whole_lifecycle_seconds','warm_verify_seconds','input_preparation_seconds','whole_including_input_preparation_seconds','memory_watchdog','source_concurrency','affinity','aggregate_memory_budget_bytes','per_native_repl_address_limit_bytes','maximum_live_native_repls']}if closed and not args.partial else None),
  current_cost_scope='Current request/body sums overlap and include observation overhead; this is neither a native/off-on speedup nor an Amdahl/avoidable-work bound. Tails are ranked by this observation, not an uninstrumented baseline. Missing timing remains explicit.')
 prefix='qualification32v3'if args.qualification else'partial'if args.partial else'full'
 dest_csv=args.output_dir/(prefix+'-source-coverage.csv')
 with dest_csv.open('w',newline='')as f:
  writer=csv.DictWriter(f,fieldnames=list(ledger[0]),lineterminator='\n')
  writer.writeheader();writer.writerows(ledger)
 out['source_ledger']=str(dest_csv.relative_to(R))
 sample_dest=args.output_dir/(prefix+'-sampling-diagnostics.jsonl')
 with sample_dest.open('w')as f:
  for diagnostic in sampling:f.write(json.dumps(diagnostic,separators=(',',':'))+'\n')
 out['sampling_diagnostics']=str(sample_dest.relative_to(R))
 out['sampling_summary']=dict(entries=len(sampling),
  zero_float_feasible_entries=sum(x['float_all_hypotheses_points']==0 for x in sampling),
  zero_float_feasible_historical_failed_entries=sum(x['float_all_hypotheses_points']==0 and costs[x['source_id']]['failed']=='True'for x in sampling),
  float_counterexample_proposals=sum(x['float_counterexample_proposals']for x in sampling),
  exact_candidates_checked=sum(x['exact_candidates_checked']for x in sampling),
  note='Counts of numeric proposals, not exact feasible-point coverage or proof of absence.')

 dest=args.output_dir/('qualification32v3-coverage.json'if args.qualification else'partial-coverage.json'if args.partial else'full-coverage.json')
 dest.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k not in['witnesses','unsupported_reasons','limitations']},indent=2))
if __name__=='__main__':main()
