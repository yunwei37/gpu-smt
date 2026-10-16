from pathlib import Path
import zipfile,gzip,json,collections,datetime,importlib.util
D=Path(__file__).parent
split_spec=importlib.util.spec_from_file_location('split_stage','/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/server/split.py')
split=importlib.util.module_from_spec(split_spec);__import__('sys').modules[split_spec.name]=split;split_spec.loader.exec_module(split)
analysis_spec=importlib.util.spec_from_file_location('analysis_stage',D/'analyze.py')
analysis=importlib.util.module_from_spec(analysis_spec);analysis_spec.loader.exec_module(analysis)
selected=[json.loads(x) for x in (D/'stage-probe-input.jsonl').read_text().splitlines()]
bybody={split.split_snippet(x['code']).body:x['proof_id'] for x in selected}
results={}
for dirname,label in [('stage-probe1','profile-original'),('stage-probe2','profile-compiled')]:
 base=D/dirname;p=base/(label+'.terminal.json')
 if not p.exists():continue
 terminal=json.loads(p.read_text())
 if terminal['failure'] or terminal['returned']!=len(selected):continue
 with zipfile.ZipFile(base/(label+'.zip')) as z:
  rows=[json.loads(x) for x in z.read(label+'/results.jsonl').splitlines()]
  parsed={}
  for name in z.namelist():
   if '/native-profiles/' not in name or not name.endswith('.json.gz'):continue
   profile=json.loads(gzip.decompress(z.read(name)))
   main=next((t for t in profile['threads'] if t.get('isMainThread')),None)
   id=bybody.get(main['name']) if main else None
   if id is None:continue
   cost=collections.Counter()
   for thread in profile['threads']:
    for stack,weight in zip(thread['samples']['stack'],thread['samples']['weight']):
     frame=thread['stackTable']['frame'][stack];fn=thread['frameTable']['func'][frame]
     string=thread['stringArray'][thread['funcTable']['name'][fn]]
     cost[string]+=weight
   groups={}
   for stage,key in [('oracle','Invoking oracle'),('final_expression','Building final expression'),('linear_forms','linearFormsAndMaxVar'),('kernel','Kernel:')]:
    groups[stage]=sum(value for cls,value in cost.items() if key in cls)
   parsed[id]={'stages_leaf_wall_ms':groups,'profile_file':name}
  for row in rows:
   id=row['proof_id'];body=json.loads(z.read(label+'/'+row['raw_response']))
   parsed.setdefault(id,{})
   parsed[id].update(basic=row['basic'],request_seconds=row['elapsed_seconds'],native_payload=analysis.native(body,row['status_code']))
 results[label]={'whole_diagnostic_seconds':terminal['whole_seconds'],'per_source':parsed}
differences=[]
if len(results)==2:
 a=results['profile-original']['per_source'];b=results['profile-compiled']['per_source']
 for id in a:
  if a[id]['native_payload']!=b[id]['native_payload']:differences.append(id)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_sources':[x['proof_id'] for x in selected],'methods':results,'native_payload_difference_ids':differences,'scope':'Median/max priorpartialGCtrace-cost files plus realerror; intentionally selected3source diagnostic, not representative/replicated wholecorpus speedup. CPU4-7/width4/8004 and PPprofiling match, alternate-order repetitions absent. Oracle/kernel values are officialtrace leafwall, not CPU; allraw/native timing retained. Nativepayload comparison excludes only adapterduration.'}
(D/'stage-probe-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'completed_methods':list(results),'native_diff_ids':differences,'per_source':{method:{id:{k:v for k,v in data.items() if k!='native_payload'} for id,data in result['per_source'].items()} for method,result in results.items()}},indent=2))
