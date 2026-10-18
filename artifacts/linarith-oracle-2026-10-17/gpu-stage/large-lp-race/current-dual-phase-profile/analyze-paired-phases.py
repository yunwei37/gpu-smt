from pathlib import Path
import json,gzip,collections,importlib.util
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile'
U=A/'full1000-raw'
REF=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/two-sided-oracle/full1000-third'
spec=importlib.util.spec_from_file_location('phase',A/'analyze-current-phases.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
n=json.loads((A/'full1000-fast-hybrid-phase-analysis.json').read_text());c=json.loads((A/'full1000-oracle-highs-phase-analysis.json').read_text())
def responses(d):return{x['proof_id']:x for x in m.rows(d/'responses.jsonl.gz')}
N=responses(U/'rep1-fast-hybrid');C=responses(U/'rep1-oracle-highs');RN=responses(REF/'rep1-fast-hybrid');RC=responses(REF/'rep1-oracle-highs')
def compare(a,b):
 assert a.keys()==b.keys()
 return {'sources':len(a),'verdict_differences':[k for k in a if a[k]['outcome']!=b[k]['outcome']],
  'full_JSON_differences':[k for k in a if a[k]['response']!=b[k]['response']],
  'non_message_differences':[k for k in a if {x:y for x,y in a[k]['response'].items()if x!='messages'}!={x:y for x,y in b[k]['response'].items()if x!='messages'}]}
nc=compare(N,C);nr=compare(N,RN);cr=compare(C,RC)
assert not nc['verdict_differences']and not nc['non_message_differences']
assert not nr['verdict_differences']and not nr['non_message_differences']
assert not cr['verdict_differences']and not cr['non_message_differences']
races=list(m.rows(U/'rep1-oracle-highs/lp-races.jsonl'));rk={(x['source'],x['call_id'])for x in races};assert len(rk)==len(races)
external=list(m.rows(U/'rep1-oracle-highs-backend/support-calls.jsonl.gz'));parsed=[x for x in external if x['rows']is not None]
for x in parsed:assert(x['input']['source'],x['input']['call_id'])in rk
solver=sum(x['reply']['solver_seconds']for x in parsed)
build=sum(x['reply']['build_ns']for x in parsed)/1e9
call=sum(x['reply']['call_ns']for x in parsed)/1e9
proxy_cpu=sum(x['thread_cpu_ns']for x in external)/1e9
tails={};pn={x['proof_id']:x for x in n['per_candidate']};pc={x['proof_id']:x for x in c['per_candidate']}
for fraction in ['0.01','0.1']:
 ids=n['own_ranked_tail'][fraction]['proof_ids'];out={}
 for label,p in [('native',pn),('CPU_oracle',pc)]:
  a=collections.Counter();b=collections.Counter()
  for k in ids:a.update(p[k]['Lean_exclusive_calling_thread_CPU_seconds']);b.update(p[k]['numeric_reply_elapsed_sums_seconds_NOT_CPU'])
  out[label]={'summed_candidate_service_seconds':sum(p[k]['service_seconds']for k in ids),
   'Lean_exclusive_calling_thread_CPU_seconds':dict(a),'numeric_reply_elapsed_sums_seconds_NOT_CPU':dict(b)}
 tails[fraction]={'native_ranked_proof_ids':ids,'comparison':out,'scope':'Same source IDs selected by native individual service spans. Sums overlap; not a cohort elapsed ratio.'}
wholeN=n['terminal']['whole_ns']/1e9;wholeC=c['terminal']['whole_ns']/1e9
en=n['optimistic_fixed_path_envelope'];ec=c['optimistic_fixed_path_envelope']
result={'scope':'Own-clock complete current-build diagnostic pair. All logging/metadata/gzip and proxy lifecycle charged. Not a fourth primary pair or a globally strongest-CPU claim.',
 'native_seconds':wholeN,'CPU_oracle_seconds':wholeC,'diagnostic_native_over_CPU':wholeN/wholeC,
 'fidelity':{'native_versus_retained_native':nr,'CPU_versus_retained_CPU':cr,'native_versus_CPU':nc},
 'data_quality':{'native':n['data_quality_defects'],'CPU':c['data_quality_defects']},
 'current_external_HiGHS':{'races':len(races),'race_winners':dict(collections.Counter(x['winner']for x in races)),
 'race_whole_elapsed_sum_seconds':sum(x['whole_ns']for x in races)/1e9,
 'legacy_winner_label_scope':'gpu means external CPU HiGHS in this CPU-only cell; no CUDA work occurred.','parsed':len(parsed),'aborted_or_unparsed':len(external)-len(parsed),
 'solver_elapsed_sum_seconds':solver,'build_elapsed_sum_seconds':build,'call_elapsed_sum_seconds':call,
 'proxy_calling_thread_CPU_sum_seconds':proxy_cpu,'actual_float_shapes':{k:m.quant([x[k]for x in parsed])for k in ['rows','cols','nnz']},
 'models_with_cross_source_lifetime_overlap':sum(any(i!=j and x['input']['source']!=y['input']['source']and x['start_ns']<y['end_ns']and y['start_ns']<x['end_ns']for j,y in enumerate(parsed))for i,x in enumerate(parsed)),
 'LP_model_availability':m.overlap([dict(start_ns=x['start_ns'],end_ns=x['end_ns'],source=x['input']['source'])for x in parsed]),
 'scope':'935 parsed floating-model requests are a subset of all current numerical calls; unparsed/cancelled worker compute remains unknown.'},
 'zero_cost_sensitivity_NOT_strict_Amdahl':{'native_full_products_LP_RPC_envelope_fraction':en['occupied_union_fraction'],
 'native_fixed_lane_zero_envelope_seconds':en['fixed_lane_model_whole_seconds'],'native_over_native_zero_envelope':wholeN/en['fixed_lane_model_whole_seconds'],
 'CPU_full_products_LP_RPC_envelope_fraction':ec['occupied_union_fraction'],'CPU_fixed_lane_zero_envelope_seconds':ec['fixed_lane_model_whole_seconds'],
 'native_over_CPU_zero_envelope':wholeN/ec['fixed_lane_model_whole_seconds'],'scope':ec['scope'],
 'closure_decision':'Both optimistic fixed-path sensitivities remain above1.5, and neither is a scheduler-independent proof. Overall GPU impossibility is not established; do not close the project or hourly task.'},
 'native_ranked_tail_comparison':tails,
 'missing_for_strict_attribution':['current native/cancelled numerical-worker internal pure-LP CPU and exact-repair split',
 'GPU-ready intervals separated from IPC/locks','support-changing/scheduling behavior versus fixed-path sensitivity',
 'strongest matched native-frontend controls and full-population generality']}
(A/'full1000-paired-phase-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in ['fidelity','native_ranked_tail_comparison']},indent=2))
print('FIDELITY_COUNTS',{k:{x:len(y)if isinstance(y,list)else y for x,y in v.items()}for k,v in result['fidelity'].items()})
