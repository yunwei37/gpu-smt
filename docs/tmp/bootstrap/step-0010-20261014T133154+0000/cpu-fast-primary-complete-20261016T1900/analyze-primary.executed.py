from pathlib import Path
import json,zipfile,collections,datetime
D=Path('/workspaces/repository/artifacts/lean-modern-native-compilation-2026-10-14');B=D/'farkas-fast427-full1'
methods=['full-hybrid','fast-hybrid','full-highs','fast-highs']
def clean(v):
 v=json.loads(json.dumps(v))
 for frame in v.get('results',[]):
  if isinstance(frame.get('response'),dict):frame['response'].pop('time',None)
 return v
def cell(label):
 p=B/(label+'.terminal.json')
 if not p.exists():return {'status':'not terminal'}
 t=json.loads(p.read_text());path=B/(label+'.zip')
 if t['failure'] or t['returned']!=29750 or not path.exists():return {'status':'failed or partial','terminal':t}
 with zipfile.ZipFile(path) as z:
  rows=[json.loads(x) for x in z.read(label+'/results.jsonl').splitlines()]
  inputs=[json.loads(x) for x in z.read(label+'/input.jsonl').splitlines()]
  assert z.read(label+'/input.jsonl')==(D/'input.jsonl').read_bytes()
  assert len(rows)==len(inputs)==29750
  assert sorted((x['ordinal'],x['source_index'])for x in rows)==[(i,x['index'])for i,x in enumerate(inputs)]
  command=json.loads(z.read(label+'/command.json'))
  payload={x['source_index']:json.loads(z.read(label+'/'+x['raw_response'])) for x in rows}
  values=sorted(x['elapsed_seconds'] for x in rows)
  summary={'whole_seconds':t['whole_seconds'],'attempts_per_second':t['returned']/t['whole_seconds'],
   'counts':dict(collections.Counter(x['basic'] for x in rows)),
   'median_request_seconds':values[round((len(values)-1)*.5)],'p95_request_seconds':values[round((len(values)-1)*.95)],'p99_request_seconds':values[round((len(values)-1)*.99)]}
  return {'status':'complete acquisition; review pending','terminal':t,'summary':summary,'inputs':inputs,'rows':rows,'payload':payload,'command':command}
cells={(rep,m):cell(f'goedel427-rep{rep}-{m}') for rep in range(3) for m in methods};pairs=[]
for rep in range(3):
 for solver in ['hybrid','highs']:
  a=cells[(rep,'full-'+solver)];b=cells[(rep,'fast-'+solver)]
  if 'summary' not in a or 'summary' not in b:continue
  assert a['inputs']==b['inputs']
  assert len(a['rows'])==len(b['rows'])==29750
  basic={r['source_index']:r['basic'] for r in a['rows']}
  pairs.append({'rep':rep,'solver':solver,'whole_change_percent':100*(b['summary']['whole_seconds']/a['summary']['whole_seconds']-1),
   'basic_difference_ids':[x['source_index'] for x in b['rows'] if basic[x['source_index']]!=x['basic']],
   'native_payload_differences_excluding_only_backward_response_time':[i for i in a['payload'] if clean(a['payload'][i])!=clean(b['payload'].get(i,{}))]})
oracle_pairs=[]
for rep in range(3):
 for preprocessing in ['full','fast']:
  a=cells[(rep,preprocessing+'-hybrid')];b=cells[(rep,preprocessing+'-highs')]
  if 'summary' not in a or 'summary' not in b:continue
  assert a['inputs']==b['inputs']
  for key in ['command','cwd','backend','affinity','stock_defaults','api']:
   assert a['command'][key]==b['command'][key],key
  basics={x['source_index']:x['basic']for x in a['rows']}
  changes=[{'source_index':x['source_index'],'reference':basics[x['source_index']],'candidate':x['basic']}
   for x in b['rows']if basics[x['source_index']]!=x['basic']]
  differences=[i for i in a['payload']if clean(a['payload'][i])!=clean(b['payload'].get(i,{}))]
  oracle_pairs.append({'rep':rep,'preprocessing':preprocessing,'reference':'hybrid','candidate':'highs',
   'reference_whole_seconds':a['summary']['whole_seconds'],'candidate_whole_seconds':b['summary']['whole_seconds'],
   'whole_change_percent':100*(b['summary']['whole_seconds']/a['summary']['whole_seconds']-1),
   'reference_command':a['command'],'candidate_command':b['command'],'basic_differences':changes,
   'native_payload_differences_excluding_only_backward_response_time':differences,
   'scope':'Supporting same-block CPU oracle comparison; full four-method repetitions/resources remain required.'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cells':{f'{rep}-{m}':{k:v for k,v in x.items() if k in ['status','terminal','summary']} for (rep,m),x in cells.items()},
 'complete_matched_primary_pairs':pairs,'complete_matched_oracle_comparisons':oracle_pairs,'scope':'All12primary conditions are complete; four separate resource profiles and full16condition acquisition remain incomplete. All original outcomes and native differences remain; no global CPU ranking, new-system novelty, GPU gain or resource superiority is inferred.'}
(Path("/workspaces/repository/docs/tmp/bootstrap/step-0010-20261014T133154+0000/cpu-fast-primary-complete-20261016T1900")/'primary-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'complete_primary_cells':sum('summary'in x for x in cells.values()),'complete_primary_pairs':len(pairs),'planned_total_conditions':16,'status':'incomplete' if len(pairs)<6 else 'primary complete; profiles/review still needed'}))
