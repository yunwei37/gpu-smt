"""Lossless closed-run publication; split compressed byte streams for Git."""
from pathlib import Path
import argparse,json,gzip,shutil,resource,os,datetime
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
os.sched_setaffinity(0,{12,13,14,15});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
assert json.loads((a.source/'terminal.json').read_text())['state']=='complete'
assert not a.out.exists(),'Do not overwrite retained archives'
a.out.mkdir(parents=True);manifest=[];chunk=32*1024**2
for src in a.source.rglob('*'):
 if not src.is_file():continue
 dst=a.out/src.relative_to(a.source);dst.parent.mkdir(parents=True,exist_ok=True)
 if src.suffix in ['.jsonl','.phases']and src.name not in ['candidate-times.jsonl','lp-races.jsonl','omega-calls.jsonl']:
  dst=dst.with_name(dst.name+'.gz')
  with src.open('rb')as inp,gzip.open(dst,'wb',compresslevel=1)as out:shutil.copyfileobj(inp,out,1024*1024)
 else:shutil.copy2(src,dst)
 if dst.stat().st_size>chunk:
  assert dst.name.endswith('.gz')
  nbytes=dst.stat().st_size;parts=[]
  with dst.open('rb')as f:
   n=0
   while data:=f.read(chunk):
    part=dst.with_name(dst.name+'.part'+str(n).zfill(5));part.write_bytes(data);parts.append(str(part.relative_to(a.out)));n+=1
  assert sum((a.out/p).stat().st_size for p in parts)==nbytes
  dst.unlink();manifest.append({'source_relative':str(src.relative_to(a.source)),'published_name':str(dst.relative_to(a.out)),'compressed_bytes':nbytes,'parts':parts,'encoding':'Concatenate parts in listed numeric order, then gzip-decompress once. Raw source bytes preserved; no JSON normalization.'})
(a.out/'archive-manifest.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(a.source),'split_compressed_streams':manifest},indent=2)+'\n')
print(json.dumps({'out':str(a.out),'files':sum(p.is_file()for p in a.out.rglob('*')),'bytes':sum(p.stat().st_size for p in a.out.rglob('*')if p.is_file()),'split_streams':len(manifest)}),flush=True)
