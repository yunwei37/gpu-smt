from pathlib import Path
import json,zipfile,collections,copy,datetime
D=Path(__file__).parent;B=D/'product-application-probe1'
labels=['full','full-products','fast','fast-products']
cells={}
def clean(raw):
 value=copy.deepcopy(raw)
 for frame in value.get('results',[]):
  if isinstance(frame,dict) and isinstance(frame.get('response'),dict):frame['response'].pop('time',None)
 return value
for label in labels:
 t=B/(label+'.terminal.json')
 if not t.exists():continue
 terminal=json.loads(t.read_text())
 if terminal['failure'] or terminal['returned']!=4:continue
 with zipfile.ZipFile(B/(label+'.zip')) as z:
  pre=label+'/'
  rows=[json.loads(x) for x in z.read(pre+'results.jsonl').decode().splitlines()]
  payload={x['source_index']:json.loads(z.read(pre+x['raw_response'])) for x in rows}
  inputs=[json.loads(x) for x in z.read(pre+'input.jsonl').decode().splitlines()]
  telemetry=[json.loads(x) for x in z.read(pre+'oracle.jsonl').decode().splitlines()] if pre+'oracle.jsonl' in z.namelist() else []
  products=[x for x in telemetry if x.get('ty')=='product-application']
  lp=collections.defaultdict(list)
  for x in telemetry:
   if 'lp' in x:lp[x.get('source')].append({k:x.get(k) for k in ['lp','cert','ok']})
 cells[label]={'terminal':terminal,'rows':rows,'payload':payload,'inputs':inputs,'lp':lp,'products':products,
  'engagement':{'observed_product_invocations':len(products),'reused':sum(x['reused'] for x in products),'built':sum(x['built'] for x in products),'all_rows':products}}
comparisons=[]
for a,b in [('full','full-products'),('fast','fast-products')]:
 if a not in cells or b not in cells:continue
 base,cand=cells[a],cells[b]
 outcomes={x['source_index']:x['basic'] for x in base['rows']}
 comparisons.append({'baseline':a,'candidate':b,'source_bytes_equal':base['inputs']==cand['inputs'],
  'basic_differences':[x['source_index'] for x in cand['rows'] if outcomes[x['source_index']]!=x['basic']],
  'native_payload_differences':[i for i,v in base['payload'].items() if clean(v)!=clean(cand['payload'].get(i,{}))],
  'native_oracle_inputs_certificates_equal':base['lp']==cand['lp'],
  'baseline_whole_s':base['terminal']['whole_seconds'],'candidate_whole_s':cand['terminal']['whole_seconds'],
  'timing_scope':'one ordered observer-enabled four-source control; no fair corpus or repeated whole performance conclusion'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed_control_cells':len(cells),'comparisons':comparisons,
 'cells':{label:{k:value[k] for k in ['terminal','engagement']} for label,value in cells.items()}}
(D/'product-application-probe1-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
