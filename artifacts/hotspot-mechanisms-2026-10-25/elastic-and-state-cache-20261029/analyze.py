"""Reuse complete native process traces and original native Syntax; no Lean invocation."""
from pathlib import Path
from collections import defaultdict,Counter
import json,gzip,os,time,re
os.sched_setaffinity(0,{11})
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
def read(p):
 p=ROOT/p
 with (gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as f:return json.load(f)
def rows(p):
 with gzip.open(ROOT/p,'rt')as f:return [json.loads(s)for s in f if s.strip()]
start=time.monotonic()
prefix=Path('artifacts/linarith-oracle-2026-10-17/prefix-opportunity')
units={x['proposalId']:x for x in rows(prefix/'native-units.jsonl.gz')}
kinds={'nlinarith','Mathlib.Tactic.intervalCases','Lean.Parser.Tactic.simpAll','Mathlib.Tactic.normNum'}
reused={}
for name in ['minif2f','proofnet']:
 inputs=rows(prefix/(name+'-input.jsonl.gz'))
 seen_prefix=set();seen_text=set();k=Counter();groups=set();text_rows=[];fallback=Counter();by_kind=defaultdict(Counter)
 for c in inputs:
  sid=f"{name}-{c['index']}";u=units.get(sid)
  if not u or not u.get('eligible'):
   fallback['native_parse_or_mapping_unavailable']+=1;continue
  # This delimiter is the retained preparer's statement boundary,not a new proof parser.
  boundary=re.search(r':=\s*by\b',c['code'])
  if boundary is None:
   fallback['no_retained_statement_boundary']+=1;continue
  statement=c['code'][:boundary.end()]
  group=(c['index']//32,c['header'],statement);groups.add(group);path=[]
  for ordinal,tactic in enumerate(u['units']):
   text=tactic['text'];kind=tactic['syntaxKind'];path.append(text)
   pk=(group,tuple(path));tk=(group,kind,text)
   repeat_prefix=pk in seen_prefix;repeat_text=tk in seen_text
   k['steps']+=1;k['rooted_unit_repeats']+=repeat_prefix;k['unrooted_same_text_repeats']+=repeat_text
   by_kind[kind]['occurrences']+=1
   by_kind[kind]['rooted_text_repeats']+=repeat_prefix
   by_kind[kind]['unrooted_text_repeats']+=repeat_text
   if kind in kinds:
    k['expensive_outer_steps']+=1
    k['expensive_rooted_unit_repeats']+=repeat_prefix
    k['expensive_unrooted_same_text_repeats']+=repeat_text
    text_rows.append(dict(id=sid,ordinal=ordinal,kind=kind,rooted_text_repeat=repeat_prefix,
     same_text_repeat=repeat_text,full_context_available=False,tactic_text=text))
   seen_prefix.add(pk);seen_text.add(tk)
 expected=read(prefix/'recomputed-counts.json')[name]
 assert k['steps']==expected['modes']['unit']['occurrences'],(name,k,expected)
 assert k['rooted_unit_repeats']==expected['modes']['unit']['reusable'],(name,k,expected)
 assert len(groups)==expected['statement_specific_groups']
 reused[name]=dict(counts=dict(k),statement_groups=len(groups),fallbacks=dict(fallback),outer_syntax_kind_counts={k:dict(v)for k,v in by_kind.items()},
  rooted_unit_repeat_fraction=k['rooted_unit_repeats']/k['steps'],
  expensive_fraction_of_rooted_unit_repeats=k['expensive_rooted_unit_repeats']/k['rooted_unit_repeats'],
  certified_complete_state_reuse_count=None,cost_of_complete_state_reuse_seconds=None,
  reason='Native Syntax contains no full target/localcontext/environment/options/metavariable state or per-step heartbeats/cost.')
 with gzip.open(OUT/(name+'-expensive-text-candidates.jsonl.gz'),'wt')as f:
  for x in text_rows:f.write(json.dumps(x)+'\n')
# Exact actual low-process-concurrency envelopes,with no CPU/tactic imputation.
trace=rows(Path('artifacts/engine-resource-profile-2026-10-25/retry-tail-full7808-20261029/attempt-envelopes.jsonl.gz'))
events=defaultdict(list)
for i,r in enumerate(trace):
 events[r['start']].append((True,i));events[r['end']].append((False,i))
profile={x['source_id']:x for x in read(Path('artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json'))}
active=set();previous=None;duration=Counter();exposure=Counter();segments=[];low_ids=set()
for stamp,changes in sorted(events.items()):
 if previous is not None and stamp>previous and 1<=len(active)<=2:
  elapsed=stamp-previous;duration[str(len(active))]+=elapsed
  ids=sorted(trace[i]['id']for i in active);low_ids.update(ids)
  segments.append(dict(start=previous,end=stamp,ids=ids))
  for sid in ids:exposure[sid]+=elapsed
 for add,i in changes:
  if add:active.add(i)
  else:active.remove(i)
 previous=stamp
assert not active
sample=Counter();covered=[];missing=[]
def family(key):
 key=key.lower().replace('_','')
 if 'intervalcases'in key:return 'interval_cases_constructor'
 if 'rcases'in key or 'tactic.cases'in key:return 'cases_or_rcases_boundary'
 if 'allgoals'in key or '<;>'in key:return 'goal_combinator_boundary'
 if 'simpall'in key:return 'simp_all'
 if 'simp'in key:return 'other_simp'
 return 'other_tactic_or_unattributed'
for sid in sorted(low_ids):
 p=profile.get(sid)
 if not p or not p.get('has_body_profile_data'):missing.append(sid);continue
 covered.append(sid)
 for x in p['sampled_CPU_weights']:
  if x['family']=='tactic':sample[family(x['key'])]+=x['nanoseconds']/1e9
tails=[x for x in trace if x['exclusive']]
tailids={x['id']for x in tails}
oldtail=Counter();tailprofile=[]
for sid in sorted(tailids):
 p=profile.get(sid)
 if p and p.get('has_body_profile_data'):
  tailprofile.append(sid)
  for x in p['sampled_CPU_weights']:
   if x['family']=='tactic':oldtail[family(x['key'])]+=x['nanoseconds']/1e9
result=dict(source='complete frozen13d4606native process envelopes + distinct historical480profile + original Syntax corpus',
 current_low_concurrency_wall_seconds=dict(duration),current_low_concurrency_unique_ids=len(low_ids),
 low_concurrency_IDs_with_historical_body_profile=len(covered),low_concurrency_IDs_without_historical_body_profile=len(missing),
 historical_conditioned_CPU_seconds=dict(sample),exclusive_tail_IDs=len(tailids),
 exclusive_tail_IDs_with_historical_body_profile=len(tailprofile),
 historical_exclusive_tail_CPU_seconds=dict(oldtail),
 measured_current_tail_independent_branch_wall_fraction=None,
 reason='Current process trace has no tactic phase/goal dependencies;historical CPU cannot be transferred onto its wall denominator. Constructor CPU is not branch execution CPU.',
 exact_state_cache=reused,analysis_seconds=time.monotonic()-start,
 scope='Offline opportunity only;no certified independence/state hit,parallelism implementation,gain or new native capture.')
(OUT/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
with gzip.open(OUT/'low-concurrency-segments.jsonl.gz','wt')as f:
 for x in segments:f.write(json.dumps(x)+'\n')
(OUT/'profile-coverage.json').write_text(json.dumps(dict(covered=covered,missing=missing,tail_profile=tailprofile,exposure_seconds=dict(exposure)),indent=2)+'\n')
print(json.dumps(result,indent=2))
