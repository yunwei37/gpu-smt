from pathlib import Path
import json,gzip
r=Path(__file__).parent
read=lambda p:json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
source=gzip.decompress((r/'native/Input.lean.gz').read_bytes()).decode()
summary={}
for n in ['preflight-native','preflight-core','native','import-only','core','public']:
 t=read(r/n/'terminal.json');v=read(r/n/'results.jsonl.gz')['results'][0];ar=read(r/n/'archival.json')
 assert v['outcome']['status']=='accepted' and len(v['attempts'])==1 and not v['cached'] and not v['coalesced']
 summary[n]={'whole':t['cell_seconds'],'with_archive':t['cell_seconds']+ar['seconds'],'response':v['outcome']['response']}
for n in ['import-only','core','public']:
 s=gzip.decompress((r/n/'Input.lean.gz').read_bytes()).decode()
 s=s.replace('import SharedCNF\n','',1)
 if n=='core':s=s.replace('bv_decide_shared_core','bv_decide')
 if n=='public':s=s.replace('bv_decide_shared','bv_decide')
 assert s==source
assert all(v['response']==summary['native']['response'] for v in summary.values())
print(json.dumps({'cells':summary,'core_over_native':summary['core']['whole']/summary['native']['whole'],'public_over_native':summary['public']['whole']/summary['native']['whole']},indent=2))
