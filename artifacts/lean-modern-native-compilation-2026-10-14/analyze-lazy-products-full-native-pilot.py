from pathlib import Path
import json,zipfile,copy,statistics,datetime
D=Path(__file__).parent;B=D/'lazy-products-full-native-pilot1'
methods=['eager','lazy','fast'];cells={}
def clean(value):
 v=copy.deepcopy(value)
 for x in v.get('results',[]):
  if isinstance(x.get('response'),dict):x['response'].pop('time',None)
 return v
for rep in range(3):
 for method in methods:
  label=f'rep{rep}-{method}';tp=B/(label+'.terminal.json');zp=B/(label+'.zip')
  if not tp.exists() or not zp.exists():continue
  t=json.loads(tp.read_text())
  if t['failure'] or t['returned']!=5:continue
  with zipfile.ZipFile(zp) as z:
   rows=[json.loads(s) for s in z.read(label+'/results.jsonl').decode().splitlines()]
   source=z.read(label+'/input.jsonl')
   native={x['source_index']:clean(json.loads(z.read(label+'/'+x['raw_response']))) for x in rows}
  cells[(rep,method)]={'terminal':t,'source':source,'native':native,'basic':{x['source_index']:x['basic'] for x in rows}}
pairs=[]
for rep in range(3):
 for reference in ['eager','fast']:
  if (rep,reference) not in cells or (rep,'lazy') not in cells:continue
  a,b=cells[(rep,reference)],cells[(rep,'lazy')]
  pairs.append({'rep':rep,'reference':reference,'reference_seconds':a['terminal']['whole_seconds'],
   'lazy_seconds':b['terminal']['whole_seconds'],
   'wall_reduction_percent':100*(1-b['terminal']['whole_seconds']/a['terminal']['whole_seconds']),
   'source_bytes_equal':a['source']==b['source'],
   'basic_difference_indices':[i for i,x in a['basic'].items() if x!=b['basic'].get(i)],
   'native_payload_difference_indices':[i for i,x in a['native'].items() if x!=b['native'].get(i)]})
summaries={}
for reference in ['eager','fast']:
 values=[x['wall_reduction_percent'] for x in pairs if x['reference']==reference]
 summaries[reference]={'completed_pairs':len(values),'mean_reduction_percent':statistics.mean(values) if values else None,
  'observed_range_percent':[min(values),max(values)] if values else None}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'complete_cells':len(cells),'planned_cells':9,
 'pairs':pairs,'summaries':summaries,'cells':{f'{r}-{m}':v['terminal'] for (r,m),v in cells.items()},
 'scope':'five selected original public sources, three rotated whole-server trios, observeroff, identicalfullnative+HiGHS; sourcevariation/sharedbackground/startup included. No allpopulation gain or confidenceinterval.'}
(D/'lazy-products-full-native-pilot1-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['utc','complete_cells','planned_cells','summaries']}))
