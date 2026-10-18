from pathlib import Path
import json,gzip,collections
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/native-omega-control'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/native-omega-control')
RAW=A/'full1000-raw'if(A/'full1000-raw').exists()else U
def rows(p):
 with(gzip.open(p,'rt')if p.suffix=='.gz'else open(p))as f:return list(map(json.loads,f))
def nonmsg(x):return{k:v for k,v in x.items()if k!='messages'}
cells={}
for label in ['native-dual-omega','direct-dual-omega','direct-dual-off']:
 d=RAW/('full1000-'+label)
 t=json.loads((d/'rep1-oracle-highs/terminal.json').read_text());assert t['state']=='complete'
 rs=rows(d/'rep1-oracle-highs/responses.jsonl.gz');assert len(rs)==1000
 calls=rows(d/'omega-calls.jsonl')if(d/'omega-calls.jsonl').exists()else[]
 cells[label]={'whole_seconds':t['whole_ns']/1e9,'counts':t['counts'],'effective_RLIMIT_AS':t['effective_RLIMIT_AS'],'observer_errors':t['sampling_read_errors'],
  'omega_outcomes':dict(collections.Counter(x['outcome']for x in calls)),'omega_elapsed_sum_seconds':sum(x['end_ns']-x['start_ns']for x in calls)/1e9,
  'responses':{x['proof_id']:x for x in rs}}
base=cells['native-dual-omega']['responses'];comparisons={}
for label,c in cells.items():
 rs=c['responses'];assert base.keys()==rs.keys()
 dif={'verdict':[k for k in base if base[k]['outcome']!=rs[k]['outcome']],
 'non_message':[k for k in base if nonmsg(base[k]['response'])!=nonmsg(rs[k]['response'])],
 'full_JSON':[k for k in base if base[k]['response']!=rs[k]['response']]}
 assert not dif['verdict']and not dif['non_message']
 comparisons[label]=dif
# Original native reference is a fidelity control only, no cross-clock ratio.
ref=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/two-sided-oracle/full1000-third/rep1-fast-hybrid/responses.jsonl.gz'
original={x['proof_id']:x for x in rows(ref)}
original_diffs={}
for label,c in cells.items():
 rs=c['responses'];assert rs.keys()==original.keys()
 original_diffs[label]={'verdict':[k for k in rs if rs[k]['outcome']!=original[k]['outcome']],
 'non_message':[k for k in rs if nonmsg(rs[k]['response'])!=nonmsg(original[k]['response'])],
 'full_JSON':[k for k in rs if rs[k]['response']!=original[k]['response']]}
 assert not original_diffs[label]['verdict']and not original_diffs[label]['non_message']
for c in cells.values():del c['responses']
N=cells['native-dual-omega']['whole_seconds'];D=cells['direct-dual-omega']['whole_seconds'];O=cells['direct-dual-off']['whole_seconds']
result={'scope':'One complete matched1000-source original-order three-condition CPU comparison, 4CPU/8queues/48GiB. Common stock omega and same two-sided numerical backend. Not GPU performance, a confidence interval or global CPU optimum.',
 'cells':cells,'pairwise_native_on_fidelity':comparisons,'original_native_fidelity_only':original_diffs,
 'native_on_over_direct_on':N/D,'direct_on_elapsed_reduction_over_native_on':1-D/N,
 'direct_off_over_direct_on':O/D,'common_omega_direct_elapsed_reduction':1-D/O,
 'decision':'Direct frontend remains faster in this matched block, but incremental advantage is about1.172x against the stronger native frontend, not1.5x. Prior1.50862x primary aggregate retains its original comparator and is not global strongest-CPU evidence. Stock integer solving is prior art; GPU route remains open under user criterion.'}
(A/'full1000-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cells':cells,'native_on_over_direct_on':N/D,'direct_off_over_direct_on':O/D,'pairwise_diff_counts':{k:{n:len(v)for n,v in d.items()}for k,d in comparisons.items()},'original_diff_counts':{k:{n:len(v)for n,v in d.items()}for k,d in original_diffs.items()}},indent=2))
