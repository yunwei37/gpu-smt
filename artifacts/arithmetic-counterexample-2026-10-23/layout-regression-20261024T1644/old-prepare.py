"""Parse original Lean commands and wrap real arithmetic syntax, not comments."""
from pathlib import Path
import gzip,json,os,subprocess
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def prepare(items,out):
 build=json.loads((A/'build.json').read_text());sdk=Path(build['sdk']);B=Path(build['build'])
 env=dict(os.environ);env['PATH']=str(sdk/'bin')+':'+env['PATH'];env['LEAN_PATH']=build['lean_path']
 requests=[];mapped={}
 for row in items:
  code=row['code'];head=row['header']
  if code.startswith(head)and head:
   mapped[row['index']]=(head,code[len(head):])
   requests.append(json.dumps(dict(id=row['index'],body=code[len(head):])))
 x=subprocess.run([str(sdk/'bin/lean'),'--run','Prepare.lean'],cwd=B,env=env,input='\n'.join(requests)+'\n',text=True,capture_output=True)
 (out/'parser.stderr').write_text(x.stderr)
 (out/'parser-stdout.jsonl').write_text(x.stdout)
 if x.returncode:raise RuntimeError('Own native parser failed: '+x.stderr[-1000:])
 parsed={}
 for line in x.stdout.splitlines():
  q=json.loads(line)
  if 'id'in q:parsed[q['id']]=q
 snippets=[];records=[]
 for row in items:
  source='minif2f-'+str(row['index']);code=row['code'];head=row['header'];q=parsed.get(row['index'])
  n=0;reason=None
  if q and not q.get('error'):
   raw=mapped[row['index']][1].encode()
   spans=sorted(q['positions'],key=lambda a:a['start'],reverse=True)
   for p in spans:
    text=raw[p['start']:p['end']]
    assert text.decode().lstrip().startswith(p['tactic'])
    raw=raw[:p['start']]+b'(cex_guard '+json.dumps(source).encode()+b' ('+text+b'))'+raw[p['end']:]
    n+=1
   code=head+raw.decode()
   code=code.replace('import Mathlib\n','import Mathlib\nimport Counterexample\n',1)
  else:reason=q.get('error')if q else'no parseable original header'
  snippets.append(dict(proof_id=source,code=code))
  records.append(dict(proof_id=source,wrapped_tactics=n,reason=reason))
 (out/'prepared.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in snippets))
 (out/'preparation.json').write_text(json.dumps(dict(sources=len(items),wrapped_sources=sum(x['wrapped_tactics']>0 for x in records),wrapped_tactics=sum(x['wrapped_tactics']for x in records),records=records),indent=2)+'\n')
 return snippets
