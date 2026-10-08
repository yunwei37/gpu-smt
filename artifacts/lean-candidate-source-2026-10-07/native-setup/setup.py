import urllib.request,json,hashlib,tarfile,zipfile,datetime,os
from pathlib import Path
b=Path(__file__).parent
meta=[]
def fetch(u,name):
 p=b/'downloads'/name
 if not p.exists():
  print('DOWNLOAD',u,flush=True)
  with urllib.request.urlopen(u) as r,p.open('wb') as f:
   while True:
    c=r.read(1024*1024)
    if not c:break
    f.write(c)
 h=hashlib.sha256(p.read_bytes()).hexdigest();meta.append(dict(url=u,path=str(p),sha256=h,bytes=p.stat().st_size));(b/'download-metadata.json').write_text(json.dumps(meta,indent=2));return p
p=fetch('https://github.com/leanprover/lean4/releases/download/v4.9.0-rc1/lean-4.9.0-rc1-linux.zip','lean-4.9.0-rc1-linux.zip')
if not (b/'lean-4.9.0-rc1-linux/bin/lean').exists():
 with zipfile.ZipFile(p) as z:z.extractall(b)
 for p in (b/'lean-4.9.0-rc1-linux/bin').iterdir():p.chmod(p.stat().st_mode|0o111)
def archive(repo,rev,target):
 p=fetch('https://codeload.github.com/'+repo+'/tar.gz/'+rev,repo.replace('/','-')+'-'+rev+'.tar.gz')
 target.mkdir(parents=True,exist_ok=True)
 if not any(target.iterdir()):
  with tarfile.open(p) as t:
   for m in t.getmembers():
    m.name='/'.join(m.name.split('/')[1:])
    if m.name:t.extract(m,target,filter='data')
archive('xinhjBrant/mathlib4','2f65ba7f1a9144b20c8e7358513548e317d26de1',b/'mathlib4')
d=json.loads((b/'mathlib4/lake-manifest.json').read_text())
for p in d['packages']:
 repo=p['url'].removeprefix('https://github.com/').removesuffix('.git');archive(repo,p['rev'],b/'mathlib4/.lake/packages'/p['name'])
print('ARCHIVES READY',flush=True)
