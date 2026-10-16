from pathlib import Path
import json,zipfile,collections,statistics,datetime
D=Path(__file__).parent;B=D/'highs-native-cpu-full1'
methods=['tiered','hybrid','highs'];data={}
def clean(v):
 # server.routers.backward extends only results[*].response with measured time.
 # Retain every other field, including nested time fields if ever present.
 copy=json.loads(json.dumps(v))
 if isinstance(copy,dict):
  for frame in copy.get('results',[]):
   if isinstance(frame,dict) and isinstance(frame.get('response'),dict):
    frame['response'].pop('time',None)
 return copy
def read(label):
 terminal=B/(label+'.terminal.json')
 if not terminal.exists():return None
 t=json.loads(terminal.read_text());path=B/(label+'.zip')
 if t['failure'] or t['returned']!=t['expected'] or not path.exists():return {'terminal':t,'status':'partial or failed; no comparison'}
 with zipfile.ZipFile(path) as z:
  rows=[json.loads(x) for x in z.read(label+'/results.jsonl').decode().splitlines()]
  inputs=[json.loads(x) for x in z.read(label+'/input.jsonl').decode().splitlines()]
  payload={x['source_index']:json.loads(z.read(label+'/'+x['raw_response'])) for x in rows}
  elapsed=sorted(x['elapsed_seconds'] for x in rows)
  def quantile(p):return elapsed[round((len(elapsed)-1)*p)]
  return {'terminal':t,'status':'complete acquisition; result review pending','source_inputs':inputs,'rows':rows,'payload':payload,
   'summary':{'whole_seconds':t['whole_seconds'],'throughput':t['returned']/t['whole_seconds'],'counts':dict(collections.Counter(x['basic'] for x in rows)),
     'median_request_s':quantile(.5),'p95_request_s':quantile(.95),'p99_request_s':quantile(.99)}}
for rep in range(3):
 for m in methods:data[(rep,m)]=read(f'goedel427-rep{rep}-{m}')
observations=[]
for rep in range(3):
 trio=[data[(rep,m)] for m in methods]
 if not all(x and 'summary' in x for x in trio):continue
 base=trio[0]
 for method,candidate in zip(methods[1:],trio[1:]):
  assert base['source_inputs']==candidate['source_inputs']
  assert len(base['rows'])==len(candidate['rows'])==29750
  fields=[i for i in base['payload'] if clean(base['payload'][i])!=clean(candidate['payload'].get(i))]
  basic={x['source_index']:x['basic'] for x in base['rows']}
  outcomes=[x['source_index'] for x in candidate['rows'] if basic[x['source_index']]!=x['basic']]
  observations.append({'rep':rep,'method':method,'whole_change_percent':100*(candidate['summary']['whole_seconds']/base['summary']['whole_seconds']-1),
   'native_payload_differences_excluding_adapter_time':fields,'basic_differences':outcomes,'qualification':'native/artifact differences must be reviewed before superiority; exact certificate search may produce different proof-internal IDs but is not arbitrary backend transparency'})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'complete acquisitions only; three method twelve-condition matrix must finish, independent result review not completed',
 'cells':{f'{rep}-{m}':{k:v for k,v in value.items() if k in ['terminal','status','summary']} if value else {'status':'not terminal'} for (rep,m),value in data.items()},
 'complete_primary_trio_comparisons':observations}
(D/'highs-native-cpu-complete-cells-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'complete_cells':sum(bool(v and 'summary' in v) for v in data.values()),'complete_primary_trios':len(observations)//2,'matrix_status':'incomplete' if len(observations)<6 else 'primary complete; profiles/review still required'}))
