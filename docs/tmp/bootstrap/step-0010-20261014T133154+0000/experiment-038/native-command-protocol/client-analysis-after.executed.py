import pathlib,json
from kimina_client import ReplResponse
n=pathlib.Path('/workspaces/repository/docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-command-protocol')
a=json.loads((n/'after/terminal.json').read_text())
out=[]
stock={row['proof_id']:row['response'] for row in a['methods']['plain']['rows']}
for method,t in a['methods'].items():
 assert t['state']=='complete' and t['normal_eof'] and t['exit_code']==0
 for row in t['rows']:
  assert row['response']==stock[row['proof_id']]
  status=ReplResponse(id=row['proof_id'],response=row['response']).analyze().model_dump(mode='json')
  out.append({'method':method,'proof_id':row['proof_id'],'exact_same_native_value_as_plain':True,'official_client_analysis':status})
assert [x['official_client_analysis']['status'] for x in out]==['valid','lean_error','valid','lean_error']
(n/'after-client-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
