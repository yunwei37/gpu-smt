import pathlib,json,inspect
from kimina_client import ReplResponse
n=pathlib.Path('/workspaces/repository/docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-command-protocol')
v=json.loads((n/'before/private/responses.json').read_text())
result=[]
for row in v:
 before=ReplResponse(id=row['proof_id'],response=row['response']).analyze().model_dump(mode='json')
 inner=ReplResponse(id=row['proof_id'],response=row['response']['response']).analyze().model_dump(mode='json')
 result.append({'proof_id':row['proof_id'],'official_client_outer':before,'official_client_nested_native':inner})
(n/'before-client-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
