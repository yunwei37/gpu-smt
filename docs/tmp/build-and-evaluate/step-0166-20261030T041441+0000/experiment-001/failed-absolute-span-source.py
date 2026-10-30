"""Cross-proof native-Syntax call opportunities; source/state proxies stay distinct."""
import argparse,collections,gzip,json,pathlib,re,runpy
ROOT=pathlib.Path(__file__).resolve().parents[2]
PAIR=ROOT/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
STRIP=runpy.run_path(str(ROOT/'bench/lean-candidate-scheduling/analyze.py'))['strip_comments']
def read(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 inputs={x['id']:x for x in read(PAIR/'input7808.json.gz')['candidates']}
 results=read(PAIR/'engine.stdout.gz')['results']
 failed={x['id'] for x in results if x['outcome']['status']=='resource_exhausted'}
 assert len(failed)==41
 with gzip.open(ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/native-units.jsonl.gz','rt') as f:
  syntax={x['proposalId']:x for line in f if (x:=json.loads(line))['proposalId'] in failed}
 assert set(syntax)==failed and all(x['eligible'] for x in syntax.values())
 profile={x['source_id']:x for x in json.loads((ROOT/'artifacts/lean-failure-profile-2026-10-25/full480-analysis/per-source.json').read_text())}
 envelopes={}
 with gzip.open(ROOT/'artifacts/engine-resource-profile-2026-10-25/retry-tail-full7808-20261029/attempt-envelopes.jsonl.gz','rt') as f:
  for line in f:
   x=json.loads(line)
   if x['exclusive'] and x['id'] in failed:envelopes[x['id']]=x
 assert set(envelopes)==failed
 callgroups=collections.defaultdict(list);prefixgroups=collections.defaultdict(list);targetgroups=collections.defaultdict(list);rows=[]
 for sid in sorted(failed,key=lambda s:envelopes[s]['start']):
  c=inputs[sid];units=syntax[sid]['units'];proofpath=[];calls=[]
  for ordinal,u in enumerate(units):
   assert c['code'].encode()[u['startByte']:u['stopByte']].decode()==u['text'],('native byte mapping',sid,ordinal)
   text=STRIP(u['text']).strip();proofpath.append((u['syntaxKind'],text))
   if u['syntaxKind'].endswith(('.tacticRfl','.normNum','.simpAll')) or u['syntaxKind']=='nlinarith' or 'intervalCases' in u['syntaxKind']:
    key=(c['task_id'],u['syntaxKind'],text)
    callgroups[key].append((sid,ordinal))
    prefixgroups[(c['task_id'],tuple(proofpath))].append((sid,ordinal))
    calls.append({'ordinal':ordinal,'kind':u['syntaxKind'],'text':text,'start_byte':u['startByte'],'stop_byte':u['stopByte']})
  # Declared narrow source template:have : S=E := by ...;rw [that];rfl.
  # Recover the explicit computation expression,not an elaborated state or proof.
  recovered=None;reason='outside the declared three-unit template'
  if len(units)==3 and units[0]['syntaxKind'].endswith('.tacticHave_') and units[1]['syntaxKind'].endswith('.rwSeq') and units[2]['syntaxKind'].endswith('.tacticRfl'):
   h=STRIP(units[0]['text'])
   match=re.fullmatch(r'\s*have(?:\s+([^\s:]+))?\s*:\s*S\s*=\s*(.*?)\s*:=\s*by\b.*',h,re.S)
   name=(match.group(1) or 'this') if match else None
   rewrite=STRIP(units[1]['text']).strip()
   if match and rewrite==f'rw [{name}]':
    rhs=' '.join(match.group(2).split())
    # Exact source tokens only:no alpha,notation,definitional or semantic canonicalization.
    recovered={'explicit_set_expression':rhs,'rewritten_goal_template':f'({rhs}).card = 100',
      'rewrite_lemma_name':name,'tactic':'rfl','budget_bytes':48*1024**3}
    if c['task_id']=='amc12a_2020_p4':
     header=re.split(r':=\s*by\b',STRIP(c['code']),maxsplit=1)[0]
     assert re.search(r':\s*S\.card\s*=\s*100\s*$',header),('goal template',sid)
     targetgroups[(c['task_id'],rhs,'rfl',48*1024**3)].append(sid);reason='template match;source-level target only'
    else:recovered=None;reason='cardinality goal only certified as this source-template shape for amc12a_2020_p4'
  old=profile.get(sid,{})
  rflcpu=sum(w['nanoseconds']/1e9 for w in old.get('sampled_CPU_weights',[]) if w.get('family')=='tactic' and any(k in w.get('key','').lower() for k in ['eqrefl','rfl']))
  rows.append({'id':sid,'task':c['task_id'],'native_units':units,'expensive_standalone_syntax_calls':calls,'source_target_template':recovered,'template_status':reason,
    'historical_rfl_sampled_CPU_seconds':rflcpu,'current_exclusive_envelope_seconds':envelopes[sid]['end']-envelopes[sid]['start'],
    'complete_native_target_context_hidden_state':None})
 def cross(groups):
  selected=[]
  for key,items in groups.items():
   seen=set();ordered=[]
   for item in items:
    sid=item[0] if isinstance(item,tuple) else item
    if sid not in seen:ordered.append(sid);seen.add(sid)
   if len(ordered)>1:
    selected.append({'key':key,'distinct_proofs':ordered,'later_proofs':ordered[1:],
     'conditional_later_whole_candidate_envelope_seconds':sum(envelopes[s]['end']-envelopes[s]['start'] for s in ordered[1:])})
  return selected
 data={'resource_sources':41,'native_syntax_coverage':41,'same_call_text_cross_proof_groups':cross(callgroups),
   'same_rooted_native_unit_text_cross_proof_groups':cross(prefixgroups),
   'source_rewritten_target_template_groups':cross(targetgroups),
   'template_matched_sources':sum(x['source_target_template'] is not None for x in rows),
   'qualified_native_full_state_hits':None,'native_invocations':0,'per_source':rows,
   'scope':'Different proofs may repeat calls even without identical source. Native Syntax supplies call kinds/spans but not runtime reachability or full entry states. Narrow rewritten-target templates exclude extra simp/other steps and are not elaborated goals/context matches. Whole-candidate envelopes are conditional opportunity,not time inside the matching call;historical CPU clocks stay separate.',
   'safety':'Same target/tactic/global RSS cap does not identify remaining allocator/GC/retained-heap state. No cross-budget failure certificate or native rejection is derived.'}
 (a.out/'result.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in data.items() if k not in ['per_source','scope','safety']},ensure_ascii=False))
 for g in data['source_rewritten_target_template_groups']:print(json.dumps(g,ensure_ascii=False))
if __name__=='__main__':main()
