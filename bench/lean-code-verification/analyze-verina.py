"""Read real native results and Lean4.18 Firefox tracing weights."""
from pathlib import Path
import argparse,collections,gzip,json,re
def rows(path):
 if path.exists():return [json.loads(x)for x in path.open()]
 with gzip.open(path.with_name(path.name+'.gz'),'rt')as f:return [json.loads(x)for x in f]
def label(thread,stack):
 st=thread['stackTable'];frame=st['frame'][stack]
 fn=thread['frameTable']['func'][frame]
 return thread['stringArray'][thread['funcTable']['name'][fn]]
def compact(text):
 pieces=text.split(': ',2)
 return ': '.join(pieces[:2])if text.startswith('Elab.step: ')else pieces[0]
def analyze(root):
 assert json.loads((root/'client-exit.json').read_text())['exit']==0
 native={r['source_id']:r for r in rows(root/'native/results.jsonl')}
 profiled={r['source_id']:r for r in rows(root/'profile/results.jsonl')}
 assert set(native)==set(profiled)
 groups={};traces=[];per=[]
 for sid,r in sorted(profiled.items()):
  whole=collections.Counter();tactic=collections.Counter();family=collections.Counter()
  trace=root/'profile/profiles'/(sid+'.json.gz')
  if trace.exists():
   data=json.loads(gzip.decompress(trace.read_bytes()))
   for thread in data['threads']:
    assert thread['samples']['weightType']=='tracing-ms'
    st=thread['stackTable'];samples=thread['samples']
    for i,ms in enumerate(samples['weight']):
     if ms==0:continue
     assert ms>=0
     stack=samples['stack'][i];whole[compact(label(thread,stack))]+=ms/1000
     while stack is not None:
      name=label(thread,stack)
      if name.startswith('Elab.step: ')and name.split(': ',2)[1].startswith(('Lean.Parser.Tactic.','Mathlib.Tactic.','tactic','Lean.cdot')):
       kind=name.split(': ',2)[1];tactic[kind]+=ms/1000
       lower=kind.lower()
       fam=next((f for f in ['bv_decide','omega','grind','decide','simp']if
        (f=='bv_decide'and('bvdecide'in lower or'bv_decide'in lower))or
        (f!='bv_decide'and lower.rsplit('.',1)[-1].startswith(f))), 'other tactic')
       family[fam]+=ms/1000;break
      stack=st['prefix'][stack]
     else:family['outside traced tactic']+=ms/1000
  group=r['status'];g=groups.setdefault(group,dict(sources=0,component=collections.Counter(),tactic=collections.Counter(),family=collections.Counter()))
  g['sources']+=1;g['component'].update(whole);g['tactic'].update(tactic);g['family'].update(family)
  per.append(dict(source_id=sid,native_status=native[sid]['status'],profile_status=r['status'],
   native_whole_file_seconds=native[sid]['whole_file_seconds'],profile_whole_file_seconds=r['whole_file_seconds'],
   trace_available=trace.exists(),trace_exclusive_weights_seconds=dict(whole),nearest_tactic_weights_seconds=dict(tactic),
   source_has_explicit_admission=r['source_has_explicit_admission']))
 summaries=json.loads((root/'summary.json').read_text())
 for s in summaries:
  assert s['state']=='complete'and not s['remaining_owned_descendants']and not s['memory_watchdog']['error']
  assert s['memory_watchdog']['peak_sampled_owned_rss_bytes']<=48*1024**3
 result=dict(sources=len(native),native_counts=dict(collections.Counter(x['status']for x in native.values())),
  profile_counts=dict(collections.Counter(x['status']for x in profiled.values())),
  status_changes=[dict(source_id=s,native=native[s]['status'],profile=profiled[s]['status'])for s in native if native[s]['status']!=profiled[s]['status']],
  lifecycles=summaries,groups={name:dict(sources=g['sources'],
   component_exclusive_trace_weights_seconds=g['component'].most_common(),
   nearest_tactic_trace_weights_seconds=g['tactic'].most_common(),
   family_trace_weights_seconds=g['family'].most_common())for name,g in groups.items()},
  scope='Unmodified official reference sources at pinned Lean4.18. Structured trace uses exclusive elapsed slices between children with default trace thresholds. threadCPUDelta is synthesized from wall slices by upstream exporter, never measured CPU. Weights sum across traces/threads/files, not whole-group elapsed or removable work. Admitted stubs separated.')
 (root/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 (root/'per-source-analysis.json').write_text(json.dumps(per,indent=2)+'\n')
 lines=['# Verina original-source native characterization — root self-review','',result['scope'],'',
  'Sources: '+str(len(native)),'Native counts: '+json.dumps(result['native_counts']),
  'Diagnostic counts: '+json.dumps(result['profile_counts']),
  'Status changes: '+json.dumps(result['status_changes']),'']
 for name,g in result['groups'].items():
  lines+=['## '+name+' ('+str(g['sources'])+' sources)','',
   '| Exclusive traced component | Accumulated wall-slice seconds |','|---|---:|']
  for kind,v in g['component_exclusive_trace_weights_seconds'][:12]:lines.append('|'+kind.replace('|','/')+'|'+f'{v:.6f}'+'|')
  lines+=['','| Nearest traced tactic family | Accumulated wall-slice seconds |','|---|---:|']
  for kind,v in g['family_trace_weights_seconds']:lines.append('|'+kind+'|'+f'{v:.6f}'+'|')
  lines.append('')
 lines+=['A missing tactic trace can be below the default threshold; absence is not zero cost.',
  'Native exit0 without an explicit admission token is deliberately narrower than a complete theorem-soundness certification.',
  'This is workload characterization, not a comparison with another prover system or a GPU result.','']
 (root/'analysis.md').write_text('\n'.join(lines))
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True);a=p.parse_args()
 r=analyze(a.run);print(json.dumps({k:r[k]for k in ['sources','native_counts','profile_counts','status_changes','groups']},indent=2))
