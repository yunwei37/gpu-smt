"""Reuse native profiles and full-source controls; no candidate execution."""
from pathlib import Path
import collections,csv,gzip,json,re,runpy
R=Path(__file__).resolve().parents[2];A=Path(__file__).resolve().parent
source=json.loads(gzip.decompress((R/'artifacts/engine-resource-profile-2026-10-25/population-inputs/all.json.gz').read_bytes()))
codes={x['id']:x for x in source['candidates']}
strip=runpy.run_path(str(R/'bench/lean-candidate-scheduling/analyze.py'))['strip_comments']
profile=json.loads((R/'artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json').read_text())
base=R/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off/results.jsonl'
base=base if base.exists()else base.with_suffix(base.suffix+'.gz')
with(gzip.open(base,'rt')if base.suffix=='.gz'else base.open())as stream:
 native={x['proof_id']:x for x in map(json.loads,stream)}
assert set(codes)==set(native)and len(codes)==7808
def features(code):
 text=strip(code)
 return dict(interval_cases=len(re.findall(r'\binterval_cases\b',text)),
   simp_all=bool(re.search(r'\bsimp_all\b',text)),
   modular_rules=any(rule in text for rule in ['Nat.mul_mod','Nat.add_mod','Nat.pow_mod']),
   commutative_rules=any(rule in text for rule in ['add_comm','mul_comm','add_left_comm','mul_left_comm']),
   mentions_pow_succ='pow_succ'in text,
   finite_sum_rule='Finset.sum_range_succ'in text)
feats={sid:features(row['code'])for sid,row in codes.items()}
predicates={
 'mentions_interval_cases':lambda f:f['interval_cases']>0,
 'mentions_three_or_more_interval_cases':lambda f:f['interval_cases']>=3,
 'mentions_simp_all':lambda f:f['simp_all'],
 'simp_all_and_modular_rule_somewhere_in_source':lambda f:f['simp_all']and f['modular_rules'],
 'simp_all_and_commutative_rule_somewhere_in_source':lambda f:f['simp_all']and f['commutative_rules'],
 'simp_all_and_finite_sum_rule_somewhere_in_source':lambda f:f['simp_all']and f['finite_sum_rule'],
 'simp_all_and_pow_succ_somewhere_in_source':lambda f:f['simp_all']and f['mentions_pow_succ']}
controls={}
for name,pred in predicates.items():
 ids=[sid for sid,f in feats.items()if pred(f)]
 controls[name]=dict(sources=len(ids),statuses=dict(collections.Counter(native[sid]['status']for sid in ids)),
   accepted_counterexample_ids=[sid for sid in ids if native[sid]['status']=='valid'][:12],
   scope='Source-token engagement only; not exact tactic-state/argument attribution or sufficient failure evidence.')
timeouts=[x for x in profile if x['baseline_status']=='timeout_error'];assert len(timeouts)==83
families=collections.defaultdict(lambda:dict(cpu_ns=0,ids=[],tasks=set()))
rows=[]
for item in timeouts:
 sid=item['source_id'];weights=collections.Counter()
 for value in item['sampled_CPU_weights']:
  if value['family']=='tactic':weights[value['key']]+=value['nanoseconds']
 dominant=max(weights,key=weights.get)
 family='interval_cases'if'intervalCases'in dominant else'simp_all'if'simpAll'in dominant else'other'
 families[family]['cpu_ns']+=weights[dominant]
 families[family]['ids'].append(sid);families[family]['tasks'].add(codes[sid]['task_id'])
 rows.append(dict(source_id=sid,task_id=codes[sid]['task_id'],dominant=dominant,
   dominant_endpoint_cpu_seconds=weights[dominant]/1e9,
   interval_endpoint_cpu_seconds=sum(v for k,v in weights.items()if'intervalCases'in k)/1e9,
   simp_all_endpoint_cpu_seconds=sum(v for k,v in weights.items()if'simpAll'in k)/1e9,
   measured_exclusive_thread_cpu_seconds=item['measured_exclusive_cpu_seconds'],
   **feats[sid]))
