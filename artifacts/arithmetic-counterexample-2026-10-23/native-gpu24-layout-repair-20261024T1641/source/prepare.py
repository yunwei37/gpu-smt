"""Wrap actual arithmetic syntax while preserving Lean layout; reparse natively."""
from pathlib import Path
import gzip,json,os,subprocess
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def prepare(items,out):
 build=json.loads((A/'build.json').read_text());sdk=Path(build['sdk']);B=Path(build['build'])
 env=dict(os.environ);env['PATH']=str(sdk/'bin')+':'+env['PATH'];env['LEAN_PATH']=build['lean_path']
 def native_parse(requests,label):
  x=subprocess.run([str(sdk/'bin/lean'),'--run','Prepare.lean'],cwd=B,env=env,
   input='\n'.join(json.dumps(q)for q in requests)+'\n',text=True,capture_output=True)
  (out/(label+'.stderr')).write_text(x.stderr);(out/(label+'-stdout.jsonl')).write_text(x.stdout)
  if x.returncode:raise RuntimeError('Own native parser failed: '+x.stderr[-1000:])
  parsed={}
  for line in x.stdout.splitlines():
   q=json.loads(line)
   if 'id'in q:parsed[q['id']]=q
  return parsed
 requests=[];mapped={}
 for row in items:
  code=row['code'];head=row['header']
  if code.startswith(head)and head:
   mapped[row['index']]=(head,code[len(head):])
   requests.append(dict(id=row['index'],body=code[len(head):]))
 parsed=native_parse(requests,'parser')
 snippets=[];records=[];checks=[]
 for row in items:
  source='minif2f-'+str(row['index']);code=row['code'];head=row['header'];q=parsed.get(row['index'])
  n=0;reason=None;skipped=[]
  if q and not q.get('error'):
   raw=mapped[row['index']][1].encode()
   for span in sorted(q['positions'],key=lambda a:a['start'],reverse=True):
    text=raw[span['start']:span['end']]
    assert text.decode().lstrip().startswith(span['tactic'])
    if b'\n'in text and b'"'in text:
     skipped.append(dict(start=span['start'],end=span['end'],reason='multiline quoted text retained native'));continue
    prefix=b'(cex_guard '+json.dumps(source).encode()+b' ('
    shifted=text.replace(b'\n',b'\n'+b' '*len(prefix))
    raw=raw[:span['start']]+prefix+shifted+b'))'+raw[span['end']:]
    n+=1
   if n:
    body=raw.decode();checks.append(dict(id=row['index'],body=body))
    code=(head+body).replace('import Mathlib\n','import Mathlib\nimport Counterexample\n',1)
  else:reason=q.get('error')if q else'no parseable original header'
  snippets.append(dict(proof_id=source,code=code))
  records.append(dict(proof_id=source,wrapped_tactics=n,reason=reason,skipped_tactics=skipped))
 checked=native_parse(checks,'wrapper-parser')if checks else{}
 for row,snippet,record in zip(items,snippets,records):
  if not record['wrapped_tactics']:continue
  result=checked.get(row['index'])
  if result is None or result.get('error'):
   snippet['code']=row['code'];record['wrapped_tactics']=0
   record['reason']='wrapped native parser fallback: '+(result.get('error','unknown')if result else'no response')
 (out/'prepared.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n'for x in snippets))
 (out/'preparation.json').write_text(json.dumps(dict(sources=len(items),wrapped_sources=sum(x['wrapped_tactics']>0 for x in records),wrapped_tactics=sum(x['wrapped_tactics']for x in records),native_wrapper_reparse=True,records=records),indent=2)+'\n')
 return snippets
