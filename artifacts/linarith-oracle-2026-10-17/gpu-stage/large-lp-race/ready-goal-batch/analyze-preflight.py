from pathlib import Path
import json,gzip,collections
A=Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/ready-goal-batch')
def rows(p):
 with(gzip.open(p,'rt')if p.suffix=='.gz'else open(p))as f:return list(map(json.loads,f))
raw=A/'preflight-raw';result={}
base={x['proof_id']:x for x in rows(raw/'sequential/rep1-oracle-highs/responses.jsonl.gz')}
for label in ['sequential','ready-batch']:
 d=raw/label;t=json.loads((d/'rep1-oracle-highs/terminal.json').read_text());rs={x['proof_id']:x for x in rows(d/'rep1-oracle-highs/responses.jsonl.gz')}
 assert base.keys()==rs.keys()
 verdict=[k for k in base if base[k]['outcome']!=rs[k]['outcome']]
 non=[k for k in base if {a:b for a,b in base[k]['response'].items()if a!='messages'}!={a:b for a,b in rs[k]['response'].items()if a!='messages'}]
 assert not verdict and not non
 result[label]={'whole_seconds':t['whole_ns']/1e9,'counts':t['counts'],'verdict_differences':verdict,'non_message_differences':non,'full_JSON_differences':[k for k in base if base[k]['response']!=rs[k]['response']],'observer_errors':t['sampling_read_errors'],'effective_RLIMIT_AS':t['effective_RLIMIT_AS']}
events=rows(raw/'ready-batch/goal-batches.jsonl');ok=[x for x in events if x['outcome']=='checked']
keys=[(x['source'],i)for x in ok for i in x['call_ids']];assert len(keys)==len(set(keys))
calls=rows(raw/'ready-batch/rep1-oracle-highs-backend/support-calls.jsonl.gz')
parsed=[x for x in calls if x['rows']is not None]
eligible=[x for x in parsed if(x['input']['source'],x['input']['call_id'])in set(keys)]
result.update(scope='Real12-source CPU preflight, common omega,4CPU8--11/eightqueues/48GiB; arithmetic batch formation is not GPU performance.',
 batch_outcomes=dict(collections.Counter(x['outcome']for x in events)),batch_sizes=[x['models']for x in ok],
 checked_problems=sum(x['checked']for x in ok),per_problem_native_fallback=sum(x['fallback']for x in ok),
 outer_fallbacks=[{'goals':x['goals'],'error':x['error']}for x in events if x['outcome']!='checked'],
 numerical_workers=sorted(set(x['numeric_workers']for x in ok)),
 parsed_external_LP_requests_in_ready_groups=len(eligible),
 latency_reduction=1-result['ready-batch']['whole_seconds']/result['sequential']['whole_seconds'],
 limitation='Only bare arithmetic tails covered. Initial grouped numerical replies/LP shapes are not retained; this count describes exported arithmetic problems, not large-GPU eligibility or device kernels. No GPU run or full-matrix admission.')
(A/'preflight-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
