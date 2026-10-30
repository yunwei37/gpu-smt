"""Offline resource-tail opportunity audit; no native invocation or replay claim."""
import argparse, collections, gzip, json, pathlib, re, runpy, time
ROOT=pathlib.Path(__file__).resolve().parents[2]
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
ENVELOPES=ROOT/'artifacts/engine-resource-profile-2026-10-25/retry-tail-full7808-20261029/attempt-envelopes.jsonl.gz'
STRIP=runpy.run_path(str(ROOT/'bench/lean-candidate-scheduling/analyze.py'))['strip_comments']
def read(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def audit():
 inputs=read(PAIR/'input7808.json.gz')['candidates']
 run=read(PAIR/'engine.stdout.gz')
 by={x['id']:x for x in inputs}
 rows={x['id']:x for x in run['results']}
 with gzip.open(ENVELOPES,'rt') as f:envelopes=[json.loads(l) for l in f]
 solo=sorted((x for x in envelopes if x['exclusive']),key=lambda x:x['start'])
 failed=[x for x in solo if x['status']=='resource_exhausted']
 assert len(inputs)==len(rows)==7808 and len(solo)==42 and len(failed)==41
 # Source projections are opportunity proxies. They do not reconstruct a Lean state.
 projections={}
 descriptions={
  'byte_exact_source':'Complete original source bytes; still not a complete session state.',
  'comment_stripped_source':'Existing lexical stripper; diagnostic coordinates and trivia removed/changed.',
  'whitespace_collapsed_proxy':'Whitespace-collapse proxy only; not syntax or semantic canonicalization.',
  'task_last_line_proxy':'Task identity plus last source line only; all earlier proof/context effects ignored.',
  'task_only_proxy':'Same mathematical problem, not the same elaborated goal or local context.',
 }
 all_keys={}
 for c in inputs:
  text=STRIP(c['code'])
  lines=[l.strip() for l in text.splitlines() if l.strip()]
  all_keys[c['id']]={
   'byte_exact_source':c['code'],
   'comment_stripped_source':text,
   'whitespace_collapsed_proxy':' '.join(text.split()),
   'task_last_line_proxy':(c['task_id'],lines[-1] if lines else ''),
   'task_only_proxy':c['task_id'],
  }
 for name,description in descriptions.items():
  groups=collections.defaultdict(list)
  for e in failed:groups[all_keys[e['id']][name]].append(e)
  repeated=[g for g in groups.values() if len(g)>1]
  elidable=[e for g in repeated for e in g[1:]]
  projections[name]={
   'description':description,'unique_failed_groups':len(groups),
   'repeated_groups':len(repeated),'later_failed_candidates':len(elidable),
   'conditional_whole_candidate_envelope_seconds':sum(e['end']-e['start'] for e in elidable),
   'scope':'If every later whole candidate could be elided after the first producer at zero cost. Not tactic-stage time, qualified savings or a strict global acceleration bound.',
   'groups':[{'key':key,'ids':[e['id'] for e in g],
      'envelope_seconds':sum(e['end']-e['start'] for e in g),
      'later_candidate_envelope_seconds':sum(e['end']-e['start'] for e in g[1:])}
      for key,g in groups.items()],
  }
 per_source=[]
 for e in failed:
  c=by[e['id']];row=rows[e['id']]
  text=STRIP(c['code'])
  attempts=row['attempts']
  per_source.append({
   'id':c['id'],'task_id':c['task_id'],'last_source_line':all_keys[c['id']]['task_last_line_proxy'][1],
   'source_call_token_counts':dict(collections.Counter(re.findall(r'\b(?:rfl|decide|simp_all|norm_num|nlinarith|linarith|interval_cases)\b',text))),
   'solo_registered_envelope_seconds':e['end']-e['start'],
   'solo_reported_attempt_seconds':e['reported_attempt_seconds'],
   'status':row['outcome']['status'],'error':row['outcome']['error'],
   'attempt_statuses':[a['status'] for a in attempts],
   'observed_failed_entry_goal_context_and_scope':None,
   'deterministic_native_instruction_or_heartbeat_exhaustion_record':None,
  })
 return {
  'source':'Frozen full7808 engine13d4606; no cross-run clocks',
  'sources':7808,'final_resource_failures':41,'exclusive_attempts':42,
  'exclusive_statuses':dict(collections.Counter(e['status'] for e in solo)),
  'failed_tasks':dict(collections.Counter(by[e['id']]['task_id'] for e in failed)),
  'engine_internal_wall_seconds':run['lifecycle_seconds'],
  'all_exclusive_registered_envelope_seconds':sum(e['end']-e['start'] for e in solo),
  'resource_failed_registered_envelope_seconds':sum(e['end']-e['start'] for e in failed),
  'failed_entry_complete_state_coverage':{'observed':0,'missing':41,'exact_goal_call_match_rate':None},
  'operational_failure_producers_qualified_for_budget_monotone_rejection':0,
  'projections':projections,'per_source':per_source,
  'semantics':'RSS watchdog outcomes depend on allocation/GC/shared pages/prepared parent/peer footprint and 1s sampling. No deterministic <=B monotonicity theorem follows. Even matching tactic input requires replay effects, diagnostics, original budget and control flow; source-level resource failure is not logical rejection.',
  'native_invocations':0,
 }
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();d=audit();d['analysis_seconds']=time.monotonic()-start
 (a.out/'result.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in d.items() if k not in ['per_source','projections']},ensure_ascii=False))
 print(json.dumps({k:{f:v[f] for f in ['unique_failed_groups','later_failed_candidates','conditional_whole_candidate_envelope_seconds']} for k,v in d['projections'].items()},ensure_ascii=False))
if __name__=='__main__':main()
