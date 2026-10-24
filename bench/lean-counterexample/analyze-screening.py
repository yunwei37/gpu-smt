"""Analyze a closed own off/on pair, with failures and fixed baseline tails."""
from pathlib import Path
import argparse,collections,csv,gzip,json,math
def rows(path):
 source=path if path.exists()else path.with_name(path.name+'.gz')
 with(gzip.open(source,'rt')if source.suffix=='.gz'else source.open())as stream:
  for line in stream:
   if not line.endswith('\n'):raise RuntimeError('Only closed, newline-complete results are admissible')
   if line.strip():yield json.loads(line)
def elapsed(a,b):
 return a/b if b>0 else None
def read_cell(directory):
 terminal=json.loads((directory/'terminal.json').read_text())
 if terminal['state']!='complete':raise RuntimeError('Preserve partial cell; not a completed pair')
 if terminal['memory_watchdog']['error']or terminal['owned_live_descendants_after_shutdown']:
  raise RuntimeError('Monitoring or retirement incomplete')
 data=list(rows(directory/'results.jsonl'))
 ids=[x['proof_id']for x in data]
 if len(set(ids))!=len(ids)or terminal['returned']!=len(ids):raise RuntimeError('Result IDs incomplete')
 responses=collections.defaultdict(list)
 for x in rows(directory/'http.jsonl'):
  if x.get('event')!='response':continue
  request=json.loads(x['request']);sources=request.get('snippets',[])
  if len(sources)!=1:continue
  sid=sources[0]['id']
  if sid in ids:responses[sid].append((x['end_ns']-x['start_ns'])/1e9)
 if any(len(responses[sid])!=1 for sid in ids):
  raise RuntimeError('HTTP attempt ambiguity; retain retries and inspect before comparing')
 return terminal,{x['proof_id']:x for x in data},{sid:v[0]for sid,v in responses.items()}
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--off',type=Path,required=True);p.add_argument('--on',type=Path,required=True)
 p.add_argument('--out',type=Path,required=True)
 p.add_argument('--lifecycle',type=Path);p.add_argument('--preparation',type=Path)
 args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
 off,a,ta=read_cell(args.off);on,b,tb=read_cell(args.on)
 if list(a)!=list(b):raise RuntimeError('Different original source order/set')
 for key in ['source_concurrency','affinity','aggregate_memory_budget_bytes',
             'per_native_repl_address_limit_bytes','maximum_live_native_repls']:
  if off[key]!=on[key]:raise RuntimeError('Resource mismatch: '+key)
 acceptance_changes=[sid for sid in a if(a[sid]['status']=='valid')!=(b[sid]['status']=='valid')]
 changes=[dict(source_id=sid,off=a[sid]['status'],on=b[sid]['status'])for sid in a if a[sid]['status']!=b[sid]['status']]
 def group(ids):
  ids=list(ids)
  return dict(sources=len(ids),off_counts=dict(collections.Counter(a[i]['status']for i in ids)),
   on_counts=dict(collections.Counter(b[i]['status']for i in ids)),
   off_HTTP_sum_seconds=sum(ta[i]for i in ids),on_HTTP_sum_seconds=sum(tb[i]for i in ids),
   off_reported_body_sum_seconds=sum(a[i]['result'].get('time',0)or 0 for i in ids),
   on_reported_body_sum_seconds=sum(b[i]['result'].get('time',0)or 0 for i in ids))
 ranked=sorted(a,key=lambda i:ta[i],reverse=True)
 groups={'all_sources':group(a),'baseline_failed':group(i for i in a if a[i]['status']!='valid'),
  'baseline_timeout':group(i for i in a if a[i]['status']=='timeout_error'),
  'baseline_slowest_1_percent':group(ranked[:math.ceil(len(a)*.01)]),
  'baseline_slowest_10_percent':group(ranked[:math.ceil(len(a)*.1)])}
 entries=list(rows(args.on/'goals.jsonl'))if(args.on/'goals.jsonl').exists()or(args.on/'goals.jsonl.gz').exists()else[]
 screening=dict(entries=len(entries),cpu_closed_entries=sum(x.get('answer',{}).get('evaluation_backend')=='cpu_closed'for x in entries),supported_entries=sum(x['payload']['supported']for x in entries),
  exact_refuted_entries=sum(bool(x.get('answer',{}).get('exact_counterexample'))for x in entries),
  exact_refuted_sources=sorted({x['source_id']for x in entries if x.get('answer',{}).get('exact_counterexample')}),
  fallback_errors=dict(collections.Counter(x['answer']['fallback_error']for x in entries if x.get('answer',{}).get('fallback_error'))),
  returned_point_recheck_failures=sum(x.get('answer',{}).get('candidate_point_received',False)and not x['answer'].get('candidate_exact_recheck_passed')for x in entries),
  provider_backends=dict(collections.Counter(x['answer']['provider_backend']for x in entries if x.get('answer',{}).get('provider_backend'))))
 output=dict(scope='One closed own off/on pair; fixed order, root self-review required. Acceptance means the recorded SDK status valid.',
  source_count=len(a),off_mode=off.get('own_mode',off.get('own_method_mode')),
  on_mode=on.get('own_mode',on.get('own_method_mode')),acceptance_changed_sources=acceptance_changes,
  status_changes=changes,groups=groups,screening=screening,
  off_warm_verify_seconds=off['warm_verify_seconds'],on_warm_verify_seconds=on['warm_verify_seconds'],
  warm_whole_group_ratio=elapsed(off['warm_verify_seconds'],on['warm_verify_seconds']),
  off_native_lifecycle_seconds=off['whole_lifecycle_seconds'],on_native_lifecycle_seconds=on['whole_lifecycle_seconds'],
  native_lifecycle_ratio=elapsed(off['whole_lifecycle_seconds'],on['whole_lifecycle_seconds']),
  resource_point={k:off[k]for k in ['source_concurrency','affinity','aggregate_memory_budget_bytes',
   'per_native_repl_address_limit_bytes','maximum_live_native_repls']},
  memory={name:terminal['memory_watchdog']for name,terminal in [('off',off),('on',on)]},
  limitations=['Qualification is not full benchmark evidence. No inference of acceleration if the on mode is observe.',
   'HTTP and reported-body sums overlap across candidates: they are cumulative outcome-conditioned costs, not whole elapsed savings.',
   'Tail cohorts are fixed by baseline HTTP time, then compared on identical IDs; timeouts and resource failures remain.',
   'One off-first pair does not quantify run-order/host-load variance; existing captures are not rescaled.',
   'Native cell lifecycle excludes provider creation/retirement and own input parsing; cold decomposition requires the controller receipt.',
   'Opaque environment handles/error messages may differ; the reported accepted-set/status check is not full response equivalence.'])
 if args.lifecycle:
  life=json.loads(args.lifecycle.read_text())
  if life['clientExit']!=0 or life['providerExit']!=0 or life['ownJobRemains']or life['cleanupErrors']:
   raise RuntimeError('Provider lifecycle incomplete; preserve raw before comparison')
  prep=json.loads(args.preparation.read_text())['preparation_seconds']if args.preparation else None
  output['provider_lifecycle']=life
  output['cold_time_accounting']=dict(
   combined_pair_controller_seconds=life['completeColdLifecycleSeconds'],
   provider_creation_to_API_seconds=life['startupToAPIReadySeconds'],provider_retirement_seconds=life['retirementSeconds'],
   shared_input_preparation_seconds=prep,
   native_with_own_preparation_seconds=off['whole_lifecycle_seconds']+prep if prep is not None else None,
   on_controller_residual_seconds=life['completeColdLifecycleSeconds']-off['whole_lifecycle_seconds'],
   note='Controller residual removes the measured native off cell from the combined pair clock; it includes input preparation, GPU path, API/controller overhead and provider retirement. It is an explicit cold accounting convention, not an isolated second run.')
 with(args.out/'paired-sources.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=['source_id','off_status','on_status','off_HTTP_seconds','on_HTTP_seconds'],lineterminator='\n');w.writeheader()
  for sid in a:w.writerow(dict(source_id=sid,off_status=a[sid]['status'],on_status=b[sid]['status'],off_HTTP_seconds=ta[sid],on_HTTP_seconds=tb[sid]))
 (args.out/'result.json').write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps({k:v for k,v in output.items()if k not in ['memory','provider_lifecycle']},indent=2))
if __name__=='__main__':main()
