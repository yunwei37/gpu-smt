"""Reanalyze existing complete E023 replay timing; no verifier run or SHA gate."""
from pathlib import Path
import json,zipfile,statistics,collections,datetime
R=Path('/workspaces/repository')
D=R/'artifacts/lean-service-lifecycle-2026-10-13/experiment023'
B=D/'full1-proofnet'
prior=json.loads((D/'review-proofnet/recomputed.json').read_text())
old={x['label']:x for x in prior['cells']}
original=(R/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/proofnet/input.jsonl').read_bytes()
inputs=[json.loads(l) for l in original.splitlines()]
def quant(v,p):
 v=sorted(v);a=(len(v)-1)*p;i=int(a)
 return (v[i]+(v[min(i+1,len(v)-1)]-v[i])*(a-i))/1e9
cells=[]
for path in sorted(B.glob('proofnet-*.zip')):
 label=path.stem
 terminal=json.loads((B/(label+'.terminal.json')).read_text())
 with zipfile.ZipFile(path) as z:
  assert z.read(label+'/input.jsonl')==original
  receipt=json.loads(z.read(label+'/receipt.json'))
  with z.open(label+'/results.jsonl') as f:rows=[json.loads(l) for l in f]
  assert terminal['returncode']==0 and len(rows)==len(inputs)==5952
  assert receipt['completed_inputs']==5952
  assert len({r['source_index'] for r in rows})==5952
  for row in rows:
   assert inputs[row['ordinal']]['index']==row['source_index']
   assert row['scheduled_arrival_to_terminal_ns']==row['completion_monotonic_ns']-row['scheduled_arrival_monotonic_ns']
   assert row['scheduled_arrival_to_terminal_ns']==row['generator_lag_ns']+row['pending_queue_ns']+row['dispatch_to_terminal_ns']
  assert receipt['actual_affinity']==[0,1,2,3] and receipt['jobs']==4
  metrics={}
  for key in ['scheduled_arrival_to_terminal_ns','generator_lag_ns','pending_queue_ns','dispatch_to_terminal_ns']:
   v=[row[key] for row in rows]
   metrics[key]={'mean_s':statistics.mean(v)/1e9,'p50_s':quant(v,.5),'p95_s':quant(v,.95),'p99_s':quant(v,.99)}
   for ours,theirs in [('p50_s','p50'),('p95_s','p95'),('p99_s','p99')]:
    assert abs(metrics[key][ours]-old[label]['metrics'][key][theirs])<1e-9
  whole=receipt['whole_capture_ns']/1e9
  assert whole==old[label]['whole']
  cells.append({'label':label,'method':receipt['method'],'rate':receipt['synthetic_arrivals_per_second'],
   'primary':not terminal['profile'],'whole_seconds':whole,'returned':len(rows),'attempts_per_whole_second':len(rows)/whole,
   'cache_returns':sum(bool(row['cached']) for row in rows),'metrics':metrics,'resources':old[label]['resources']})
assert len(cells)==30
aggregate=[]
for rate in sorted({c['rate'] for c in cells if c['primary']}):
 for method in ['prepared','snapshot','branch']:
  cohort=[c for c in cells if c['primary'] and c['rate']==rate and c['method']==method]
  assert len(cohort)==3
  aggregate.append({'rate':rate,'method':method,'whole_seconds':[c['whole_seconds'] for c in cohort],
   'arrival_p95_s':[c['metrics']['scheduled_arrival_to_terminal_ns']['p95_s'] for c in cohort],
   'arrival_mean_s':[c['metrics']['scheduled_arrival_to_terminal_ns']['mean_s'] for c in cohort],
   'generator_mean_s':[c['metrics']['generator_lag_ns']['mean_s'] for c in cohort],
   'queue_mean_s':[c['metrics']['pending_queue_ns']['mean_s'] for c in cohort],
   'dispatch_mean_s':[c['metrics']['dispatch_to_terminal_ns']['mean_s'] for c in cohort]})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'complete_proofnet_cells':30,'total_returned':sum(c['returned']for c in cells),
 'scope':'Existing complete ProofNet half of the planned two-cohort service matrix, not fresh final evaluation. Original sources; synthetic scheduled arrivals; four permitted shared CPUs; three primary repetitions/rate; single profiles separate. Basic-outcome qualification remains the retained prior raw review, not a universal artifact/cancellation claim.',
 'aggregate':aggregate,'cells':cells}
target=Path(__file__).with_name('service-replay-summary.json')
target.write_text(json.dumps(out,indent=2)+'\n')
print('complete_cells',len(cells),'outcomes',out['total_returned'])
for x in aggregate:
 print(json.dumps(x))
