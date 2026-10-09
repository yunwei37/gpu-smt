from pathlib import Path
import urllib.request,json,hashlib,zipfile,tarfile,datetime,os
root=Path('/tmp/gpu-smt-lean421-native'); out=Path('/workspaces/repository/artifacts/leanpolish-native-2026-10-09/source-provenance'); meta=[]
def fetch(url,path,expected=None):
 print('fetch',url,flush=True)
 with urllib.request.urlopen(url,timeout=120) as r,path.open('xb') as f:
  while b:=r.read(1024*1024): f.write(b)
 h=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
 meta.append(dict(url=url,path=str(path),bytes=path.stat().st_size,sha256=h,timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()));(out/'acquisition.json').write_text(json.dumps(meta,indent=2))
 if expected: assert h==expected,(h,expected)
 return path
def extract(p,target):
 target.mkdir()
 with tarfile.open(p) as t:
  for m in t.getmembers():
   m.name='/'.join(m.name.split('/')[1:])
   if m.name:t.extract(m,target,filter='data')
p=fetch('https://github.com/leanprover/lean4/releases/download/v4.21.0/lean-4.21.0-linux.zip',root/'lean-4.21.0-linux.zip')
with zipfile.ZipFile(p) as z:z.extractall(root)
for p in (root/'lean-4.21.0-linux/bin').iterdir():p.chmod(p.stat().st_mode|0o111)
m=fetch('https://codeload.github.com/leanprover-community/mathlib4/tar.gz/308445d7985027f538e281e18df29ca16ede2ba3',root/'mathlib4.tar.gz');extract(m,root/'mathlib4')
for pkg in json.loads((root/'mathlib4/lake-manifest.json').read_text())['packages']:
 repo=pkg['url'].removeprefix('https://github.com/').removesuffix('.git');p=fetch('https://codeload.github.com/'+repo+'/tar.gz/'+pkg['rev'],root/(pkg['name']+'.tar.gz'));extract(p,root/'mathlib4/.lake/packages'/pkg['name'])
base='https://huggingface.co/datasets/leanpolish-anon/lean-proof-compression/resolve/64422193ada0449e2a60d4486955e7319920ed69/experiments/'
for n,h in [('complete_menu_pools.tar.gz','307d94f373bb657cbf33017d97c8e9af763c7447d8a08d3b543ac43e84b49dba'),('complete_menu_runs.tar.gz','448f5cb3d253d9859a776685d5779819f57a300d99a423b4ba73d3771e0d8656')]:
 fetch(base+n,out/n,h)
print('acquisition complete',flush=True)