rows.sort(key=lambda x:max(x['interval_endpoint_cpu_seconds'],x['simp_all_endpoint_cpu_seconds']),reverse=True)
with(A/'timeouts83.csv').open('w')as stream:
 writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
for value in families.values():
 value['tasks']=sorted(value['tasks'])
 value['dominant_cpu_seconds']=value.pop('cpu_ns')/1e9
 value['count']=len(value['ids'])
result=dict(selected_timeouts=83,whole_population=7808,
 original_status_counts=dict(collections.Counter(x['status']for x in native.values())),
 dominant_groups=dict(families),source_pattern_controls=controls,
 interval_endpoint_cpu_seconds=sum(x['interval_endpoint_cpu_seconds']for x in rows),
 simp_all_endpoint_cpu_seconds=sum(x['simp_all_endpoint_cpu_seconds']for x in rows),
 scope='Completed original480profile83timeouts, own sampled tactic CPU. Original full native statuses for7808source controls. Not a new run, whole-wall saving, per-call parser or failure witness.',
 source_profile='artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json',
 native_status_reference=str(base.relative_to(R)))
(A/'result.json').write_text(json.dumps(result,indent=2)+'\n')
summary=['# Native hotspot mechanism analysis — root self-review','',
 'The83oldtimeouts were fully profiled; source controls retain all7808native outcomes.',
 'No new candidate executed and no runtime/native source was modified.','',
 '|Dominant observed tactic|Timeout sources|Distinct tasks|Dominant sampled CPU(s)|',
 '|---|---:|---:|---:|']
for name,g in families.items():summary.append(f"|{name}|{g['count']}|{len(g['tasks'])}|{g['dominant_cpu_seconds']:.3f}|")
summary+=['','|Source pattern (not a failure witness)|All sources|Accepted|Timeouts|','|---|---:|---:|---:|']
for name,g in controls.items():summary.append(f"|{name}|{g['sources']}|{g['statuses'].get('valid',0)}|{g['statuses'].get('timeout_error',0)}|")
summary+=['','## Native source implications','',
 'Pinned4.9Mathlib IntervalCases.intervalCases first allocates all cases for',
 'one interval and constructs their bisect proof tree; only its frontend then',
 'introduces/substitutes each goal and returns it to following tactics.',
 'A source range/cartesian count is neither a proof of falsehood nor an exact',
 '300s wall-clock lower bound. Nested tactic evaluation/backtracking matters.',
 '',
 'Pinned Lean Simp.simpLoop already stops its post-rewrite recursion when',
 'the expression equals the original (unless other phases recurse). Thus an',
 'unchanged expression after one full root rewrite is already handled by',
 'native Lean; adding that same check is not a new failure mechanism.',
 'Actual time may involve expression growth, multi-step cycles, conditional',
 'discharge or repeated context updates. Current profiles do not distinguish',
 'these; no cycle certificate is inferred from a rule name or CPU category.',
 '',
 'Source-pattern accepted controls invalidate blanket rule-name rejection.',
 'Next native hook must retain expression/context/options and whether the',
 'operation is inside a fallback/try/first/discharger before a checked witness',
 'may reject a complete request. Unknown keeps native execution. Keep hooks',
 'off until the existing sole group retires; no shortened timeout is introduced.',
 '',
 'The detailed83source/task/timing table is timeouts83.csv. Its observed CPU',
 'denominator is the same profile; original cumulative HTTP/whole-controller',
 'clocks are not substituted. This supporting diagnosis does not close an RQ.']
(A/'result-review.md').write_text('\n'.join(summary)+'\n')
print(json.dumps(dict(groups={k:dict(count=v['count'],tasks=len(v['tasks']))for k,v in families.items()},controls={k:v['statuses']for k,v in controls.items()})))
