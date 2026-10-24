"""Existing miniF2F native failure costs, not a counterexample-coverage result."""
from pathlib import Path
import csv,gzip,json,collections
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17'
O=R/'artifacts/arithmetic-counterexample-2026-10-23'
with gzip.open(A/'prefix-opportunity/minif2f-input.jsonl.gz','rt')as f: inputs=[json.loads(x)for x in f]
with gzip.open(A/'shred-closing/aggregate-budget-20261019/full-population/http-full/minif2f/rep1-native/results.jsonl.gz','rt')as f: results=[json.loads(x)for x in f]
with(A/'shred-closing/aggregate-budget-20261019/native-full-source-latencies.csv').open()as f: spans={x['proof_id']:x for x in csv.DictReader(f)}
assert len(inputs)==len(results)==len(spans)==7808
rows=[]
for i,x in enumerate(results):
 assert x['proof_id']=='minif2f-'+str(i)and inputs[i]['index']==i
 body=x['result'].get('time')
 raw=spans[x['proof_id']]['completed_HTTP_attempt_seconds']
 rows.append(dict(proof_id=x['proof_id'],status=x['status'],failed=x['status']!='valid',
  reported_body_seconds=body if isinstance(body,(int,float))else None,
  recorded_HTTP_seconds=float(raw)if raw else None,
  source_mentions_arithmetic='linarith'in inputs[i]['code'],
  printed_linarith_failure='linarith failed to find a contradiction'in json.dumps(x,ensure_ascii=False)))
groups={}
for label,pred in [
 ('all',lambda x:True),('failed',lambda x:x['failed']),('accepted',lambda x:not x['failed']),
 ('timeout',lambda x:x['status']=='timeout_error'),('resource_failure',lambda x:x['status']=='resource_failure'),
 ('failed_source_mentions_arithmetic',lambda x:x['failed']and x['source_mentions_arithmetic']),
 ('timeout_source_mentions_arithmetic',lambda x:x['status']=='timeout_error'and x['source_mentions_arithmetic']),
 ('printed_linarith_failure',lambda x:x['printed_linarith_failure'])]:
 selected=[x for x in rows if pred(x)]
 groups[label]=dict(sources=len(selected),statuses=dict(collections.Counter(x['status']for x in selected)),
  reported_body_sum_seconds=sum(x['reported_body_seconds']for x in selected if x['reported_body_seconds']is not None),
  missing_body_seconds=sum(x['reported_body_seconds']is None for x in selected),
  recorded_HTTP_sum_seconds=sum(x['recorded_HTTP_seconds']for x in selected if x['recorded_HTTP_seconds']is not None),
  missing_HTTP_seconds=sum(x['recorded_HTTP_seconds']is None for x in selected))
out=dict(dataset='All7808originalminiF2Fcandidates',baseline_source='Existing closed native capture, no new external-system replication.',
 groups=groups,failed_fraction_reported_body=groups['failed']['reported_body_sum_seconds']/groups['all']['reported_body_sum_seconds'],
 failed_fraction_HTTP=groups['failed']['recorded_HTTP_sum_seconds']/groups['all']['recorded_HTTP_sum_seconds'],
 counterexample_confirmed_sources=None,
 limitations=['Accumulated request spans overlap, not additive cohort whole wall or CPU.',
 'Textual arithmetic mentions include comments and unexecuted branches; not observed tactic entries.',
 'A printed linarith failure/false goal does not mean a satisfiable context or a false theorem.',
 'Absent exact goal witnesses are unknown, never zero counterexample opportunities.',
 'SDK resource failures report body0 bookkeeping; their actual request costs are not zero.'])
(O/'failure-costs.json').write_text(json.dumps(out,indent=2)+'\n')
with(O/'failure-source-costs.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps(out,indent=2))
